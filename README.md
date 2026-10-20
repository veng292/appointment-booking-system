# 🎟️ BookMySlot — General Appointment Booking System

A modern, **humanized light-themed** appointment booking web application inspired by **BookMyShow**, supporting three distinct service categories under a single unified booking engine:

1. **🏥 Doctor Appointments** (General Consultation, Dental Checkup, Eye Examination)
2. **💇 Salon & Spa Appointments** (Haircut, Hair Styling, Facial)
3. **🔧 Vehicle Service Appointments** (Synthetic Oil Change, General Maintenance, Tyre Rotation)

---

## 🛠️ Technology Stack

- **Backend**: Python 3 + Flask
- **Database**: SQLite (`bookings.db` initialized automatically)
- **Frontend**: Clean Humanized Light Theme (HTML5, Vanilla CSS, Vanilla JavaScript)
- **Automated Testing**: `pytest` (8 tests passing with isolated temp database)

---

## 🚀 Quick Start (Running in VS Code)

### 1. Open Terminal in VS Code
Open your project folder in VS Code (`Ctrl + ` `~` or `Terminal -> New Terminal`).

### 2. Install Dependencies
```powershell
pip install flask pytest
```
*(Or use `py -3 -m pip install flask pytest`)*

### 3. Run the Application
```powershell
python app.py
```
*(Or `py -3 app.py`)*

Then open your browser at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Automated Tests

Run the full pytest suite with isolated in-memory test databases:
```powershell
pytest tests/ -v
```
*(Or `py -3 -m pytest tests/ -v`)*

**Results**: All 8 tests pass covering home page loading, slot retrieval, valid booking, field validation, duplicate booking rejection, multi-service slot sharing, and SQLite persistence.

---

## ⏱️ 2-Minute Presentation Demo Script

1. **Home Page (30s)**:
   - Point out the clean, humanized BookMyShow-style layout with the top hero carousel, city selector, and search bar.
   - Show the 3 service category cards (Doctor, Salon, Vehicle Service) and poster cards with verified ratings (★ 4.9), durations, and transparent fees.
2. **Book an Appointment (45s)**:
   - Click **"Book Slot"** on any card (e.g., Doctor - General Consultation).
   - Demonstrate the **horizontal cinema-style date selector** (`WED 21 OCT`, `THU 22 OCT`, etc.).
   - Show showtimes categorized into **Morning, Afternoon, and Evening** sessions.
   - Click an available time slot (green border turns to active coral red with instant summary calculation).
   - Enter Customer Name (e.g. `Rahul Sharma`) and 10-digit Mobile Number (`9876543210`).
   - Click **"Confirm & Generate Ticket"**.
3. **M-Ticket Confirmation & ACID Enforcement (30s)**:
   - Show the authentic **Digital M-Ticket** with perforated edges, QR code, and booking reference ID.
   - Go back and try to book the exact same slot: show the friendly duplicate rejection error preventing double-bookings.
4. **My Bookings Wallet (15s)**:
   - Click **"My Bookings"** in the top bar, enter the mobile number, and show how booked passes are retrieved from SQLite.

---

## ⚠️ Honest Limitations

- **Authentication**: No customer account registration or login (by design for quick workshop demo).
- **Online Payments**: Pricing and convenience fees are illustrative; no payment gateway integration.
- **Predefined Slots**: Demonstrates a fixed 7-slot schedule per day rather than arbitrary minute-by-minute calendar booking.
- **SMS / Email Alerts**: No external notification APIs are used (fully self-contained local application).

