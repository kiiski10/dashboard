import cv2, time

class Camera:
    def __init__(self, camNr):
        self.validFrame = True
        self.camNr = camNr
        self.video = cv2.VideoCapture(self.camNr)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        print("Camera warming up..")
        time.sleep(1) # Give camera some time to start
        self.frame = None
        print("CAPTURE START")

    def update(self):
        successful, self.frame = self.video.read()
        if not successful:
            self.validFrame = False
            print("ERROR")

    def __del__(self):
        print("CAPTURE END")
        self.video.release()

    def frameAsJpeg(self, frame):
        successful, jpeg = cv2.imencode(".jpg", frame)
        return(jpeg.tobytes())

    def frame_gen(self):
        while True:
            self.update()
            if not self.validFrame:
                return
            yield(
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + self.frameAsJpeg(self.frame) + b'\r\n\r\n'
            )
