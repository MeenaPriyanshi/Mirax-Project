from flask import Flask, request, jsonify, render_template
import mysql.connector
import jwt
import datetime
import json
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iitk_athletics_super_secret_key'

# --- Email Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'thevinchi007@gmail.com'
app.config['MAIL_PASSWORD'] = 'kvgknqqouleriixt'
mail = Mail(app)

# --- Temporary Stores (For OTPs) ---
otp_store = {}
reg_otp_store = {}


# --- Database Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sujalm@24",  # Your MySQL password
        database="birthday_management_system"
    )


# --- Authentication Middleware ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM accounts WHERE id = %s", (data['id'],))
            current_user = cursor.fetchone()
            db.close()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


# ==========================================
# HTML PAGE ROUTES
# ==========================================
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')


@app.route('/manager/dashboard')
def manager_dashboard():
    return render_template('manager_dashboard.html')


@app.route('/member/dashboard')
def member_dashboard():
    return render_template('member_dashboard.html')


# ==========================================
# API ROUTES: FORGOT PASSWORD
# ==========================================
@app.route('/api/forgot-password/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()

    if not user:
        return jsonify({'message': 'No account found with that email'}), 404

    otp = str(random.randint(100000, 999999))
    otp_store[email] = {'otp': otp, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}

    msg = Message("IITK Athletics - Password Reset OTP", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Your OTP for resetting your password is: {otp}\nThis code will expire in 10 minutes."
    mail.send(msg)

    return jsonify({'message': 'OTP sent successfully'})


@app.route('/api/forgot-password/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    record = otp_store.get(email)
    if not record or record['otp'] != otp or datetime.datetime.utcnow() > record['exp']:
        return jsonify({'message': 'Invalid or expired OTP'}), 400

    return jsonify({'message': 'OTP verified'})


@app.route('/api/forgot-password/reset', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    hashed_pw = generate_password_hash(password, method='scrypt')
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE accounts SET password_hash = %s WHERE email = %s", (hashed_pw, email))
    db.commit()
    db.close()

    if email in otp_store:
        del otp_store[email]

    return jsonify({'message': 'Password reset successfully!'})


# ==========================================
# API ROUTES: LOGIN & REGISTRATION
# ==========================================
@app.route('/api/register/send-otp', methods=['POST'])
def register_send_otp():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accounts WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()
    db.close()

    if existing_user:
        return jsonify({'error': 'Username or email already exists in our system.'}), 400

    otp = str(random.randint(100000, 999999))
    reg_otp_store[email] = {
        'otp': otp,
        'username': username,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    msg = Message("IITK Athletics - Verify Your Email", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Welcome to the Athletics Tracker!\n\nYour registration OTP is: {otp}\n\nThis code will expire in 10 minutes."
    mail.send(msg)

    return jsonify({'message': 'OTP sent successfully to your email.'})


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    record = reg_otp_store.get(email)
    if not record or record['otp'] != otp or datetime.datetime.utcnow() > record['exp']:
        return jsonify({'error': 'Invalid or expired OTP'}), 400

    hashed_password = generate_password_hash(record['password'], method='scrypt')
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO accounts (username, email, password_hash, role) VALUES (%s, %s, %s, 'member')",
                       (record['username'], email, hashed_password))
        db.commit()
        del reg_otp_store[email]
        return jsonify({'message': 'Registered successfully!'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while saving your account.'}), 500
    finally:
        db.close()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accounts WHERE username = %s", (data['username'],))
    user = cursor.fetchone()
    db.close()

    if user and check_password_hash(user['password_hash'], data['password']):
        token = jwt.encode({
            'id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token, 'role': user['role'], 'username': user['username']})
    return jsonify({'message': 'Invalid credentials'}), 401


# ==========================================
# API ROUTES: MANAGER
# ==========================================
@app.route('/api/manager/birthdays', methods=['GET', 'POST', 'DELETE'])
@token_required
def manage_birthdays(current_user):
    if current_user['role'] != 'manager': return jsonify({'message': 'Unauthorized'}), 403
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM birthdays ORDER BY MONTH(dob), DAY(dob)")
        result = cursor.fetchall()
        db.close()
        return jsonify(result)

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            df = pd.read_csv(file)

            df.columns = df.columns.str.lower().str.strip()

            name_col = next((col for col in df.columns if 'name' in col), None)
            batch_col = next((col for col in df.columns if 'batch' in col), None)
            dob_col = next((col for col in df.columns if 'dob' in col or 'date' in col), None)

            if not name_col or not dob_col:
                db.close()
                return jsonify({'error': 'Spreadsheet must contain a Name and DOB column.'}), 400

            from datetime import datetime
            for _, row in df.iterrows():
                if pd.isna(row[name_col]) or pd.isna(row[dob_col]):
                    continue

                name_val = str(row[name_col]).strip()
                batch_val = str(row[batch_col]).strip() if batch_col and not pd.isna(row[batch_col]) else "N/A"
                dob_val = str(row[dob_col]).strip()

                try:
                    parsed_date = datetime.strptime(f"{dob_val} 2000", "%d %B %Y").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        parsed_date = pd.to_datetime(dob_val).strftime("%Y-%m-%d")
                    except Exception:
                        continue

                cursor.execute("INSERT INTO birthdays (Name, Batch, dob) VALUES (%s, %s, %s)",
                               (name_val, batch_val, parsed_date))
        else:
            data = request.get_json()
            cursor.execute("INSERT INTO birthdays (Name, Batch, dob) VALUES (%s, %s, %s)",
                           (data['name'], data['batch'], data['dob']))
        db.commit()
        db.close()
        return jsonify({'message': 'Added successfully'})

    if request.method == 'DELETE':
        data = request.get_json()
        cursor.execute("DELETE FROM birthdays WHERE Sl_no = %s", (data['Sl_no'],))
        db.commit()
        db.close()
        return jsonify({'message': 'Deleted successfully'})


@app.route('/api/manager/pending', methods=['GET', 'POST'])
@token_required
def manage_pending(current_user):
    if current_user['role'] != 'manager': return jsonify({'message': 'Unauthorized'}), 403
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("""
                       SELECT p.id, b.Sl_no, b.Name, b.Batch, b.dob
                       FROM postponed p
                                JOIN birthdays b ON p.Sl = b.Sl_no
                       """)
        result = cursor.fetchall()
        db.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.get_json()
        format_strings = ','.join(['%s'] * len(data['celebrated_ids']))
        if format_strings:
            cursor.execute(f"DELETE FROM postponed WHERE id IN ({format_strings})", tuple(data['celebrated_ids']))
            db.commit()
        db.close()
        return jsonify({'message': 'Updated pending list'})


@app.route('/api/manager/messages', methods=['GET', 'DELETE'])
@token_required
def view_messages(current_user):
    if current_user['role'] != 'manager': return jsonify({'message': 'Unauthorized'}), 403
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("""
                       SELECT m.id, m.topic, m.description, m.created_at, a.username as sender
                       FROM messages m
                                JOIN accounts a ON m.member_id = a.id
                       ORDER BY m.created_at DESC
                       """)
        result = cursor.fetchall()
        db.close()
        return jsonify(result)

    if request.method == 'DELETE':
        data = request.get_json()
        cursor.execute("DELETE FROM messages WHERE id = %s", (data['msg_id'],))
        db.commit()
        db.close()
        return jsonify({'message': 'Message deleted successfully'})


# ==========================================
# API ROUTES: MEMBER
# ==========================================
@app.route('/api/member/birthdays', methods=['GET'])
@token_required
def member_view_birthdays(current_user):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM birthdays ORDER BY MONTH(dob), DAY(dob)")
    all_bday = cursor.fetchall()
    db.close()
    return jsonify(all_bday)


@app.route('/api/member/selected', methods=['GET', 'POST'])
@token_required
def manage_selected_birthdays(current_user):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'GET':
        selected_ids = json.loads(current_user['selected_birthdays'] or '[]')
        if not selected_ids: return jsonify([])
        format_strings = ','.join(['%s'] * len(selected_ids))
        cursor.execute(f"SELECT * FROM birthdays WHERE Sl_no IN ({format_strings})", tuple(selected_ids))
        result = cursor.fetchall()
        db.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.get_json()
        selected_ids = json.loads(current_user['selected_birthdays'] or '[]')
        if data['Sl_no'] not in selected_ids:
            selected_ids.append(data['Sl_no'])
            cursor.execute("UPDATE accounts SET selected_birthdays = %s WHERE id = %s",
                           (json.dumps(selected_ids), current_user['id']))
            db.commit()
        db.close()
        return jsonify({'message': 'Added to selected list'})


@app.route('/api/member/message', methods=['POST'])
@token_required
def send_message(current_user):
    data = request.get_json()
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (member_id, topic, description) VALUES (%s, %s, %s)",
                   (current_user['id'], data['topic'], data['description']))
    db.commit()
    db.close()
    return jsonify({'message': 'Message sent to Manager'})


# ==========================================
# AUTOMATED EMAILS (CRON JOBS)
# ==========================================
def daily_tasks():
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        today = datetime.date.today()

        cursor.execute("SELECT * FROM birthdays WHERE MONTH(dob) = %s AND DAY(dob) = %s", (today.month, today.day))
        todays_bdays = cursor.fetchall()

        cursor.execute("SELECT b.Name, b.Batch FROM postponed p JOIN birthdays b ON p.Sl = b.Sl_no")
        pending_bdays = cursor.fetchall()

        cursor.execute("SELECT email FROM accounts WHERE role = 'manager' LIMIT 1")
        manager = cursor.fetchone()

        if manager:
            if todays_bdays:
                msg_body = "Birthdays Today:\n" + "\n".join([f"- {b['Name']} ({b['Batch']})" for b in todays_bdays])
                msg = Message("Action Required: Today's Athletics Birthdays", sender=app.config['MAIL_USERNAME'],
                              recipients=[manager['email']])
                msg.body = msg_body + "\n\nPlease remember to update the dashboard at the end of the day if these were celebrated!"
                mail.send(msg)

                for b in todays_bdays:
                    cursor.execute("INSERT INTO postponed (Sl) VALUES (%s)", (b['Sl_no'],))
                db.commit()

            if pending_bdays:
                msg_body = "Pending Celebrations:\n" + "\n".join(
                    [f"- {b['Name']} ({b['Batch']})" for b in pending_bdays])
                msg = Message("Reminder: Pending Birthday Celebrations", sender=app.config['MAIL_USERNAME'],
                              recipients=[manager['email']])
                msg.body = msg_body
                mail.send(msg)

        db.close()


scheduler = BackgroundScheduler()
# Run daily exactly at 12:00:02 AM
scheduler.add_job(func=daily_tasks, trigger="cron", hour=0, minute=0, second=2)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)