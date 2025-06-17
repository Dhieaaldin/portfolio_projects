from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hard-coded API key (replace "sk-..." with your actual key)
<<<<<<< HEAD
API_KEY = "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"
=======
API_KEY = "(replace with your actual key)"
>>>>>>> 6fa665e9912ff7f1408c735d953ae3473bab1145

def build_prompt(features, predictions):
    return f"""Audio Sensory Analysis:

Features:
- Mean Loudness (RMS, dB): {features.get('mean_rms_db', 0):.2f}
- Max Peak Amplitude: {features.get('max_peak_amplitude', 0):.3f}
- Brightness (Spectral Centroid, Hz): {features.get('mean_spectral_centroid_hz', 0):.1f}
- Zero Crossing Rate: {features.get('mean_zcr', 0):.4f}
- Longest Loud Segment (sec): {features.get('max_loud_segment_duration_sec', 0):.2f}
- Number of Loud Segments: {features.get('num_loud_segments', 0)}

YAMNet Predictions:
{predictions}

Describe to a 18-years old the sensory feel of this sound in 1–2 short sentences.
Focus on how it might affect someone who is sensitive to sound (e.g., sharp, calm, harsh, soothing) don't use advanced scientific terms.
"""

@app.route('/prompt', methods=['POST'])
def generate_prompt():
    data = request.get_json()
    features    = data['features']
    predictions = data['predictions']

    prompt = build_prompt(features, predictions)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json"
    }
    payload = {
        "model":    "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {"role": "system", "content": "You are an assistant for autism-friendly environments."},
            {"role": "user",   "content": prompt}
        ]
    }

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    res.raise_for_status()
    answer = res.json()["choices"][0]["message"]["content"]
    return jsonify({"feedback": answer})

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(port=5004, debug=True, threaded=True)
=======
    app.run(port=5004, debug=True, threaded=True)
>>>>>>> 6fa665e9912ff7f1408c735d953ae3473bab1145
