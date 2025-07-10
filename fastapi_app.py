from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper
import os
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, VectorStoreIndex, Document
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.openai import OpenAIEmbedding
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = whisper.load_model("tiny")  # Load once when server starts

app = FastAPI()
llm = OpenAI(model="gpt-4", temperature=0.7)
# Configure global settings
Settings.llm = OpenAI(model="gpt-4", temperature=0.7)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
# Define comedy enhancement prompt template
comedy_prompt = PromptTemplate(
    "You are a screenplay assistant. Enhance the following text by adding subtle, relevant humor. "
    "Do not alter the story structure. Mark added content with [COMEDY_BLOCK]...[/COMEDY_BLOCK] tags.\n\n"
    "Screenplay:\n{transcript}"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:8501"] for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_audio(request: Request):
    audio_data = await request.body()

    file_path = "recorded_audio.webm"
    with open(file_path, "wb") as f:
        f.write(audio_data)

    # Use the preloaded model
    result = model.transcribe(file_path)
    transcript = result.get("text", "")

    return JSONResponse({"message": "OK", "transcript": transcript})

@app.post("/upload_enhanced")
async def upload_audio_enhanced(request: Request):
    try:
        audio_data = await request.body()
        if not audio_data:
            raise HTTPException(status_code=400, detail="No audio data received")
        
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"recorded_audio_{timestamp}.webm"

        # Save the uploaded audio file
        with open(file_path, "wb") as f:
            f.write(audio_data)
        
        logger.info(f"Audio file saved: {file_path}")

        # Transcribe the audio
        result = model.transcribe(file_path)
        transcript = result.get("text", "").strip()
        
        if not transcript:
            raise HTTPException(status_code=400, detail="No speech detected in audio")
        
        logger.info(f"Transcription completed: {len(transcript)} characters")

        # Create a Document object from the transcript
        document = Document(text=transcript)

        # Build a vector index from the document
        index = VectorStoreIndex.from_documents([document])

        # Create a query engine from the index
        query_engine = index.as_query_engine()

        # Enhanced prompt for better comedy generation
        prompt = (
            "You are a professional comedy writer and screenplay enhancer. "
            "Your task is to add subtle, contextually appropriate humor to the following text. "
            "Rules:\n"
            "1. Preserve the original meaning and narrative flow\n"
            "2. Add humor that fits the tone and context\n"
            "3. Use wit, wordplay, timing, and character-based humor\n"
            "4. Wrap ONLY the newly added comedic elements with [COMEDY_BLOCK]...[/COMEDY_BLOCK] tags\n"
            "5. Keep the original text intact outside of comedy blocks\n\n"
            f"Original text to enhance:\n{transcript}"
        )

        # Query the engine with the enhanced prompt
        response = query_engine.query(prompt)
        enhanced_text = str(response)

        # Count and analyze comedy blocks
        comedy_blocks = re.findall(r"\[COMEDY_BLOCK\](.*?)\[/COMEDY_BLOCK\]", enhanced_text, re.DOTALL)
        comedy_count = len(comedy_blocks)

        # Clean up the temporary file
        try:
            os.remove(file_path)
        except:
            pass

        logger.info(f"Comedy enhancement completed: {comedy_count} blocks added")

        return JSONResponse({
            "transcript": transcript,
            "enhanced": enhanced_text,
            "comedy_count": comedy_count,
            "word_count": len(transcript.split()),
            "enhancement_ratio": len(enhanced_text) / len(transcript) if transcript else 1
        })

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")