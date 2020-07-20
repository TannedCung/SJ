import dlib
import cv2
import numpy as np
from detector import *
from Eyes_draw.eye_move import *
from Head_move.Pi_head import *

class Yuhuriha():
    def __init__(self):
        self.Tracker={}
        self.vs = cv2.VideoCapture(0)
        self.Conan=Detector()
        self.eyes = Move()
        self.head = Head_move()

    def remove_bad_tracker(self, frame):
        delete_id_list = []

        # Thru all the detected objects
        for ID in self.Tracker.keys():
            trackedPosition = self.Tracker[ID].get_position()
            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            # with tracking conf < 4, that shouldn't be an actual face
            if self.Tracker[ID].update(frame) < 4 or t_x<=0 or t_y<=0:
                delete_id_list.append(ID)

        # pop the bad face
        for ID in delete_id_list:
            self.Tracker.pop(ID, None)
            self.CurrentPos.pop(ID, None)

    def reset_tracker(self):
        self.Tracker={}
        self.CurrentPos={}

    def Wake_up(self):
        frame_counter = 0
        object_number = 0
        self.reset_tracker()

        while True:
            _, frame = self.vs.read()
            frame = cv2.resize(frame, (480, 320))
            frame = np.fliplr(frame)
            frame = np.array(frame)
            frame_counter += 1
            self.remove_bad_tracker(frame=frame)
            # detect every 20 frames
            if not frame_counter%30:
                object_locate = self.Conan.detect_v1(frame=frame)

                for (_x, _y, _w, _h) in object_locate:
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)

                    # cal center of the object
                    x_center = x + 0.5 * w
                    y_center = y + 0.5 * h  
                    matchObjectID = None 
                    for ID in self.Tracker.keys():
                        trackedPosition = self.Tracker[ID].get_position()
                        t_x = int(trackedPosition.left())
                        t_y = int(trackedPosition.top())
                        t_w = int(trackedPosition.width())
                        t_h = int(trackedPosition.height())

                        t_x_center = t_x + 0.5 * t_w
                        t_y_center = t_y + 0.5 * t_h
                        # if the center is out of the rects of existing objects, then it is no longer an existing object   
                        if (t_x <= x_center <= (t_x + t_w)) and (t_y <= y_center <= (t_y + t_h)) and (x <= t_x_center <= (x + w)) and (y <= t_y_center <= (y + h)):
                            matchObjectID = ID 
                        
                    if matchObjectID is None:
                        tracker = dlib.correlation_tracker()
                        tracker.start_track(frame, dlib.rectangle(x, y, x+w, y+h))

                        self.Tracker[object_number] = tracker
                        object_number+=1
            # tracking every frame
            point2lookAt = (0,0,0,0)
            for ID in self.Tracker.keys():
                trackedPosition = self.Tracker[ID].get_position()
                t_x = int(trackedPosition.left())
                t_y = int(trackedPosition.top())
                t_w = int(trackedPosition.width())
                t_h = int(trackedPosition.height())

                self.CurrentPos[ID] = (t_x, t_y, t_w, t_h)

                if t_w*t_h > point2lookAt[2]*point2lookAt[3]:
                    point2lookAt = self.CurrentPos[ID]

                self.Conan.mark_object(frame=frame, locate=self.CurrentPos[ID])
            
            if self.eyes.eyestrain():
                self.eyes.blink()
            # move eyes and head toward the object
            if point2lookAt != (0,0,0,0):
                self.eyes.stare_at(point2lookAt) 
                self.head.trace(point2lookAt)
            cv2.imshow("test+1", frame)
            if cv2.waitKey(5) == 27:
                break

a = Yuhuriha()
a.Wake_up()