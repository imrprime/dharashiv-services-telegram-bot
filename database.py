import sqlite3
import datetime
import csv
import io
import os
from typing import Optional, List, Dict, Any

DB_PATH = os.getenv("DB_PATH", "leads.db")

def get_connection():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        phone TEXT,
        language TEXT DEFAULT 'mr',
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Leads / Service Requests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_code TEXT UNIQUE,
        telegram_id INTEGER,
        customer_name TEXT,
        customer_phone TEXT,
        service_id TEXT,
        service_title TEXT,
        problem_description TEXT,
        location_area TEXT,
        preferred_time TEXT,
        status TEXT DEFAULT 'NEW',
        admin_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
    )
    """)
    
    conn.commit()
    conn.close()

def save_or_update_user(telegram_id: int, username: str = "", full_name: str = "", phone: str = "", language: str = "mr", address: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT telegram_id, language FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if row:
        cursor.execute("""
            UPDATE users
            SET username = COALESCE(NULLIF(?, ''), username),
                full_name = COALESCE(NULLIF(?, ''), full_name),
                phone = COALESCE(NULLIF(?, ''), phone),
                address = COALESCE(NULLIF(?, ''), address),
                updated_at = ?
            WHERE telegram_id = ?
        """, (username, full_name, phone, address, now, telegram_id))
    else:
        cursor.execute("""
            INSERT INTO users (telegram_id, username, full_name, phone, language, address, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (telegram_id, username, full_name, phone, language, address, now, now))
        
    conn.commit()
    conn.close()

def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def set_user_language(telegram_id: int, lang: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE telegram_id = ?", (lang, telegram_id))
    conn.commit()
    conn.close()

def generate_ref_code(lead_id: int) -> str:
    today = datetime.datetime.now().strftime("%y%m%d")
    return f"DH-{today}-{lead_id:04d}"

def create_lead(
    telegram_id: int,
    customer_name: str,
    customer_phone: str,
    service_id: str,
    service_title: str,
    problem_description: str,
    location_area: str,
    preferred_time: str = ""
) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO leads (
            telegram_id, customer_name, customer_phone, service_id,
            service_title, problem_description, location_area,
            preferred_time, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'NEW', ?, ?)
    """, (
        telegram_id, customer_name, customer_phone, service_id,
        service_title, problem_description, location_area,
        preferred_time, now, now
    ))
    
    lead_id = cursor.lastrowid
    ref_code = generate_ref_code(lead_id)
    
    cursor.execute("UPDATE leads SET ref_code = ? WHERE id = ?", (ref_code, lead_id))
    conn.commit()
    
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    
    # Also update user's profile with latest contact and address
    save_or_update_user(telegram_id=telegram_id, full_name=customer_name, phone=customer_phone, address=location_area)
    
    return dict(row) if row else {}

def get_lead(lead_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_lead_by_ref(ref_code: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE ref_code = ?", (ref_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_leads(telegram_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM leads
        WHERE telegram_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (telegram_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_leads(limit: int = 10, status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("""
            SELECT * FROM leads
            WHERE status = ?
            ORDER BY id DESC
            LIMIT ?
        """, (status, limit))
    else:
        cursor.execute("""
            SELECT * FROM leads
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_lead_status(lead_id: int, new_status: str, notes: Optional[str] = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if notes is not None:
        cursor.execute("""
            UPDATE leads
            SET status = ?, admin_notes = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, notes, now, lead_id))
    else:
        cursor.execute("""
            UPDATE leads
            SET status = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, now, lead_id))
        
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def export_leads_to_csv() -> str:
    """Exports all leads to a CSV string buffer."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "Lead ID", "Reference Code", "Telegram ID", "Customer Name",
        "Phone Number", "Service", "Problem / Details", "Area / Village",
        "Preferred Time", "Status", "Admin Notes", "Created At", "Updated At"
    ])
    
    for row in rows:
        writer.writerow([
            row["id"], row["ref_code"], row["telegram_id"], row["customer_name"],
            row["customer_phone"], row["service_title"], row["problem_description"],
            row["location_area"], row["preferred_time"], row["status"],
            row["admin_notes"] or "", row["created_at"], row["updated_at"]
        ])
        
    return output.getvalue()
