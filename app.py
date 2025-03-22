from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# In-memory data store
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

claims = []

# Ensure upload/download folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients")
def view_patients():
    return render_template("patients.html", patients=patients)

@app.route("/submit", methods=["GET", "POST"])
def submit_claim():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        amount = float(request.form["amount"])
        diagnosis = request.form["diagnosis"]
        claim = {
            "claim_id": f"CLM-{len(claims)+1:06}",
            "status": "Submitted",
            "amount": amount,
            "diagnosis": diagnosis,
            "patient_id": patient_id
        }
        claims.append(claim)
        return redirect(url_for("claim_status"))
    return render_template("submit.html", patients=patients)

@app.route("/status")
def claim_status():
    return render_template("status.html", claim=claims[-1] if claims else None)

@app.route("/upload", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["csv_file"]
        if file.filename.endswith(".csv"):
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)
            df = pd.read_csv(filepath)
            table_html = df.to_html(classes="data-table", index=False)
            return render_template("upload_result.html", table=table_html, filename=file.filename)
        else:
            return "❌ Invalid file type. Upload a CSV."
    return render_template("upload.html")

@app.route("/download/csv")
def download_csv():
    if not claims:
        return "⚠️ No claims submitted yet."
    df = pd.DataFrame(claims)
    filepath = os.path.join("downloads", "claim_report.csv")
    df.to_csv(filepath, index=False)
    return send_file(filepath, as_attachment=True)

@app.route("/download/pdf")
def download_pdf():
    if not claims:
        return "⚠️ No claims to print."
    claim = claims[-1]  # just show latest in PDF
    filepath = os.path.join("downloads", "claim_summary.pdf")
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, "Claim Summary Report")
    y = height - 100
    for key, value in claim.items():
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"{key.capitalize()}: {value}")
        y -= 20
    c.save()
    return send_file(filepath, as_attachment=True)

# Required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
