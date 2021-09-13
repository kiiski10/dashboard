import cv2, numpy

class Camera:
    def __init__(self, camNr):
        self.frameCount = 0
        self.camNr = camNr
        self.video = cv2.VideoCapture(self.camNr)
        self.frame = None
        print("CAPTURE START")

    def update(self):
        successful, self.frame = self.video.read()
        # if successful:
        #     self.frameCount += 1
        #     print("GOT FRAME:", self.frameCount)

    def __del__(self):
        print("CAPTURE END")
        self.video.release()


    def frameAsJpeg(self, frame):
        successful, jpeg = cv2.imencode(".jpg", frame)
        return(jpeg.tobytes())

    def frame_gen(self):
        while self.video.isOpened():
            self.update()
            yield(
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + self.frameAsJpeg(self.frame) + b'\r\n\r\n'
            )
