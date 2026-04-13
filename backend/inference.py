import base64
import numpy as np
import cv2
import keras
from tensorflow.keras.applications.resnet50 import preprocess_input

import os as _os
MODEL_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "model.keras")
NUM_FRAMES = 20
FRAME_SIZE = (224, 224)
CLASS_NAMES = ["Normal", "Anomaly"]

# Google Drive file ID — replace YOUR_FILE_ID_HERE after uploading model to Google Drive
GDRIVE_FILE_ID = "YOUR_FILE_ID_HERE"

_model = None


def _download_model_from_gdrive():
    """Download model from Google Drive if not present locally."""
    if _os.path.exists(MODEL_PATH):
        return
    print(f"Model not found at {MODEL_PATH}. Downloading from Google Drive...")
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("Model downloaded successfully.")
    except Exception as e:
        raise RuntimeError(
            f"Failed to download model from Google Drive: {e}\n"
            f"Please download manually and place at: {MODEL_PATH}"
        )


def load_model():
    global _model
    _download_model_from_gdrive()
    print(f"Loading model from {MODEL_PATH}...")
    _model = keras.saving.load_model(MODEL_PATH)
    # Warm up with a dummy prediction
    dummy = np.zeros((1, NUM_FRAMES, 224, 224, 3), dtype=np.float32)
    _model.predict(dummy, verbose=0)
    print("Model loaded and warmed up.")
    return _model


def get_model():
    if _model is None:
        load_model()
    return _model


def extract_frames_from_video(video_path):
    """Extract 20 evenly-spaced frames from a video file."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        raise ValueError("Could not read video or video is empty")

    if total_frames >= NUM_FRAMES:
        indices = np.linspace(0, total_frames - 1, NUM_FRAMES, dtype=int)
    else:
        indices = list(range(total_frames))

    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, FRAME_SIZE)
            frames.append(frame)
    cap.release()

    if len(frames) == 0:
        raise ValueError("No frames could be read from the video")

    # Pad by repeating last frame
    while len(frames) < NUM_FRAMES:
        frames.append(frames[-1])

    return frames[:NUM_FRAMES]


def decode_base64_frame(b64_string):
    """Decode a base64-encoded JPEG/PNG image to a 224x224 RGB numpy array."""
    if "," in b64_string:
        b64_string = b64_string.split(",", 1)[1]
    img_bytes = base64.b64decode(b64_string)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, FRAME_SIZE)
    return frame


def predict_frames(frames):
    """
    Predict anomaly from a list of frames.
    frames: list of numpy arrays, each (224, 224, 3) uint8 RGB
    Returns dict with label, confidence, normal_score, anomaly_score.
    """
    batch = np.array(frames, dtype=np.float32)  # (20, 224, 224, 3)
    batch = preprocess_input(batch)
    batch = np.expand_dims(batch, axis=0)  # (1, 20, 224, 224, 3)

    model = get_model()
    preds = model.predict(batch, verbose=0)  # (1, 2)

    normal_conf = float(preds[0][0])
    anomaly_conf = float(preds[0][1])
    label = CLASS_NAMES[int(np.argmax(preds[0]))]

    return {
        "label": label,
        "confidence": round(max(normal_conf, anomaly_conf), 4),
        "normal_score": round(normal_conf, 4),
        "anomaly_score": round(anomaly_conf, 4),
    }
