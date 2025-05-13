from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import whisper
import tempfile
from fastapi.responses import JSONResponse
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, VectorStoreIndex, Document
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.openai import OpenAIEmbedding

import re

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
    audio_data = await request.body()
    file_path = "recorded_audio.webm"

    # Save the uploaded audio file
    with open(file_path, "wb") as f:
        f.write(audio_data)

    # Transcribe the audio using your transcription model
    result = model.transcribe(file_path)
    transcript = result.get("text", "")

    # Create a Document object from the transcript
    document = Document(text=transcript)

    # Build a vector index from the document
    index = VectorStoreIndex.from_documents([document])

    # Create a query engine from the index
    query_engine = index.as_query_engine()

    # Define the prompt to enhance the transcript with subtle humor
    prompt = (
        "Enhance this screenplay/story by adding subtle, relevant humor. "
        "Preserve the original meaning and flow. "
        "Wrap added parts with [COMEDY_BLOCK]...[/COMEDY_BLOCK] tags.\n\n"
        f"{transcript}"
    )

    # Query the engine with the prompt
    response = query_engine.query(prompt)
    enhanced_text = str(response)

    # Count the number of comedy blocks added
    comedy_blocks = re.findall(r"\[COMEDY_BLOCK\](.*?)\[/COMEDY_BLOCK\]", enhanced_text, re.DOTALL)
    comedy_count = len(comedy_blocks)

    # Return the original and enhanced transcripts along with the comedy count
    return JSONResponse({
        "transcript": transcript,
        "enhanced": enhanced_text,
        "comedy_count": comedy_count
    })