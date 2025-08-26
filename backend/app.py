from flask import Flask, jsonify, request
from pathlib import Path
from transcription import transcribe_audio_via_service

app = Flask(__name__)

QUESTIONS_FILE = Path('./data/questions.json')
AUDIO_DIR = Path('./data/audio_answers')
TRANSCRIPTS_DIR = Path('./data/transcripts')

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        questions = QUESTIONS_FILE.read_text()
        return questions, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<question_id>', methods=['POST'])
def save_audio(question_id):
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file part in the request'}), 400
    audio = request.files['audio']
    if audio.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    save_path = AUDIO_DIR / f'{question_id}.wav'
    audio.save(str(save_path))
    return jsonify({'message': 'Audio saved successfully', 'filename': str(save_path.name)}), 200

@app.route('/transcribe/<question_id>', methods=['GET'])
def transcribe_answer(question_id):
    audio_file = AUDIO_DIR / f'{question_id}.wav'
    if not audio_file.is_file():
        return jsonify({'error': 'Audio file not found'}), 404
    try:
        transcription = transcribe_audio_via_service(str(audio_file))
        print(f"Transcription result: {transcription}")
        return jsonify({'transcription': transcription}), 200
    except Exception as e:
        print(f"Exception raised: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/transcript/<question_id>', methods=['POST'])
def save_transcription(question_id):
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': 'No transcription text provided'}), 400

    save_path = TRANSCRIPTS_DIR / f'{question_id}.txt'
    save_path.write_text(text)
    return jsonify({'message': 'Transcription saved successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
