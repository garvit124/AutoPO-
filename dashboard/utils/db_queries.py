import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from config.db_config import DB_CONFIG
import pandas as pd

def get_db_connection():
    """Get PostgreSQL database connection."""
    return psycopg2.connect(**DB_CONFIG)

def get_po_summary():
    """Get summary statistics for purchase orders."""
    conn = get_db_connection()
    query = """
        SELECT 
            COUNT(*) as total_pos,
            COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
            COUNT(CASE WHEN status = 'PARTIAL_COMPLETED' THEN 1 END) as partial,
            COUNT(CASE WHEN status = 'WAITING_FOR_REPLY' THEN 1 END) as pending,
            COUNT(CASE WHEN status LIKE 'FAILED%' OR status = 'CANCELLED_BY_CUSTOMER' THEN 1 END) as failed
        FROM purchase_orders
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_all_pos():
    """Get all purchase orders with details."""
    conn = get_db_connection()
    try:
        query = """
            SELECT 
                po_id, po_number, po_date, buyer, supplier, 
                total_amount, status, sender_email, created_at
            FROM purchase_orders
            ORDER BY created_at DESC
        """
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(f"Fallback: created_at column missing? {e}")
        query = """
            SELECT 
                po_id, po_number, po_date, buyer, supplier, 
                total_amount, status, sender_email
            FROM purchase_orders
        """
        df = pd.read_sql(query, conn)
        if 'created_at' not in df.columns:
            df['created_at'] = pd.Timestamp.now()
            
    conn.close()
    return df


def get_po_details(po_id):
    """Get detailed information for a specific PO including line items."""
    conn = get_db_connection()
    
    # Get header
    header_query = """
        SELECT * FROM purchase_orders WHERE po_id = %s
    """
    header_df = pd.read_sql(header_query, conn, params=(po_id,))
    
    # Get line items
    items_query = """
        SELECT * FROM purchase_order_items WHERE po_id = %s
    """
    items_df = pd.read_sql(items_query, conn, params=(po_id,))
    
    conn.close()
    return header_df, items_df

def get_monthly_sales():
    """Get top selling products for current month."""
    conn = get_db_connection()
    try:
        query = """
            SELECT 
                i.product_name,
                SUM(poi.quantity) as total_quantity,
                SUM(poi.line_total) as total_revenue
            FROM purchase_order_items poi
            JOIN purchase_orders po ON poi.po_id = po.po_id
            JOIN inventory i ON poi.product_id = i.product_id
            WHERE po.status IN ('COMPLETED', 'PARTIAL_COMPLETED')
            AND EXTRACT(MONTH FROM po.created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
            AND EXTRACT(YEAR FROM po.created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
            GROUP BY i.product_name
            ORDER BY total_quantity DESC
            LIMIT 10
        """
        df = pd.read_sql(query, conn)
    except:
        # Fallback without date filtering if columns are missing
        query = """
            SELECT 
                i.product_name,
                SUM(poi.quantity) as total_quantity,
                SUM(poi.line_total) as total_revenue
            FROM purchase_order_items poi
            JOIN purchase_orders po ON poi.po_id = po.po_id
            JOIN inventory i ON poi.product_id = i.product_id
            GROUP BY i.product_name
            ORDER BY total_quantity DESC
            LIMIT 10
        """
        df = pd.read_sql(query, conn)
        
    conn.close()
    return df


def get_email_count():
    """Get count of emails processed."""
    conn = get_db_connection()
    query = """
        SELECT COUNT(*) as total_emails
        FROM purchase_orders
        WHERE sender_email IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.iloc[0]['total_emails'] if not df.empty else 0

def get_recent_activity(limit=10):
    """Get recent PO activity."""
    conn = get_db_connection()
    try:
        query = """
            SELECT 
                po_number, buyer, status, total_amount, created_at
            FROM purchase_orders
            ORDER BY created_at DESC
            LIMIT %s
        """
        df = pd.read_sql(query, conn, params=(limit,))
    except:
        query = "SELECT po_number, buyer, status, total_amount FROM purchase_orders LIMIT %s"
        df = pd.read_sql(query, conn, params=(limit,))
        if 'created_at' not in df.columns:
            df['created_at'] = pd.Timestamp.now()
            
    conn.close()
    return df


def get_inventory_status():
    """Get current inventory status."""
    conn = get_db_connection()
    query = "SELECT product_id, product_name, stock_available, units_sold FROM inventory ORDER BY product_id"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


