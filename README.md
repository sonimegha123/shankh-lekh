# ShankhLekh: Audio Transcriber & Summarizer
ShankhLekh is a powerful offline tool that turns your audio recordings into written text — and then summarizes them for quick understanding.

Just upload an audio file (like a recording of a talk), and ShankhLekh will:
- Transcribe the entire audio into clean, readable text.
- Summarize the key points using a local AI model (Mistral via Ollama).
- Let you view and download both the transcript and summary in a clean web interface powered by Streamlit.

1. Clone the repository
git clone https://github.com/sonimegha123/shankhlekh.git
cd shankhlekh

3. Set up the virtual environment
python3 -m venv venv
source venv/bin/activate

5. Install dependencies
pip install -r requirements.txt

6. Install ffmpeg (for pydub and audio decoding)
Mac:
brew install ffmpeg
Ubuntu:
sudo apt install ffmpeg

5. Start the ollama server
ollama serve

6. Start the Streamlit app
streamlit run app.py


