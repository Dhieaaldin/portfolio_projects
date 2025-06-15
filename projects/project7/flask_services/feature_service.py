from flask import Flask, request, jsonify
import librosa, numpy as np, os, uuid

app = Flask(__name__)
TMP = 'tmp_features'
os.makedirs(TMP, exist_ok=True)

def analyze_audio(path):
    y, sr = librosa.load(path, sr=None)

    # Feature calculations
    rms = librosa.feature.rms(y=y)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=1.0)
    zcr = librosa.feature.zero_crossing_rate(y=y)[0]
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

    # Peak amplitude
    peaks = np.abs(y)
    max_peak_amplitude = float(np.max(peaks))

    # Loud segment detection
    threshold = 0.05  # Adjust based on desired sensitivity
    frame_duration_sec = librosa.frames_to_time(1, sr=sr)
    loud_frames = rms > threshold
    loud_durations = []
    count = 0
    for is_loud in loud_frames:
        if is_loud:
            count += 1
        elif count > 0:
            loud_durations.append(count * frame_duration_sec)
            count = 0
    if count > 0:
        loud_durations.append(count * frame_duration_sec)

    return {
        "mean_rms_db": float(np.mean(rms_db)),
        "max_peak_amplitude": max_peak_amplitude,
        "mean_spectral_centroid_hz": float(np.mean(spectral_centroids)),
        "mean_zcr": float(np.mean(zcr)),
        "max_loud_segment_duration_sec": float(max(loud_durations) if loud_durations else 0),
        "num_loud_segments": len(loud_durations)
    }

@app.route('/features', methods=['POST'])
def extract_features():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    f = request.files['audio']
    tmp = os.path.join(TMP, f"{uuid.uuid4().hex}.wav")
    f.save(tmp)
    feats = analyze_audio(tmp)
    os.remove(tmp)
    return jsonify(feats)

if __name__ == '__main__':
    app.run(port=5003, debug=True, threaded=True)
