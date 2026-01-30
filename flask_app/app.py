import os
import sys
from flask import Flask, render_template, jsonify, request
import pandas as pd

# Add the project root to the path so we can import from dashboard.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.utils.db_queries import (
    get_po_summary, get_recent_activity, get_monthly_sales, 
    get_all_pos, get_inventory_status, get_email_count
)
from dashboard.utils.file_utils import get_invoice_list, get_json_files

app = Flask(__name__)

@app.route('/')
def home():
    summary_df = get_po_summary()
    email_stats = get_email_count()
    
    summary = {
        'total_pos': summary_df['total'].iloc[0] if not summary_df.empty else 0,
        'completed': summary_df['completed'].iloc[0] if not summary_df.empty else 0,
        'failed': summary_df['failed'].iloc[0] if not summary_df.empty else 0,
        'total_emails': email_stats['total_emails'].iloc[0] if not email_stats.empty else 0
    }
    
    activity_df = get_recent_activity(10)
    activity = activity_df.to_dict('records')
    
    sales_df = get_monthly_sales()
    sales_data = sales_df.to_dict('records')
    
    status_data = {
        'completed': int(summary_df['completed'].iloc[0]) if not summary_df.empty else 0,
        'partial': int(summary_df['partial'].iloc[0]) if not summary_df.empty else 0,
        'pending': int(summary_df['pending'].iloc[0]) if not summary_df.empty else 0,
        'failed': int(summary_df['failed'].iloc[0]) if not summary_df.empty else 0
    }
    
    return render_template('index.html', summary=summary, activity=activity, sales_data=sales_data, status_data=status_data)

@app.route('/orders')
def orders():
    pos = get_all_pos().to_dict('records')
    return render_template('orders.html', orders=pos)

@app.route('/inventory')
def inventory():
    inv_df = get_inventory_status()
    inventory = inv_df.to_dict('records')
    return render_template('inventory.html', inventory=inventory)

@app.route('/invoices')
def invoices():
    inv_files = get_invoice_list()
    return render_template('invoices.html', invoices=inv_files)

@app.route('/emails')
def emails():
    # Reuse PO data for email monitoring as per original dashboard
    pos = get_all_pos().to_dict('records')
    email_stats = get_email_count().to_dict('records')[0] if not get_email_count().empty else {}
    return render_template('emails.html', emails=pos, stats=email_stats)

@app.route('/json-files')
def json_files():
    files = get_json_files()
    return render_template('json_files.html', json_files=files)

@app.route('/control-center')
def control_center():
    return render_template('control.html')

@app.route('/api/json-view')
def json_view():
    path = request.args.get('path')
    if path and os.path.exists(path):
        from dashboard.utils.file_utils import read_json_file
        return jsonify(read_json_file(path))
    return jsonify({"error": "File not found"}), 404

# API Endpoints for interactive features
@app.route('/api/pipeline/run', methods=['POST'])
def run_pipeline():
    # Placeholder for running the pipeline (IMAP + OCR)
    # In a real app, this would use Celery or a background thread
    return jsonify({"status": "success", "message": "Pipeline triggered."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
