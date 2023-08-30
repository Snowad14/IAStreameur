import os, random, glob, sys
from flask import Flask, jsonify, send_from_directory, render_template

app = Flask(__name__)

QUEUE_DIR = 'static/queue'
WAITING_DIR = 'static/waiting'
DELETE_MODE = False

@app.route('/get_video')
def get_video():
    queue_videos = [f for f in glob.glob(f"{QUEUE_DIR}/*.mp4")]
    if queue_videos:
        txtContent = open(f"{queue_videos[0].replace('.mp4', '.txt')}", "r").read()
        return jsonify({'video_path': queue_videos[0], "text": txtContent})
    
    # Si aucune vidéo dans queue, retourner une vidéo aléatoire de waiting
    waiting_videos = [f for f in glob.glob(f"{WAITING_DIR}/*.mp4")]
    if waiting_videos:
        return jsonify({'video_path': random.choice(waiting_videos)})
    
    return jsonify({'error': 'No videos available'})

@app.route('/delete_video/<string:videoId>', methods=['DELETE'])
def delete_video(videoId):
    try:
        if DELETE_MODE:
            os.remove(f"{QUEUE_DIR}/{videoId}")
            os.remove(f"{QUEUE_DIR}/{videoId.replace('.mp4', '.txt')}")
        else:
            os.replace(f"{QUEUE_DIR}/{videoId}", f"static/old/{videoId}")
            os.replace(f"{QUEUE_DIR}/{videoId.replace('.mp4', '.txt')}", f"static/old/{videoId.replace('.mp4', '.txt')}")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/')
def home():
    return render_template('index.html')

# def runServer():
#     os.chdir('flaskServer')
#     app.run(debug=False)

if __name__ == '__main__':
   app.run(debug=True)