import config from './config';
import './App.css';
import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [editedTranscription, setEditedTranscription] = useState('');

  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  useEffect(() => {
    async function fetchQuestions() {
      const response = await fetch('/api/questions');
      const data = await response.json();
      setQuestions(data.items);
    }
    fetchQuestions();
  }, []);

  useEffect(() => {
    if (!mediaRecorder) return;

    audioChunksRef.current = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' }); // Use webm for better compatibility
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    };
  }, [mediaRecorder]);

  const startRecording = () => {
    if (!recording) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          const mr = new MediaRecorder(stream);
          setMediaRecorder(mr);
          mr.start();
          setRecording(true);
        })
        .catch((err) => {
          alert('Microphone access denied or not available.');
        });
    }
  };

  const stopRecording = () => {
    if (recording && mediaRecorder) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const uploadAudio = async () => {
    if (!audioUrl) {
      alert('No audio recorded.');
      return;
    }
    const audioBlob = await fetch(audioUrl).then(r => r.blob());
    const formData = new FormData();
    formData.append('audio', audioBlob, `${questions[currentIndex].id}.wav`);

    const response = await fetch(`/api/audio/${questions[currentIndex].id}`, {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      alert('Audio uploaded successfully');
    } else {
      alert('Failed to upload audio');
    }
  };

  const fetchTranscription = async () => {
    const response = await fetch(`/api/transcribe/${questions[currentIndex].id}`);
    if (response.ok) {
      const data = await response.json();
      setTranscription(data.transcription);
      setEditedTranscription(data.transcription);
    } else {
      alert('Failed to get transcription');
    }
  };

  const saveTranscription = async () => {
    const response = await fetch(`/api/transcript/${questions[currentIndex].id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: editedTranscription })
    });
    if (response.ok) {
      alert('Transcription saved');
    } else {
      alert('Failed to save transcription');
    }
  };

  const nextQuestion = () => {
    setCurrentIndex((prev) => (prev + 1 < questions.length ? prev + 1 : prev));
    setAudioUrl(null);
    setTranscription('');
    setEditedTranscription('');
  };

  if (questions.length === 0) return <div>Loading questions...</div>;

  return (
    <div>
      <h2>Question {currentIndex + 1} of {questions.length}</h2>
      <p>{questions[currentIndex].question}</p>

      <div>
        <button onClick={startRecording} disabled={recording}>Start Recording</button>
        <button onClick={stopRecording} disabled={!recording}>Stop Recording</button>
        <button onClick={uploadAudio} disabled={!audioUrl}>Upload Audio</button>
      </div>

      {audioUrl && <audio ref={audioRef} controls src={audioUrl}></audio>}

      <div>
        <button onClick={fetchTranscription} disabled={!audioUrl}>Transcribe</button>
      </div>

      {transcription && (
        <div>
          <textarea
            value={editedTranscription}
            onChange={(e) => setEditedTranscription(e.target.value)}
            rows={5} cols={60}
          ></textarea>
          <button onClick={saveTranscription}>Save Transcription</button>
        </div>
      )}

      <div>
        <button onClick={nextQuestion}>Next Question</button>
      </div>
    </div>
  );
}

export default App;
