from os import listdir, path
import numpy as np
import scipy, cv2, os, sys, argparse, audio
import json, subprocess, random, string
from tqdm import tqdm
import torch, face_detection
from models import Wav2Lip
import platform, glob, pickle
from facedetector import face_detect
from logging import getLogger; logger = getLogger('AIStreamer')


class Wav2LipArgs:
	checkpoint_path = 'simpleWav2Lip/checkpoints/wav2lip.pth'
	face_dir = 'simpleWav2Lip/sample_data/videos'
	face = ''
	audio = 'simpleWav2Lip/sample_data/test.wav'
	outfile = 'simpleWav2Lip/results/result_voice.mp4'
	static = False
	fps = 25.
	pads = [0, 10, 0, 0]
	face_det_batch_size = 16
	wav2lip_batch_size = 128
	resize_factor = 1
	crop = [0, -1, 0, -1]
	box = [-1, -1, -1, -1]
	rotate = False
	nosmooth = False
	img_size = 96
	device = "cuda" if torch.cuda.is_available() else "cpu"

	def selectRandomVideo():
		videos = [f for f in glob.glob(f"{Wav2LipArgs.face_dir}/*.mp4")]
		Wav2LipArgs.face = random.choice(videos)

args = Wav2LipArgs()

if os.path.isfile(args.face) and args.face.split('.')[1] in ['jpg', 'png', 'jpeg']:
	args.static = True


def datagen(frames, mels):
	img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []

	newPklName = os.path.basename(Wav2LipArgs.face).replace(".mp4", ".pkl")
	pklPath = "simpleWav2Lip/sample_data/pickled/" + newPklName

	if os.path.isfile(pklPath):
		logger.info("Pickle file already exists, skipping face detection")
		with open(pklPath, "rb") as f:
			face_det_results = pickle.load(f)
	elif args.box[0] == -1:
		if not args.static:
			face_det_results = face_detect(frames, args.device, args.face_det_batch_size, args.pads, args.nosmooth) # BGR2RGB for CNN face detection
		else:
			face_det_results = face_detect([frames[0]], args.device, args.face_det_batch_size, args.pads, args.nosmooth)
	else:
		print('Using the specified bounding box instead of face detection...')
		y1, y2, x1, x2 = args.box
		face_det_results = [[f[y1: y2, x1:x2], (y1, y2, x1, x2)] for f in frames]

	for i, m in enumerate(mels):
		idx = 0 if args.static else i%len(frames)
		frame_to_save = frames[idx].copy()
		face, coords = face_det_results[idx].copy()

		face = cv2.resize(face, (args.img_size, args.img_size))
			
		img_batch.append(face)
		mel_batch.append(m)
		frame_batch.append(frame_to_save)
		coords_batch.append(coords)

		if len(img_batch) >= args.wav2lip_batch_size:
			img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)

			img_masked = img_batch.copy()
			img_masked[:, args.img_size//2:] = 0

			img_batch = np.concatenate((img_masked, img_batch), axis=3) / 255.
			mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], mel_batch.shape[2], 1])

			yield img_batch, mel_batch, frame_batch, coords_batch
			img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []

	if len(img_batch) > 0:
		img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)

		img_masked = img_batch.copy()
		img_masked[:, args.img_size//2:] = 0

		img_batch = np.concatenate((img_masked, img_batch), axis=3) / 255.
		mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], mel_batch.shape[2], 1])

		yield img_batch, mel_batch, frame_batch, coords_batch

mel_step_size = 16
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def _load(checkpoint_path):
	if device == 'cuda':
		checkpoint = torch.load(checkpoint_path)
	else:
		checkpoint = torch.load(checkpoint_path,
								map_location=lambda storage, loc: storage)
	return checkpoint

def load_model(path):
	model = Wav2Lip()
	checkpoint = _load(path)
	s = checkpoint["state_dict"]
	new_s = {}
	for k, v in s.items():
		new_s[k.replace('module.', '')] = v
	model.load_state_dict(new_s)

	model = model.to(device)
	return model.eval()

model = load_model(args.checkpoint_path)
logger.info(f"Model Wav2Lib loaded: {args.checkpoint_path} with {device}")

def main():
	Wav2LipArgs.selectRandomVideo()

	if not os.path.isfile(args.face):
		raise ValueError(f'Empty folder of mp4 files : {args.face_dir}')

	elif args.face.split('.')[1] in ['jpg', 'png', 'jpeg']:
		full_frames = [cv2.imread(args.face)]
		fps = args.fps

	else:
		video_stream = cv2.VideoCapture(args.face)
		fps = video_stream.get(cv2.CAP_PROP_FPS)

		logger.info("Reading video frames...")

		full_frames = []
		while 1:
			still_reading, frame = video_stream.read()
			if not still_reading:
				video_stream.release()
				break
			if args.resize_factor > 1:
				frame = cv2.resize(frame, (frame.shape[1]//args.resize_factor, frame.shape[0]//args.resize_factor))

			if args.rotate:
				frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

			y1, y2, x1, x2 = args.crop
			if x2 == -1: x2 = frame.shape[1]
			if y2 == -1: y2 = frame.shape[0]

			frame = frame[y1:y2, x1:x2]

			full_frames.append(frame)

	logger.info("Number of frames available for inference: "+str(len(full_frames)))

	if not args.audio.endswith('.wav'):
		print('Extracting raw audio...')
		command = 'ffmpeg -y -i {} -strict -2 {}'.format(args.audio, 'temp/temp.wav')

		subprocess.call(command, shell=True)
		args.audio = 'temp/temp.wav'

	wav = audio.load_wav(args.audio, 16000)
	mel = audio.melspectrogram(wav)
	# print(mel.shape)

	if np.isnan(mel.reshape(-1)).sum() > 0:
		raise ValueError('Mel contains nan! Using a TTS voice? Add a small epsilon noise to the wav file and try again')

	mel_chunks = []
	mel_idx_multiplier = 80./fps 
	i = 0
	while 1:
		start_idx = int(i * mel_idx_multiplier)
		if start_idx + mel_step_size > len(mel[0]):
			mel_chunks.append(mel[:, len(mel[0]) - mel_step_size:])
			break
		mel_chunks.append(mel[:, start_idx : start_idx + mel_step_size])
		i += 1

	logger.info("Length of mel chunks: {}".format(len(mel_chunks)))

	full_frames = full_frames[:len(mel_chunks)]

	batch_size = args.wav2lip_batch_size

	gen = datagen(full_frames.copy(), mel_chunks)

	for i, (img_batch, mel_batch, frames, coords) in enumerate(tqdm(gen, 
											total=int(np.ceil(float(len(mel_chunks))/batch_size)))):
		if i == 0:

			frame_h, frame_w = full_frames[0].shape[:-1]
			out = cv2.VideoWriter('simpleWav2Lip/temp/result.avi', 
									cv2.VideoWriter_fourcc(*'DIVX'), fps, (frame_w, frame_h))

		img_batch = torch.FloatTensor(np.transpose(img_batch, (0, 3, 1, 2))).to(device)
		mel_batch = torch.FloatTensor(np.transpose(mel_batch, (0, 3, 1, 2))).to(device)

		with torch.no_grad():
			pred = model(mel_batch, img_batch)

		pred = pred.cpu().numpy().transpose(0, 2, 3, 1) * 255.
		
		for p, f, c in zip(pred, frames, coords):
			y1, y2, x1, x2 = c
			p = cv2.resize(p.astype(np.uint8), (x2 - x1, y2 - y1))

			f[y1:y2, x1:x2] = p
			out.write(f)

	out.release()

	logger.info("Sucess, merging video and audio to mp4..")
	# command = 'ffmpeg -y -i {} -i {} -strict -2 -q:v 1 {}'.format(args.audio, 'simpleWav2Lip/temp/result.avi', args.outfile)
	# subprocess.call(command, shell=platform.system() != 'Windows')

	command = ['ffmpeg', '-y', '-i', args.audio, '-i', 'simpleWav2Lip/temp/result.avi', '-strict', '-2', '-q:v', '1', args.outfile]
	with open(os.devnull, 'w') as devnull:
		subprocess.call(command, stdout=devnull, stderr=subprocess.STDOUT, shell=platform.system() != 'Windows') 

	logger.info("Success! Saved output video "+ args.outfile)

if __name__ == '__main__':
	main()
