import glob, pickle, cv2, os
from facedetector import face_detect

for mp4video in glob.glob("sample_data/videos/*.mp4"):
    full_frames = [cv2.imread(mp4video)]
    fps = 25
    video_stream = cv2.VideoCapture(mp4video)
    fps = video_stream.get(cv2.CAP_PROP_FPS)

    full_frames = []
    while True:
        still_reading, frame = video_stream.read()
        if not still_reading:
            video_stream.release()
            break
        
        y1, y2, x1, x2 = [0, -1, 0, -1]
        if x2 == -1: x2 = frame.shape[1]
        if y2 == -1: y2 = frame.shape[0]

        frame = frame[y1:y2, x1:x2]

        full_frames.append(frame)

    device = "cuda"; face_det_batch_size = 16; pads = [0, 10, 0, 0]; nosmooth = False
    results = face_detect(full_frames, device, face_det_batch_size, pads, nosmooth)
    newPklName = os.path.basename(mp4video).replace(".mp4", ".pkl")
    with open(f"sample_data/pickled/{newPklName}", "wb") as f:
        pickle.dump(results, f)
    print(f"Face detection done for {mp4video}")
    