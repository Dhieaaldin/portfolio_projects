from flask import Flask, request, jsonify
from pydub import AudioSegment
import os, uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_3gp_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="3gp")
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

@app.route('/upload', methods=['POST'])
def upload_and_convert():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    f = request.files['audio']
    file_id = uuid.uuid4().hex
    in_path  = os.path.join(UPLOAD_FOLDER, f"{file_id}.3gp")
    out_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.wav")

    f.save(in_path)
    convert_3gp_to_wav(in_path, out_path)
    return jsonify({'converted_path': out_path})

if __name__ == '__main__':
    app.run(port=5001, debug=True, threaded=True)
