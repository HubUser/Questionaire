from flask import Flask, request, jsonify
from pydub import AudioSegment
import nemo.collections.asr as nemo_asr
import os
import tempfile

app = Flask(__name__)

# Load transcription model once
# Use nvidia/parakeet-tdt-0.6b-v3 for multilingual suport
asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name="nvidia/parakeet-tdt-0.6b-v2")
asr_model.change_attention_model(self_attention_model="rel_pos_local_attn", att_context_size=[256, 256])

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Expecting a file upload
    if 'file' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400
    file = request.files['file']

    # Save the file temporarily
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(file.read())
        temp_path = temp_file.name

        # Directly transcribe assuming file is already wav
        output = asr_model.transcribe([temp_path])

    transcription = output[0].text
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
