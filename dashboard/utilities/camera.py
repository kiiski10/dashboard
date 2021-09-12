import cv2, numpy

class Camera:
    def __init__(self, camNr):
        self.video = cv2.VideoCapture(camNr)
        self.successful = True
        self.frame = None
        self.openCvPreviewWin = False

    def update(self):
        self.successful, self.frame = self.video.read()

    def frameAsJpeg(self, frame):
        successful, jpeg = cv2.imencode(".jpg", frame)
        return(jpeg.tobytes())

    def frame_gen(self):
        while True:
            self.update()
            yield(
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + self.frameAsJpeg(self.frame) + b'\r\n\r\n'
            )
        #self.video.release()
