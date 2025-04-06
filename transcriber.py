#!/usr/bin/env python

from faster_whisper import WhisperModel
from pydub import AudioSegment
import os
import concurrent.futures
import ollama  

EXTERNAL_DRIVE_PATH = "/Volumes/Elements/shankhLekh/"

def split_audio(input_path, chunk_length_ms=120000):
    audio = AudioSegment.from_file(input_path, format="m4a")
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_name = f"{os.path.basename(input_path)}_chunk_{i // chunk_length_ms}.wav"
        chunk_path = os.path.join(EXTERNAL_DRIVE_PATH, chunk_name)
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

def transcribe_chunk(chunk_path, model):
    segments, _ = model.transcribe(chunk_path)
    return " ".join(segment.text for segment in segments)

def summarize_transcript(transcript_path):
    with open(transcript_path, "r", encoding="utf-8") as file:
        transcript = file.read()

    if len(transcript) > 4000:
        transcript = transcript[:4000]

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "Summarize the following transcript in clear, concise language."},
            {"role": "user", "content": transcript}
        ]
    )
    return response["message"]["content"]

def transcribe_audio(audio_path):
    chunks = split_audio(audio_path)
    model = WhisperModel("small", device="auto")  
    transcript_path = os.path.join(EXTERNAL_DRIVE_PATH, "full_transcript.txt")

    with open(transcript_path, "a", encoding="utf-8") as file, \
         concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_chunk = {executor.submit(transcribe_chunk, chunk, model): chunk for chunk in chunks}

        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            try:
                transcript = future.result()
                file.write(transcript + "\n")
                file.flush()
                print(f"Chunk saved: {chunk}")
            except Exception as e:
                print(f"Error processing {chunk}: {e}")

    print(f"Full transcript saved at: {transcript_path}")

    print("\nGenerating summary...")
    summary = summarize_transcript(transcript_path)
    print("\n=== SUMMARY ===\n", summary)

if __name__ == "__main__":
    audio_file = input("Enter the path to your audio file: ")
    transcribe_audio(audio_file)
