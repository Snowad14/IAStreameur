import sys, io, uuid, os
sys.path.append('simpleWav2Lip')
from simpleWav2Lip.inference import Wav2LipArgs, main

def performInference(audio, videoId):
    # newAudioPath = f"simpleWav2Lip/sample_data/{str(uuid.uuid4())[:8]}.wav"
    audioPath = "simpleWav2Lip/sample_data/test.wav"
    open(audioPath, "wb").write(audio)
    main()
    os.rename("simpleWav2Lip/results/result_voice.mp4", "flaskServer/static/queue/" + videoId + ".mp4")

if __name__ == "__main__":
    performInference(open("rdm/test.wav", "rb").read())