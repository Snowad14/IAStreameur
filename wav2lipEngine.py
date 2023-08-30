import sys, io, uuid, os
sys.path.append('simpleWav2Lip')
from simpleWav2Lip.inference import Wav2LipArgs, main

def performInference(videoId):
    main()
    os.rename("simpleWav2Lip/results/result_voice.mp4", "flaskServer/static/queue/" + videoId + ".mp4")

if __name__ == "__main__":
    performInference(open("rdm/test.wav", "rb").read())