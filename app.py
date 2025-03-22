from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Mock data
patients = [
    {
        "patient_id": "P001",
        "name": "Alice Carter",
        "dob": "1982-04-19",
        "insurance": "Blue Cross",
        "outstanding_claims": 2
    },
    {
        "patient_id": "P002",
        "name": "David Kim",
        "dob": "1975-08-03",
        "insurance": "UnitedHealth",
        "outstanding_claims": 0
    }
]

last_claim = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients")
def view_patients():
    return render_template("patients.html", patients=patients)

@app.route("/submit", methods=["GET", "POST"])
def submit_claim():
    global last_claim
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        amount = float(request.form["amount"])
        diagnosis = request.form["diagnosis"]
        last_claim = {
            "claim_id": "CLM-987654",
            "status": "Submitted",
            "amount": amount,
            "diagnosis": diagnosis,
            "patient_id": patient_id
        }
        return redirect(url_for("claim_status"))
    return render_template("submit.html", patients=patients)

@app.route("/status")
def claim_status():
    return render_template("status.html", claim=last_claim)
# Set up folders
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 📤 Upload CSV Route
@app.route("/upload", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["csv_file"]
        if file.filename.endswith(".csv"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            df = pd.read_csv(filepath)
            # Convert to HTML table
            table_html = df.to_html(classes="data-table", index=False)
            return render_template("upload_result.html", table=table_html, filename=file.filename)
        else:
            return "❌ Invalid file type. Please upload a CSV file."
    return render_template("upload.html")

# ⬇️ Download CSV Route
@app.route("/download/csv")
def download_csv():
    if not last_claim:
        return "⚠️ No claim has been submitted yet. Please submit one first."

    df = pd.DataFrame([last_claim])
    filepath = os.path.join(DOWNLOAD_FOLDER, "claim_report.csv")
    df.to_csv(filepath, index=False)

    try:
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return "❌ Could not find the file to download."

# ⬇️ Download PDF Route
@app.route("/download/pdf")
def download_pdf():
    filepath = os.path.join(DOWNLOAD_FOLDER, "claim_summary.pdf")
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, "Claim Summary Report")

    if last_claim:
        y = height - 100
        for key, value in last_claim.items():
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"{key.capitalize()}: {value}")
            y -= 20
    else:
        c.drawString(50, height - 100, "No claim submitted yet.")

    c.save()

    try:
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return "❌ PDF file not found."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)