import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import threading
import queue
import os
from pydub import AudioSegment

class QuestionGUI(tk.Tk):
    def __init__(self, questions, output_dir):
        super().__init__()
        self.questions = questions
        self.output_dir = output_dir
        self.current_question_index = 0

        self.title("Audio Response Recorder")
        self.geometry("500x300")

        self.question_label = tk.Label(self, text=self.questions[self.current_question_index], font=("Arial", 14), wraplength=480)
        self.question_label.pack(pady=20)

        self.record_button = tk.Button(self, text="Record Answer", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        self.next_button = tk.Button(self, text="Next Question", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Recording attributes
        self.is_recording = False
        self.fs = 44100  # Sample rate
        self.recorded_frames = []
        self.q = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def record_audio(self):
        with sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback):
            while self.is_recording:
                try:
                    data = self.q.get(timeout=0.1)
                    self.recorded_frames.append(data)
                except queue.Empty:
                    pass

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.config(text="Stop Recording")
            self.recorded_frames = []  # Clear previous recordings
            self.record_thread = threading.Thread(target=self.record_audio)
            self.record_thread.start()
        else:
            self.is_recording = False
            self.record_thread.join()
            self.save_recording()
            self.record_button.config(text="Record Answer")
            self.next_button.config(state=tk.NORMAL)

    def save_recording(self):
        audio_data = np.concatenate(self.recorded_frames, axis=0)
        temp_wav = os.path.join(self.output_dir, f"answer_{self.current_question_index}.wav")
        # Save as wav using soundfile
        import soundfile as sf
        sf.write(temp_wav, audio_data, self.fs)

        # Convert wav to mp3
        mp3_filename = os.path.join(self.output_dir, f"answer_{self.current_question_index}.mp3")
        sound = AudioSegment.from_wav(temp_wav)
        sound.export(mp3_filename, format="mp3")
        os.remove(temp_wav)  # Remove temporary wav file

        messagebox.showinfo("Saved", f"Answer saved as {mp3_filename}")

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.question_label.config(text=self.questions[self.current_question_index])
            self.next_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("End", "No more questions.")
            self.destroy()

    def on_close(self):
        if self.is_recording:
            if not messagebox.askokcancel("Quit", "Recording is in progress. Do you want to quit?"):
                return
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

