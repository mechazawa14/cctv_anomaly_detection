import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from inference import load_model, extract_frames_from_video, decode_base64_frame, predict_frames

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

# Load model at startup
load_model()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/predict/video", methods=["POST"])
def predict_video():
    """Accept a video file, extract 20 frames, predict."""
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files["video"]
    suffix = os.path.splitext(video_file.filename)[1] or ".mp4"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        video_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        frames = extract_frames_from_video(tmp_path)
        result = predict_frames(frames)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp_path)


@app.route("/api/predict/frames", methods=["POST"])
def predict_webcam_frames():
    """Accept JSON with base64-encoded frames from webcam."""
    data = request.get_json()
    if not data or "frames" not in data:
        return jsonify({"error": "No frames provided"}), 400

    b64_frames = data["frames"]
    if len(b64_frames) < 1:
        return jsonify({"error": "At least 1 frame required"}), 400

    try:
        frames = [decode_base64_frame(f) for f in b64_frames]

        # Pad to 20 if fewer
        while len(frames) < 20:
            frames.append(frames[-1])
        frames = frames[:20]

        result = predict_frames(frames)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
