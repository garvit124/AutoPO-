import os
import json
from datetime import datetime

def get_invoice_list():
    """Get list of generated invoices."""
    invoice_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "invoices")
    
    if not os.path.exists(invoice_dir):
        return []
    
    invoices = []
    for filename in os.listdir(invoice_dir):
        if filename.endswith('.pdf'):
            filepath = os.path.join(invoice_dir, filename)
            stat = os.stat(filepath)
            invoices.append({
                'filename': filename,
                'path': filepath,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_mtime)
            })
    
    return sorted(invoices, key=lambda x: x['created'], reverse=True)

def get_json_files():
    """Get list of processed JSON files."""
    json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "processed_json")
    
    if not os.path.exists(json_dir):
        return []
    
    json_files = []
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(json_dir, filename)
            stat = os.stat(filepath)
            json_files.append({
                'filename': filename,
                'path': filepath,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_mtime)
            })
    
    return sorted(json_files, key=lambda x: x['created'], reverse=True)

def read_json_file(filepath):
    """Read and return JSON file content."""
    with open(filepath, 'r') as f:
        return json.load(f)
