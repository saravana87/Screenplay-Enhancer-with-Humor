# 🎬 Screenplay Enhancer with Humor

An AI-powered application that transcribes audio recordings and enhances them with contextually appropriate humor using OpenAI's GPT-4 and Whisper models.

## ✨ Features

- **Audio Recording**: Record audio directly in the browser
- **Speech-to-Text**: Transcribe audio using OpenAI Whisper
- **Comedy Enhancement**: Add humor using GPT-4 with multiple comedy styles
- **Real-time Processing**: Live feedback and processing status
- **Visual Highlighting**: Comedy blocks are highlighted in the output
- **Multiple Comedy Styles**: Choose from subtle, witty, slapstick, dry, or satirical humor

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Screenplay-Enhancer-with-Humor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Running the Application

1. Start the FastAPI backend:
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8502
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run streamlitjs.py
```

3. Open your browser and navigate to `http://localhost:8501`

## 🎯 Usage

1. Select your preferred comedy style from the dropdown
2. Click "Start Recording" and speak into your microphone
3. Click "Stop Recording" when finished
4. Wait for the AI to process your audio
5. Review the original transcript and enhanced version side-by-side

## 🛠️ Technical Architecture

- **Frontend**: Streamlit with embedded HTML/JavaScript
- **Backend**: FastAPI with async endpoints
- **AI Models**: 
  - OpenAI Whisper (speech-to-text)
  - OpenAI GPT-4 (text enhancement)
- **Vector Store**: LlamaIndex for document processing

## 🔧 Configuration

Edit `config.py` to customize:
- OpenAI model selection
- Whisper model size
- Audio file size limits
- Comedy style definitions

## 📝 API Endpoints

- `POST /upload_enhanced`: Upload audio and get enhanced transcript
- `POST /upload`: Simple transcription without enhancement

## 🎭 Comedy Styles

- **Subtle**: Understated, gentle humor
- **Witty**: Clever wordplay and smart observations
- **Slapstick**: Physical comedy and exaggerated situations
- **Dry**: Deadpan, matter-of-fact humor
- **Satirical**: Observational and satirical comedy

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Whisper models
- LlamaIndex for vector store capabilities
- Streamlit for the web framework
- FastAPI for the backend API

