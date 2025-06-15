from flask import Flask, request, jsonify
from utils import load_yamnet_model, predict_over_full_audio
import os, uuid

app = Flask(__name__)
TMP = 'tmp_predict'
os.makedirs(TMP, exist_ok=True)

model = load_yamnet_model()

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    f = request.files['audio']
    tmp = os.path.join(TMP, f"{uuid.uuid4().hex}.wav")
    f.save(tmp)
    preds = predict_over_full_audio(tmp, model)
    os.remove(tmp)
    return jsonify({'predictions': preds})

if __name__ == '__main__':
    app.run(port=5002, debug=True, threaded=True)
