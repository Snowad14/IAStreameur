import os, sys
from scipy.io import wavfile
from elevenlabs import generate, play
from voiceModels import rvcGenerator
from TTS.api import TTS
from utils import Config
import edge_tts, asyncio

audioPath = "simpleWav2Lip/sample_data/test.wav"

def gen_elevenlabs(text):
    audio = generate(
        text=text,
        voice=Config.get_value("elevenlabs_voice"),
        model="eleven_multilingual_v2",
        api_key=os.getenv("ELEVENLABS_KEY")
    )
    open(audioPath, "wb").write(audio)

def gen_RVC():
    modelName = Config.get_value("rvc_name")
    result, sr = rvcGenerator.applyRVC(
        model_path=f"voiceModels/rvcModels/{modelName}.pth",
        file_index=f"voiceModels/rvcModels/{modelName}.index",
        input_audio_path=audioPath,
    )
    wavfile.write(audioPath, sr, result)

def gen_VITS(text):
    api = TTS("tts_models/fra/fairseq/vits")
    api.tts_to_file(
        text,
        file_path=audioPath
    )

async def gen_Edge(text):
    voice = Config.get_value("edgetts_voice")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(audioPath)

if __name__ == "__main__":
    from dotenv import load_dotenv; load_dotenv()
    # gen_Edge("Bonjour snowad14, bonjour à tous les viewers présents sur Twitch. Je suis ravi d'être ici aujourd'hui pour répondre à vos questions et discuter avec vous. N'hésitez pas à me poser tout ce qui vous passe par la tête !")
    # play(gen_elevenlabs("Bonjour"))
    # gen_RVC("sample.wav")
    # gen_VITS("Bonjour je suis content d'etre ici a vous parlez, moi Emmanuel Macron")
    # gen_RVC()
    # gen_Edge("Bonjour tous le monde, je suis Emmanuel Macron")
    # gen_RVC()