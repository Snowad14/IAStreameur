import os
from elevenlabs import generate, play

def gen_elevenlabs(text):
    audio = generate(
        text=text,
        voice="Callum",
        model="eleven_multilingual_v2",
        api_key=os.getenv("ELEVENLABS_KEY")
    )
    return audio

if __name__ == "__main__":
    from dotenv import load_dotenv; load_dotenv()
    play(gen_elevenlabs("Bonjour"))