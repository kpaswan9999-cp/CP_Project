# ⚡ StreamAI: Premium 5G Network Quality Predictor

StreamAI is a high-end, AI-driven diagnostic platform designed to predict 5G streaming quality using real-time network telemetry. Featuring a **Gold & Teal Glassmorphic UI** and a **Scientific Neural Network Background**, it provides users with professional diagnostic tickets and historical data management.

---

## 📋 Project Definition

### **Problem Statement**
5G network instability—driven by fluctuating Signal Strength (dBm), high Latency, and Jitter—often results in unpredictable buffering and playback failure for high-definition (4K/8K) streaming. Traditional network tools fail to provide real-time, AI-validated insights into exactly *how* these metrics impact the end-user experience.

### **Objective**
The primary goal of StreamAI is to develop a professional-grade, automated diagnostic system that:
1.  **Captures** complex 5G telemetry metrics accurately.
2.  **Analyzes** data patterns using a trained **RandomForest** AI model.
3.  **Delivers** scientific grading on a user-friendly 1–5 scale.
4.  **Generates** high-fidelity PDF reports for diagnostic logging and troubleshooting.

### **Final Conclusion**
StreamAI successfully bridges the gap between raw technical data and actionable user diagnostics. By shifting model outputs to an intuitive 1–5 range and providing a cinematic, interactive interface, the platform empowers users to manage and optimize their streaming connectivity with AI-backed confidence.

---

## 🎨 Premium Features

-   **Scientific Neural Background**: An interactive canvas-based neural network that reacts to mouse movement and pulses with a digital heartbeat.
-   **Professional PDF Tickets**: High-fidelity, dark-themed PDF reports containing detailed AI logs and telemetry history.
-   **1–5 Quality Scoring**: An intuitive, user-friendly rating system (mapped from raw AI 0–4 classification).
-   **Internal Processing Logs**: Real-time "Live Trace" transparency into the AI's inference steps.
-   **Advanced Animation System**: Cinematic staggered reveals and floating hero cards using high-performance CSS and JS curves.

---

## 📖 Platform Workflow (How it Works)

1.  **⚡ Network Telemetry**: Capture 6 essential 5G metrics (Signal Strength, Speed, Latency, Jitter, VoNR, and Drops).
2.  **🧠 AI Scanning**: The system processes inputs via a trained **RandomForest** machine learning model.
3.  **📊 Quality Output**: Generation of a precise 1–5 Quality Index with confidence ratio calculation.
4.  **🚀 User Dashboard**: Interactive visualization, history management, and PDF report delivery.

---

## 🛠️ Technology Stack

-   **Backend**: Python (Flask)
-   **AI/ML**: Scikit-Learn (RandomForest Model)
-   **Frontend**: Vanilla HTML5 / CSS3 / JavaScript (ES6+)
-   **Reporting**: FPDF2 (PDF Diagnostic Tickets)
-   **Data Visualization**: Chart.js (Confidence Gauges & Metric Hierarchy)

---

## 🚀 Quick Start Instructions

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install flask numpy scikit-learn fpdf2 python-pptx
```

### 2. Run the Application
Start the Flask server from the terminal:
```bash
python app.py
```

### 3. Access the Dashboard
Open your browser and navigate to:
**http://127.0.0.1:5000**

---

## 📂 Project Structure

- `app.py`: Core Flask application with ML inference & PDF generation logic.
- `prediction_history.json`: Local persistence for user history records.
- `model.pkl`: Pre-trained RandomForest model for 5G quality classification.
- `templates/index.html`: Main landing page with "How it Works" guide and input portal.
- `templates/result.html`: Post-prediction dashboard with technical logs and charts.

---

*Developed with a focus on Premium Performance and Scientific Accuracy.*
