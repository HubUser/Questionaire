This project is a comprehensive full-stack application designed to present text questions to users and record their spoken answers as audio files.

## Components

### Backend
- Provides a REST API for serving questions, receiving audio recordings, and handling transcription data.
- Built with Python Flask.
- Dockerized for easy deployment.

### Frontend
- React-based user interface for displaying questions and recording answers.
- Allows playing back recorded audio and editing transcriptions.
- Includes configuration for backend API URL.

### Transcription Service
- Separate Flask service using NVIDIA NeMo ASR model for automatic speech recognition.
- Runs in its own container.

### Proxy
- Nginx configured to serve the frontend static files and proxy API requests to the backend.

## Setup and Installation

### Prerequisites
- Docker and Docker Compose or Podman Compose for container orchestration.

### Running the Application
- Use the provided `podman-compose.yml` to build and run the containers:

```bash
podman-compose up --build
```

- This will start the frontend, backend, transcription service, and nginx proxy.
- Access the frontend via `http://localhost:3050`.

## Development

- Backend code is in the `backend` directory.
- Frontend code is in the `frontend` directory.
- Transcription service code is in the `transcription_service` directory.

## Key Changes from Previous Version

- Removed the old Tkinter GUI application for audio recording (`audio_question_gui.py`).
- Moved to a modern React frontend with audio recording in the browser.
- Added backend Flask API with Docker support.
- Introduced a dedicated speech transcription microservice using NVIDIA NeMo ASR.
- Added Nginx Docker configuration for serving the frontend and proxying API calls.
- Updated the frontend to fetch questions and post audio to new API routes.

## Requirements

- Backend Python dependencies are listed in `backend/requirements.txt`.
- Transcription service dependencies in `transcription_service/requirements_core.txt` and `transcription_service/requirements.txt`.
- Frontend dependencies managed via `frontend/package.json`.

## Usage

- Frontend: Use the UI to navigate through questions, record audio responses, listen back, and edit transcriptions.
- Backend handles saving audio files and transcription data.
- Transcription service provides asynchronous speech-to-text.

## Notes

- The application is containerized for easy deployment and scalability.
- Backend exposes port 5000.
- Transcription service exposed on port 5001.
- Frontend served via Nginx on port 80 inside the container, mapped to 3050 on the host.

---

This updated application replaces the previous local Python Tkinter GUI with a scalable modern web architecture supporting audio question presentation and answer recording as audio files.
