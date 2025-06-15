import os, uuid, traceback, logging, requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

CONV_URL   = "http://localhost:5001/upload"
FEAT_URL   = "http://localhost:5003/features"
PRED_URL   = "http://localhost:5002/predict"
PROMPT_URL = "http://localhost:5004/prompt"

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    p3 = wav = None
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        # 1) Save raw .3gp
        f3  = request.files['audio']
        fid = uuid.uuid4().hex
        p3  = os.path.join(UPLOAD_FOLDER, f"{fid}.3gp")
        f3.save(p3)

        # 2) Convert to wav
        with open(p3, 'rb') as fp:
            r = requests.post(CONV_URL, files={
                'audio': (f"{fid}.3gp", fp, 'audio/3gp')
            })
        r.raise_for_status()
        wav = r.json()['converted_path']

        # 3) Extract features
        with open(wav, 'rb') as wf:
            fr = requests.post(FEAT_URL, files={
                'audio': ("audio.wav", wf, 'audio/wav')
            })
        fr.raise_for_status()
        features = fr.json()

        # 4) Prediction
        with open(wav, 'rb') as wf:
            pr = requests.post(PRED_URL, files={
                'audio': ("audio.wav", wf, 'audio/wav')
            })
        pr.raise_for_status()
        predictions = pr.json().get('predictions', [])

        # 5) Generate feedback
        pg = requests.post(PROMPT_URL, json={
            'features':    features,
            'predictions': predictions
        })
        pg.raise_for_status()
        feedback = pg.json().get('feedback', '')

        # 6) Return everything
        return jsonify({
            'features':    features,
            'predictions': predictions,
            'feedback':    feedback
        })

    except Exception:
        tb = traceback.format_exc()
        logging.error("Error in /analyze:\n%s", tb)
        return jsonify({'error': 'Internal Server Error', 'traceback': tb}), 500

    finally:
        for path in (p3, wav):
            if path and os.path.exists(path):
                os.remove(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
