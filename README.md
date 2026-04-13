# 🎥 CCTV Anomaly Detection System

## 📌 Overview

This project is an AI-powered CCTV anomaly detection system designed to identify unusual or suspicious activities in video footage. It leverages deep learning techniques to analyze sequences of frames and classify them into normal and anomalous categories.

The system is built as an end-to-end pipeline, covering data preprocessing, model training, and deployment through a user-friendly application interface.

---

## 🚀 Features

* 🎯 Detects anomalous activities in CCTV footage
* 🧠 Deep learning-based sequence modeling
* 📹 Supports video input for real-time or offline analysis
* ⚡ Automatic model download and setup
* 🌐 Clean and simple application interface

---

## 🛠️ Tech Stack

* Python
* TensorFlow / Keras
* OpenCV
* NumPy
* Flask 
---

## 📂 Project Structure

```
project/
│
├── app.py                 # Main application
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
├── notebooks/
│   └── training.ipynb    # Model training notebook
```

---

## ⚙️ Setup Instructions

1. Clone the repository:

```
git clone https://github.com/mechazawa14/cctv_anomaly_detection.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
python app.py
```

⚠️ Note: The trained model will be automatically downloaded during the first run.

---

## 🧠 Model Details

The model is trained on a dataset containing various categories of normal and anomalous activities such as:

* Assault
* Robbery
* Road accidents
* Vandalism
* Shoplifting
* And more

It uses a deep learning architecture (CNN + LSTM or similar) to capture both spatial and temporal features from video frames.

---

## 📊 Results

* Achieved strong performance on validation data
* Metrics used: Accuracy, F1-score
* Demonstrates reliable anomaly detection in diverse scenarios

---

## 📓 Training Notebook

The complete model training and preprocessing pipeline is available in the `notebooks/` directory.

---

## 📥 Pretrained Model

Due to GitHub file size limitations, the trained model is hosted externally.

The application automatically downloads the model when executed.

🔗 Model Link:
https://drive.google.com/file/d/1pskixXAV91M687kDe_eBy5JR2XB5ZCH7/view?usp=drive_link
---

## 💡 Future Improvements

* Real-time CCTV stream integration
* Multi-class anomaly classification
* Improved dataset and model generalization
* UI/UX enhancements

---

## 👨‍💻 Author

* Md. Abdul Raheem Alam

---

## ⭐ Acknowledgements

* Open-source datasets and tools
* Deep learning frameworks and community support
