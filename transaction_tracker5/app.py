from flask import Flask, request, render_template_string, redirect, url_for, flash
from datetime import datetime
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'meta_engine_secure_key'

# ==========================================
# 1. THE META-CONFIGURATION MATRIX
# ==========================================
APP_TITLE = "The Architect | Retail POS Ledger"

SCHEMA_GROUPS = {
    "Transaction Identity": [
        "Receipt_Number", "Transaction_Date_Time", "Store_Location_ID", 
        "Register_Lane_Number", "Cashier_Employee_ID"
    ],
    "Basket Summary": [
        "Total_Item_Count", "Produce_Weighted_Lbs", "Meat_Weighted_Lbs", 
        "Alcohol_Tobacco_Present", "Physical_Coupons_Scanned"
    ],
    "Financials": [
        "Subtotal_Amount", "Tax_Amount", "Discount_Total", 
        "Final_Amount_Paid"
    ],
    "Payment Processing": [
        "Primary_Payment_Method", "Card_Network", "Card_Last_Four", 
        "EBT_SNAP_Amount_Applied", "Approval_Code", "Cash_Change_Returned"
    ],
    "Customer Loyalty": [
        "Loyalty_Member_ID", "Points_Earned_This_Txn", "Points_Redeemed", 
        "Digital_App_Scanned", "Lifetime_Value_Tier"
    ],
    "Exceptions & Logs": [
        "Voided_Transaction_Flag", "Refund_Return_Flag", "Supervisor_Override_ID", 
        "Self_Checkout_Flag", "General_Audit_Notes"
    ]
}

ALL_FIELDS = [field for group in SCHEMA_GROUPS.values() for field in group]

# The high-level overview for the Dashboard Ledger
LEDGER_HEADERS = [
    "Transaction_Date_Time", "Receipt_Number", "Total_Item_Count", 
    "Primary_Payment_Method", "Final_Amount_Paid", "Loyalty_Member_ID"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'dynamic_vault.db')

# ==========================================
# 2. HTML TEMPLATES (Dynamically Rendered)
# ==========================================
SHARED_CSS = """
    <style>
        :root { --bg: #0f172a; --surface: #1e293b; --primary: #38bdf8; --text: #f8fafc; --muted: #94a3b8; --border: #334155; --success: #10b981; --warning: #f59e0b; --danger: #f43f5e; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); padding: 2rem; margin: 0; }
        .container { max-width: 1200px; margin: auto; background: var(--surface); padding: 2rem; border-radius: 8px; border: 1px solid var(--border); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
        h1, h2 { color: var(--primary); text-transform: uppercase; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
        h2 { font-size: 1rem; color: var(--muted); margin-top: 2rem; }
        .nav { margin-bottom: 1.5rem; display: flex; gap: 1rem; }
        .nav a { color: var(--primary); text-decoration: none; font-weight: bold; padding: 0.5rem 1rem; border: 1px solid var(--primary); border-radius: 4px; transition: 0.2s; }
        .nav a:hover { background: var(--primary); color: #000; }
        .flash { padding: 1rem; background: rgba(16, 185, 129, 0.2); color: var(--success); border: 1px solid var(--success); margin-bottom: 1rem; text-align: center; border-radius: 4px; font-weight: bold; }
        .flash.error { background: rgba(244, 63, 94, 0.2); color: var(--danger); border-color: var(--danger); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
        .form-group { display: flex; flex-direction: column; }
        label { font-size: 0.75rem; color: var(--muted); margin-bottom: 0.3rem; text-transform: uppercase; }
        input, select, textarea { background: var(--bg); color: var(--text); border: 1px solid var(--border); padding: 0.75rem; border-radius: 4px; outline: none; }
        input:focus { border-color: var(--primary); }
        .btn-update { background: var(--warning); color: #000; border: none; padding: 1rem; width: 100%; font-weight: bold; cursor: pointer; border-radius: 4px; font-size: 1rem; margin-top: 2rem;}
        .btn-update:hover { opacity: 0.9; }
        .btn-delete { background: transparent; color: var(--danger); border: 1px solid var(--danger); padding: 0.5rem 1rem; width: 100%; font-weight: bold; cursor: pointer; border-radius: 4px; margin-top: 1rem; text-transform: uppercase; text-decoration: none; display: block; text-align: center; box-sizing: border-box;}
        .btn-delete:hover { background: var(--danger); color: #fff; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; text-align: left; font-size: 0.9rem; }
        th, td { padding: 0.75rem; border-bottom: 1px solid var(--border); }
        th { color: var(--muted); text-transform: uppercase; font-size: 0.75rem; }
        tr:hover { background: rgba(255,255,255,0.05); }
        .btn-edit { background: transparent; color: var(--primary); border: 1px solid var(--primary); padding: 0.3rem 0.6rem; text-decoration: none; border-radius: 4px; font-size: 0.75rem; font-weight: bold;}
        .btn-edit:hover { background: var(--primary); color: #000; }
    </style>
"""

HTML_LEDGER = SHARED_CSS + """
<!DOCTYPE html>
<html lang="en">
<head><title>{{ app_title }} | Ledger</title></head>
<body>
<div class="container">
    <div class="nav"><a href="/new">+ New Record</a> <a href="/ledger">View Ledger</a></div>
    <h1>{{ app_title }}</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, msg in messages %}
                <div class="flash {{ 'error' if category == 'error' else '' }}">{{ msg }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <table>
        <thead>
            <tr>
                <th>Created At</th>
                {% for header in ledger_headers %}
                    <th>{{ header.replace('_', ' ') }}</th>
                {% endfor %}
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for row in records %}
            <tr>
                <td>{{ row['Created_At'][:10] }}</td>
                {% for header in ledger_headers %}
                    <td style="font-weight:bold;">{{ row[header] if row[header] else '--' }}</td>
                {% endfor %}
                <td><a href="/edit/{{ row['Record_ID'] }}" class="btn-edit">OPEN CANVAS</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
</body>
</html>
"""

HTML_EDIT = SHARED_CSS + """
<!DOCTYPE html>
<html lang="en">
<head><title>{{ app_title }} | Deep Edit</title></head>
<body>
<div class="container">
    <div class="nav"><a href="/new">+ New Record</a> <a href="/ledger">View Ledger</a></div>
    <h1>Deep Edit :: {{ record['Record_ID'] }}</h1>
    
    <form action="/update/{{ record['Record_ID'] }}" method="POST">
        {% for group_name, fields in schema_groups.items() %}
            <h2>{{ group_name }}</h2>
            <div class="grid">
                {% for field in fields %}
                <div class="form-group">
                    <label>{{ field.replace('_', ' ') }}</label>
                    <input type="text" name="{{ field }}" value="{{ record[field] if record[field] != None else '' }}">
                </div>
                {% endfor %}
            </div>
        {% endfor %}
        
        <button type="submit" class="btn-update">COMMIT OVERRIDES</button>
    </form>
    
    <a href="/delete/{{ record['Record_ID'] }}" class="btn-delete" onclick="return confirm('Are you sure you want to permanently delete this record?');">REMOVE RECORD</a>
</div>
</body>
</html>
"""

# ==========================================
# 3. GENERALIZED ROUTING LOGIC
# ==========================================
@app.route('/')
def home():
    return redirect(url_for('view_ledger'))

@app.route('/ledger')
def view_ledger():
    if not os.path.exists(DB_FILE):
        return "Database Vault not found. Please run init_database.py first."

    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM dynamic_ledger ORDER BY Created_At DESC", conn)
    conn.close()
    
    # Bulletproof data sanitization for the UI
    df = df.where(pd.notnull(df), None)
    records = df.to_dict('records')
    
    return render_template_string(
        HTML_LEDGER, 
        records=records, 
        ledger_headers=LEDGER_HEADERS,
        app_title=APP_TITLE
    )

@app.route('/new')
def new_record():
    """Generates a blank UUID skeleton based on the dynamic schema and jumps to Edit."""
    if not os.path.exists(DB_FILE):
        return "Database Vault not found. Please run init_database.py first."

    now = datetime.now()
    record_id = f"REC_{int(now.timestamp())}"
    created_at = now.strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dynamic_ledger (Record_ID, Created_At) VALUES (?, ?)", (record_id, created_at))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        flash(f"Database generation error: {e}", "error")
        return redirect(url_for('view_ledger'))
    finally:
        conn.close()

    return redirect(url_for('edit_record', record_id=record_id))

@app.route('/edit/<record_id>')
def edit_record(record_id):
    """Pulls the specific record and dynamically iterates through SCHEMA_GROUPS to build inputs."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM dynamic_ledger WHERE Record_ID = ?", conn, params=(record_id,))
    conn.close()

    if df.empty:
        flash("Record not found.", "error")
        return redirect(url_for('view_ledger'))

    record_dict = df.where(pd.notnull(df), None).iloc[0].to_dict()
    
    return render_template_string(
        HTML_EDIT, 
        record=record_dict, 
        schema_groups=SCHEMA_GROUPS,
        app_title=APP_TITLE
    )

@app.route('/update/<record_id>', methods=['POST'])
def update_record(record_id):
    """Dynamically reads the submitted form and updates the respective columns."""
    form = request.form.to_dict()
    
    updates = []
    values = []
    
    for field in ALL_FIELDS:
        if field in form:
            updates.append(f"{field} = ?")
            # Save everything as string; SQLite handles dynamic typing effectively
            values.append(str(form[field]) if form[field] != '' else None)

    values.append(record_id)

    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE dynamic_ledger SET {', '.join(updates)} WHERE Record_ID = ?", tuple(values))
        conn.commit()
        flash(f"Record {record_id} successfully updated.", "success")
    except sqlite3.Error as e:
        conn.rollback()
        flash(f"SQL Error: {e}", "error")
    finally:
        conn.close()

    return redirect(url_for('view_ledger'))

@app.route('/delete/<record_id>')
def delete_record(record_id):
    """The Kill Switch."""
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dynamic_ledger WHERE Record_ID = ?", (record_id,))
        conn.commit()
        flash(f"Record {record_id} permanently purged.", "success")
    except sqlite3.Error as e:
        conn.rollback()
        flash(f"Failed to delete record: {e}", "error")
    finally:
        conn.close()

    return redirect(url_for('view_ledger'))

if __name__ == '__main__':
    print(f"⚙️ Booting Meta-Engine: {APP_TITLE} (Ledger Active)")
    app.config['TEMPLATES_AUTO_RELOAD'] = True 
    app.run(debug=True, use_reloader=True, port=5005)