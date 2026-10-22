# 🌸 FlowerCare AI

FlowerCare AI is a Streamlit application designed for flower plant disease diagnosis and natural/organic gardening remedies.

---

## 🚀 Getting Started

### 1. Set as Active Workspace
To work directly inside this project in your editor, open or set your active workspace to:
```
C:\Users\Satya Srinivas\.gemini\antigravity\scratch\flowercare-ai
```

### 2. Install Dependencies
Open your terminal or command prompt and install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Launch the Streamlit web server:
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 🌿 Key Features

1. **Camera & Gallery Image Input:** Take photos directly via your webcam/phone camera or upload images from your local gallery.
2. **Deterministic & Realistic Diagnosis:** Diagnoses diseases or flags healthy foliage across 9 flower varieties (Rose, Hibiscus, Marigold, Sunflower, Jasmine, Tulip, Chrysanthemum, Gerbera, Lotus).
3. **Organic Solutions & Care:** Step-by-step natural remedies and cultural hygiene practices without harsh synthetic chemicals.
4. **Searchable Disease Library:** Filter by flower type or search by keyword/symptoms.
5. **Scan History & Profile Dashboard:** Tracks previous scans and provides garden health statistics.
6. **No-Loop Retake Handling:** Safe session key resetting prevents upload/camera bounce-back loops.

---

## 🧠 Upgrading to Real AI / Machine Learning

To replace the mock prediction with a live AI model, update the `predict_disease(image_bytes)` function in `app.py`:

- **Option A (Google Gemini API):** Pass `image_bytes` to Gemini 2.0 Flash with a prompt requesting structured JSON diagnosis.
- **Option B (Trained CNN / MobileNetV2):** Load your `.h5` or `.onnx` model weights via `@st.cache_resource` and run tensor inference on preprocessed images.
