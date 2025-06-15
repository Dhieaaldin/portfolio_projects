import librosa
import numpy as np
import tensorflow as tf
import soundfile as sf

LABELS = [line.strip() for line in open("yamnet_label_list.txt")]

def load_yamnet_model():
    interpreter = tf.lite.Interpreter(model_path="yamnet.tflite")
    interpreter.allocate_tensors()
    return interpreter

def predict_over_full_audio(audio_path, interpreter, label_file="yamnet_label_list.txt"):
    # Load audio as mono with 16kHz sample rate
    waveform, sr = librosa.load(audio_path, sr=16000, mono=True)
    waveform = waveform.astype(np.float32)

    chunk_size = 15600  # 0.975s at 16kHz
    num_chunks = len(waveform) // chunk_size

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    with open(label_file) as f:
        labels = f.read().splitlines()

    predictions = []

    for i in range(num_chunks):
        chunk = waveform[i * chunk_size: (i + 1) * chunk_size]

        if len(chunk) < chunk_size:
            # Pad the last chunk
            chunk = np.pad(chunk, (0, chunk_size - len(chunk)), mode='constant')

        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], chunk)
        interpreter.invoke()

        scores = interpreter.get_tensor(output_details[0]['index'])[0]
        predicted_index = np.argmax(scores)
        confidence = float(scores[predicted_index])
        predicted_label = labels[predicted_index]

        predictions.append((i, predicted_label, confidence))

    return predictions