"""
General Appointment Booking System - BookMyShow Theme Edition
A Flask-based web application supporting Doctor, Salon, and Vehicle Service appointments.
Demonstration application for educational / workshop presentation.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "bookings.db")

# --- BookMyShow Style Enriched Services Data ---
SERVICES = {
    "Doctor": {
        "icon": "🏥",
        "tag": "Healthcare & Wellness",
        "color": "#f84464",
        "badge": "VERIFIED CLINICS",
        "description": "Consult verified specialist doctors with instant confirmed tokens.",
        "services": [
            {
                "id": "doc_general",
                "name": "General Consultation",
                "provider": "Dr. A. Kumar",
                "specialty": "MBBS, MD • Senior Physician",
                "duration": "30 min",
                "price": "₹500",
                "rating": "4.9",
                "votes": "2.4k",
                "languages": "English, Hindi",
                "badge": "BESTSELLER",
                "location": "CareMax Hospital, Indiranagar",
                "image": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=700&q=80",
            },
            {
                "id": "doc_dental",
                "name": "Dental Checkup",
                "provider": "Dr. S. Patel",
                "specialty": "BDS, MDS • Cosmetic Dental Surgeon",
                "duration": "45 min",
                "price": "₹650",
                "rating": "4.8",
                "votes": "1.8k",
                "languages": "English, Hindi, Gujarati",
                "badge": "POPULAR",
                "location": "SmileStudio, Koramangala",
                "image": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=700&q=80",
            },
            {
                "id": "doc_eye",
                "name": "Eye Examination",
                "provider": "Dr. R. Iyer",
                "specialty": "MS (Ophthalmology) • Retina Specialist",
                "duration": "30 min",
                "price": "₹450",
                "rating": "4.7",
                "votes": "1.2k",
                "languages": "English, Tamil, Hindi",
                "badge": "RECOMMENDED",
                "location": "VisionCare Centre, Jayanagar",
                "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=700&q=80",
            },
        ],
    },
    "Salon": {
        "icon": "💇",
        "tag": "Grooming & Luxury Spa",
        "color": "#e040fb",
        "badge": "TRENDING NOW",
        "description": "Premium haircut, styling & rejuvenation by top master stylists.",
        "services": [
            {
                "id": "sal_haircut",
                "name": "Haircut",
                "provider": "Stylist Meena",
                "specialty": "Senior Hair Artist • Toni & Guy Alumni",
                "duration": "30 min",
                "price": "₹350",
                "rating": "4.9",
                "votes": "3.8k",
                "languages": "English, Hindi",
                "badge": "TOP RATED",
                "location": "Glamour Lounge, Indiranagar",
                "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=700&q=80",
            },
            {
                "id": "sal_styling",
                "name": "Hair Styling",
                "provider": "Stylist Priya",
                "specialty": "Creative Director • Loreal Professional",
                "duration": "60 min",
                "price": "₹799",
                "rating": "4.8",
                "votes": "2.1k",
                "languages": "English, Hindi, Kannada",
                "badge": "PREMIUM",
                "location": "Enrich Studio, MG Road",
                "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=700&q=80",
            },
            {
                "id": "sal_facial",
                "name": "Facial",
                "provider": "Stylist Kavya",
                "specialty": "Aesthetician • Hydra & Gold Facial Expert",
                "duration": "45 min",
                "price": "₹599",
                "rating": "4.8",
                "votes": "1.5k",
                "languages": "English, Hindi",
                "badge": "POPULAR",
                "location": "Urban Spa Retreat, Whitefield",
                "image": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=700&q=80",
            },
        ],
    },
    "Vehicle Service": {
        "icon": "🔧",
        "tag": "Automotive & Express Care",
        "color": "#00e676",
        "badge": "AUTHORIZED WORKSHOPS",
        "description": "Certified mechanical repairs, multi-point checkup & periodic maintenance.",
        "services": [
            {
                "id": "veh_oil",
                "name": "Oil Change",
                "provider": "Tech. Ravi",
                "specialty": "Master Mechanic • Mobil1 & Shell Certified",
                "duration": "45 min",
                "price": "₹899",
                "rating": "4.9",
                "votes": "4.2k",
                "languages": "English, Hindi, Telugu",
                "badge": "BESTSELLER",
                "location": "SpeedyPit Auto Hub, Electronic City",
                "image": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=700&q=80",
            },
            {
                "id": "veh_general",
                "name": "General Maintenance",
                "provider": "Tech. Suresh",
                "specialty": "Chief Diagnostic Engineer • 40-Point Scan",
                "duration": "90 min",
                "price": "₹1499",
                "rating": "4.8",
                "votes": "2.9k",
                "languages": "English, Hindi",
                "badge": "COMPREHENSIVE",
                "location": "Bosch Auto Centre, Bellandur",
                "image": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=700&q=80",
            },
            {
                "id": "veh_tyres",
                "name": "Tyre Rotation",
                "provider": "Tech. Anil",
                "specialty": "3D Wheel Alignment & Laser Balancing",
                "duration": "30 min",
                "price": "₹499",
                "rating": "4.7",
                "votes": "1.9k",
                "languages": "English, Hindi",
                "badge": "EXPRESS",
                "location": "WheelAlign Express, HSR Layout",
                "image": "https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=700&q=80",
            },
        ],
    },
}

TIME_SLOTS = [
    "09:00 AM",
    "10:00 AM",
    "11:00 AM",
    "12:00 PM",
    "02:00 PM",
    "03:00 PM",
    "04:00 PM",
]


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name    TEXT NOT NULL,
                contact_number   TEXT NOT NULL,
                category         TEXT NOT NULL,
                service_id       TEXT NOT NULL,
                service_name     TEXT NOT NULL,
                provider         TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                created_at       TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE (service_id, appointment_date, appointment_time)
            )
        """)
        conn.commit()


def get_available_dates():
    dates = []
    day = datetime.today() + timedelta(days=1)
    while len(dates) < 7:
        if day.weekday() != 6:  # Skip Sunday
            dates.append(day.strftime("%Y-%m-%d"))
        day += timedelta(days=1)
    return dates


def get_date_cards():
    """Return structured date info for BookMyShow horizontal date picker."""
    date_list = []
    day = datetime.today() + timedelta(days=1)
    while len(date_list) < 7:
        if day.weekday() != 6:
            date_list.append({
                "iso": day.strftime("%Y-%m-%d"),
                "day_name": day.strftime("%a").upper(),
                "day_num": day.strftime("%d"),
                "month_name": day.strftime("%b").upper(),
            })
        day += timedelta(days=1)
    return date_list


def get_service_by_id(service_id):
    for category, data in SERVICES.items():
        for svc in data["services"]:
            if svc["id"] == service_id:
                return category, svc
    return None, None


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    # Pass flattened list of top spotlight items as well
    spotlight = []
    for cat, data in SERVICES.items():
        for s in data["services"]:
            spotlight.append({**s, "category": cat, "cat_color": data["color"], "cat_icon": data["icon"]})
    return render_template("index.html", services=SERVICES, spotlight=spotlight)


@app.route("/book")
def book():
    category = request.args.get("category", "")
    service_id = request.args.get("service_id", "")
    
    # Pre-select first service if category provided but service not chosen
    if category and not service_id and category in SERVICES:
        if SERVICES[category]["services"]:
            service_id = SERVICES[category]["services"][0]["id"]

    return render_template(
        "book.html",
        services=SERVICES,
        time_slots=TIME_SLOTS,
        available_dates=get_available_dates(),
        date_cards=get_date_cards(),
        selected_category=category,
        selected_service_id=service_id,
    )


@app.route("/api/slots")
def api_slots():
    sid = request.args.get("service_id", "")
    date = request.args.get("date", "")
    if not sid or not date:
        return jsonify({"error": "Missing parameters"}), 400
    with get_db() as conn:
        rows = conn.execute(
            "SELECT appointment_time FROM bookings WHERE service_id=? AND appointment_date=?",
            (sid, date),
        ).fetchall()
    return jsonify({
        "booked": [r["appointment_time"] for r in rows],
        "all_slots": TIME_SLOTS,
    })


@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.get_json(force=True)
    required = [
        "customer_name",
        "contact_number",
        "service_id",
        "appointment_date",
        "appointment_time",
    ]
    for f in required:
        if not data.get(f, "").strip():
            return jsonify({"success": False, "error": f'Field "{f}" is required.'}), 400

    name = data["customer_name"].strip()
    phone = data["contact_number"].strip()
    sid = data["service_id"].strip()
    date = data["appointment_date"].strip()
    time = data["appointment_time"].strip()

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"success": False, "error": "Contact number must be exactly 10 digits."}), 400
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"success": False, "error": "Invalid date format."}), 400
    if time not in TIME_SLOTS:
        return jsonify({"success": False, "error": "Invalid time slot selected."}), 400

    category, svc = get_service_by_id(sid)
    if not svc:
        return jsonify({"success": False, "error": "Unknown service selected."}), 400

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO bookings
                (customer_name, contact_number, category, service_id, service_name,
                 provider, appointment_date, appointment_time, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    name,
                    phone,
                    category,
                    sid,
                    svc["name"],
                    svc["provider"],
                    date,
                    time,
                    created_at,
                ),
            )
            conn.commit()
            bid = conn.execute("SELECT last_insert_rowid() AS rid").fetchone()["rid"]
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "error": f"Sorry! The {time} slot on {date} for {svc['name']} is already booked. Please choose another slot.",
        }), 409

    return jsonify({
        "success": True,
        "booking": {
            "id": bid,
            "customer_name": name,
            "contact_number": phone,
            "category": category,
            "service_name": svc["name"],
            "provider": svc["provider"],
            "appointment_date": date,
            "appointment_time": time,
            "created_at": created_at,
        },
    })


@app.route("/confirmation")
def confirmation():
    bid = request.args.get("booking_id")
    if not bid:
        return redirect(url_for("home"))
    with get_db() as conn:
        booking = conn.execute("SELECT * FROM bookings WHERE id=?", (bid,)).fetchone()
    if not booking:
        return redirect(url_for("home"))

    _, svc_details = get_service_by_id(booking["service_id"])
    return render_template("confirmation.html", booking=booking, service_details=svc_details)


@app.route("/my-bookings")
def my_bookings():
    contact = request.args.get("contact", "").strip()
    bookings = []
    if contact:
        with get_db() as conn:
            bookings = conn.execute(
                "SELECT * FROM bookings WHERE contact_number=? ORDER BY appointment_date, appointment_time",
                (contact,),
            ).fetchall()
    return render_template("my_bookings.html", bookings=bookings, contact=contact)


if __name__ == "__main__":
    init_db()
    print("=" * 65)
    print("  [BookMySlot] - General Appointment Booking System")
    print("  DEMONSTRATION APPLICATION - Not for real medical/commercial use")
    print("  Running at: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(debug=True, port=5000)
