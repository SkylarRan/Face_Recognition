import datetime
import time
import os
from cv2 import cv2
import threading
import inspect
import ctypes
from model import face

face_recognition = face.Recognition()
output_dir = os.path.join(os.getcwd(), "static", "record")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
frame_interval = 5


class VideoThread(threading.Thread):
    def __init__(self, rtmp, alias, location):
        super(VideoThread, self).__init__()
        self.video = cv2.VideoCapture(rtmp)
        self.alias = alias
        self.location = location
        self.frameCount = 0

    def run(self):
        print("begin recognize")
        while True:
            self.recognize()
        print("end recognize")

    def recognize(self):
        _, frame = self.video.read()
        # frame = imutils.resize(frame, width=500)
        if self.frameCount % frame_interval == 0:
            faces = face_recognition.identify(frame)
            self.add_overlays(frame, faces)
        self.frameCount += 1
        
        # (flag, jpeg) = cv2.imencode(".jpg", frame)
        # return jpeg.tobytes()

    def save_recongition_result(self, frame, name):
            timestamp = datetime.datetime.now()
            time = timestamp.strftime("%Y%m%d%H%M%S")
            imgname = time + ".jpg"
            filename = os.path.join(output_dir, imgname)
            cv2.imwrite(filename, frame)

            record = {"camera": self.alias, "location": self.location, "recognizedAt":timestamp, "frame": "record/" + imgname, "name": name}
            print(str(record))

    def add_overlays(self, frame, faces):
        if faces is not None:
            for face in faces:
                face_bb = face.bounding_box.astype(int)
                cv2.rectangle(frame,
                              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                              (0, 255, 0), 2)
                # if face.name != "unknown":
                self.save_recongition_result(frame, face.name)
                cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    def __del__(self):
        self.video.release()


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(tid):
    _async_raise(tid, SystemExit)