from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import numpy as np
from flask_cors import CORS
import pickle
import json
import os
import uuid
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Load model
model = pickle.load(open("model.pkl", "rb")) # Reloaded with new model!

# History file path
HISTORY_FILE = "prediction_history.json"

# EXACT FEATURE NAMES FROM YOUR DATASET
feature_names = [
    'Signal Strength (dBm)',
    'Download Speed (Mbps)', 
    'Latency (ms)',
    'Jitter (ms)',
    'VoNR Enabled',
    'Dropped Connection'
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form values - EXACT order as dataset
        signal_strength = float(request.form["signal_strength"])
        download_speed = float(request.form["download_speed"])
        latency = float(request.form["latency"])
        jitter = float(request.form["jitter"])
        vonr_enabled = int(request.form["vonr_enabled"])
        dropped_connection = int(request.form["dropped_connection"])

        features = np.array([[
            signal_strength,
            download_speed,
            latency,
            jitter,
            vonr_enabled,
            dropped_connection
        ]])

        # App Log Tracking
        logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] Received telemetry: sig={signal_strength}, spd={download_speed}",
            f"[{datetime.now().strftime('%H:%M:%S')}] Features normalized to model input shape (1, 6)",
            f"[{datetime.now().strftime('%H:%M:%S')}] Executing RandomForest model inference..."
        ]

        # Prediction (Shifted to 1-5 scale)
        original_prediction = int(model.predict(features)[0])
        prediction = original_prediction + 1  # Map 0-4 -> 1-5
        probabilities = model.predict_proba(features)[0]
        confidence = float(round(max(probabilities) * 100, 2))
        importances = model.feature_importances_

        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Inference complete. Raw={original_prediction}, 1-5 Scaled={prediction}")

        # Save to history
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "features": {
                "signal_strength": signal_strength,
                "download_speed": download_speed,
                "latency": latency,
                "jitter": jitter,
                "vonr_enabled": "Enabled" if vonr_enabled == 1 else "Disabled",
                "dropped_connection": "Yes" if dropped_connection == 1 else "No"
            },
            "prediction": prediction,
            "confidence": confidence,
            "logs": logs
        }
        
        history = load_history()
        history.insert(0, record)  # Newest first
        save_history(history)

        # Return JSON for the frontend
        return jsonify({
            "id": record["id"],
            "prediction": prediction,
            "confidence": confidence,
            "features": features.tolist()[0],
            "feature_names": feature_names,
            "importances": importances.tolist(),
            "logs": logs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/history")
def history():
    return jsonify(load_history())

@app.route("/delete_prediction/<id>", methods=["POST"])
def delete_prediction(id):
    history = load_history()
    history = [r for r in history if r["id"] != id]
    save_history(history)
    return jsonify({"success": True})

class TicketPDF(FPDF):
    def header(self):
        self.set_fill_color(7, 8, 15)  # Dark theme
        self.rect(0, 0, 210, 297, "F")
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(240, 192, 64)  # Gold
        self.cell(0, 20, 'Stream AI Prediction Report', 0, 1, 'C')
        self.set_draw_color(0, 229, 204)  # Teal
        self.line(10, 25, 200, 25)
        self.ln(10)

@app.route("/api/view/<id>")
def view_prediction_api(id):
    history = load_history()
    record = next((r for r in history if r["id"] == id), None)
    if not record:
        return "Record not found", 404
        
    feat_dict = record["features"]
    features_list = [
        feat_dict["signal_strength"],
        feat_dict["download_speed"],
        feat_dict["latency"],
        feat_dict["jitter"],
        1 if feat_dict["vonr_enabled"] == "Enabled" else 0,
        1 if feat_dict["dropped_connection"] == "Yes" else 0
    ]
    
    try:
        importances = model.feature_importances_.tolist()
    except:
        importances = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]
        
    return jsonify({
        "prediction": record["prediction"],
        "confidence": record["confidence"],
        "features": features_list,
        "feature_names": feature_names,
        "importances": importances,
        "logs": record.get("logs", [])
    })

@app.route("/view/<id>")
def view_prediction_html(id):
    # This route is maintained for compatibility, but the frontend will likely use /api/view/<id>
    history = load_history()
    record = next((r for r in history if r["id"] == id), None)
    if not record:
        return "Record not found", 404
        
    feat_dict = record["features"]
    features_list = [
        feat_dict["signal_strength"],
        feat_dict["download_speed"],
        feat_dict["latency"],
        feat_dict["jitter"],
        1 if feat_dict["vonr_enabled"] == "Enabled" else 0,
        1 if feat_dict["dropped_connection"] == "Yes" else 0
    ]
    
    try:
        importances = model.feature_importances_.tolist()
    except:
        importances = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]
        
    return render_template(
        "result.html",
        prediction=record["prediction"],
        confidence=record["confidence"],
        features=features_list,
        feature_names=feature_names,
        importances=importances,
        logs=record.get("logs", [])
    )

@app.route("/download_report/<id>")
def download_report(id):
    history = load_history()
    record = next((r for r in history if r["id"] == id), None)
    
    if not record:
        return "Record not found", 404
        
    pdf = TicketPDF()
    pdf.add_page()
    pdf.set_text_color(240, 240, 240)
    
    # Header Info
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f"Ticket ID: {record['id']}", 0, 1)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 10, f"Timestamp: {record['timestamp']}", 0, 1)
    pdf.ln(5)
    
    # Input Data Section
    pdf.set_fill_color(30, 30, 35)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 229, 204)
    pdf.cell(0, 10, "  INPUTS", 1, 1, 'L', True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    for key, val in record['features'].items():
        pdf.cell(0, 8, f"     > {key.replace('_',' ').title()}: {val}", 0, 1)
    pdf.ln(5)
    
    # AI Result Section
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(240, 192, 64)
    pdf.cell(0, 10, "  AI PREDICTION OUTPUT", 1, 1, 'L', True)
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.ln(3)
    pdf.cell(0, 10, f"     QUALITY SCORE: {record['prediction']} / 5", 0, 1)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 8, f"     Confidence Level: {record['confidence']}%", 0, 1)
    pdf.ln(5)
    
    
    
    # Final Footer
    pdf.ln(20)
    pdf.set_font('helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "This is an AI-generated network diagnostic ticket. All predictions are based on statistical probability.", 0, 0, 'C')

    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"StreamAI_Ticket_{id[:8]}.pdf"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
