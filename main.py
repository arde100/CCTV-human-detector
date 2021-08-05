import numpy as np
import cv2

detection_interval = 30
recording_length = 150

current_rects = None

current_frame = 0
recording_end_frame = -1

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor.getDefaultPeopleDetector())

recorder = None

cv2.startWindowThread()
cap = cv2.VideoCapture(0)

while True:

    # Reading the frame
    ret, frame = cap.read()
    if current_frame % detection_interval == 0:
        human_detected = False
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        current_rects = []
        for w, (xA, yA, xB, yB) in zip(weights, boxes):
            if w < 1.0:
                continue
            human_detected = True
            # display the detected boxes in the colour picture
            current_rects.append((xA, yA, xB, yB))

        if human_detected:
            recording_end_frame = current_frame + recording_length
    if recording_end_frame >= current_frame:
        if human_detected:
            for xA, yA, xB, yB in current_rects:
                cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)
        cv2.putText(frame, "rec", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color=(0,0,255))
        if not recorder:
            recorder = cv2.VideoWriter('output_%s.avi'%current_frame, cv2.VideoWriter_fourcc(*'MJPG'), 30., (640, 480))
        recorder.write(frame)
        if recording_end_frame == current_frame:
            recorder.release()
            recorder = None

    # displaying the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break
    current_frame += 1

if recorder:
    recorder.release()

cap.release()
cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
cv2.waitKey(1)
