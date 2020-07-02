from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from Pi_head import *

class Tracer():
	Cascade_path = "./data/haarcascade_frontalface_alt.xml"
	def __init__(self):
		# initialize the camera and grab a reference to the raw camera capture
		self.camera = PiCamera()
		self.camera.resolution = (480, 320)
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(self.camera, size=(480, 320))
		# allow the camera to warmup
		time.sleep(0.1)
		self.Pi_head = Head_move()
		self.face_cascade = cv2.CascadeClassifier(self.Cascade_path)
		# capture frames from the camera

	def cal_center(self, face):
		x, y, w, h = face
		return int((x+w)/2), int((y+h)/2)

	def Trace(self):
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			image = frame.array
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			face_poses = self.face_cascade.detectMultiScale(
													gray,
													scaleFactor=1.2,
													minNeighbors=5,
													minSize=(32, 32)
													)
			# Only trace the largest face
			face2trace = None
			if len(face_poses) > 1:  # Get the largest face as main face
				face2trace = max(face_poses, key=lambda rectangle: (rectangle[2] * rectangle[3]))  # area = w * h
			elif len(face_poses) == 1:
				face2trace = face_poses[0]

			cx, cy = self.cal_center(face2trace)
			self.Pi_head.face_trace(cx, cy)		
			cv2.imshow("Frame", image)
			key = cv2.waitKey(1) & 0xFF
			# clear the stream in preparation for the next frame
			rawCapture.truncate(0)
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

test = Tracer()
test.Trace()
