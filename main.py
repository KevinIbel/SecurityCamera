import cv2
import winsound
import datetime
import sounddevice
from scipy.io.wavfile import write

filename = 'output{0}.mp4'.format(datetime.datetime.now().strftime(" %d-%m-%Y, %H-%M-%S"))
camera = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, -1, 20.0, (640,480))
fps = 44100
duration = 40
print("Recording..")
print(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
print(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
while camera.isOpened():
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY )
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255 , cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=30)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Makes the countours squares, if you'd like it to not be, just remove the # below.
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        #Sensitivity of catching specific movements, the higher the less likely to catch wind movements.
        #change this to what you prefer.
        if cv2.contourArea(c) < 3000:
            continue
        datet = str(datetime.datetime.now())

        font = cv2.FONT_HERSHEY_SIMPLEX
        text = 'Width: ' + str(camera.get(3)) + ' Height:' + str(camera.get(4))
        frame1 = cv2.putText(frame1, text, (10, 50), font, 1,
                            (0, 255, 255), 2, cv2.LINE_AA)
        frame1 = cv2.putText(frame1, datet, (10, 100), font, 1,
                            (0, 255, 255), 2, cv2.LINE_AA)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        recording = sounddevice.rec(int(duration * fps), samplerate=fps, channels=2)
        #Below change the destination you'd like the output to be saved to.
        write("pythonProject/securitycam/output.wav", fps, recording)

        out.write(frame1)

    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Sec Cam', frame1)