# PashuDrishti - AI-Powered Livestock Identification 🐄🐃

PashuDrishti is an AI-powered platform built for the **Smart India Hackathon** that instantly identifies cattle and buffalo breeds from images with high precision. Built for speed, accuracy, and ease of use, it supports multiple Indian languages to make it accessible to farmers across the country.

## 🌟 Features
* **Dual-Stage AI Classification:** Uses a Species Router (Cattle vs. Buffalo) and specific Breed Classifiers to achieve high accuracy.
* **Multilingual UI:** Available in English, Hindi (हिंदी), Marathi (मराठी), Gujarati (ગુજરાતી), Tamil (தமிழ்), and Telugu (తెలుగు).
* **Minimalist Glassmorphism Design:** A beautiful, responsive Next.js frontend.
* **Scan History & Analytics:** View past predictions and model performance over time.

## 📊 Dataset & Models
To run this project yourself or contribute to the AI, you will need the dataset and pre-trained models.
* **Dataset (Kaggle):** [Link to your Kaggle Dataset here]
* **Pre-trained Models (Hugging Face / GDrive):** [Link to your Models here]

*(Note: Download the `.pth` model files and place them inside the `backend/app/models/weights/` directory before running the backend).*

## 🚀 How to Run Locally

### 1. Backend (FastAPI)
Navigate to the backend directory, install requirements, and start the API:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend (Next.js)
Open a new terminal, navigate to the frontend directory, and start the UI:
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:3000` in your browser!

## 🤝 Contributing
Contributions are welcome! If you want to add a new language, improve the UI, or train the model on a new livestock breed, please fork the repository and open a Pull Request.
