import os
import random

import numpy as np
import cv2

haarcascade_classifiers_dir = "../local/py3_venv/lib/python3.8/site-packages/cv2/data/"

face_cascade = cv2.CascadeClassifier(haarcascade_classifiers_dir + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(haarcascade_classifiers_dir + "haarcascade_eye.xml")

images = {}

for img_file in os.listdir("media/GAN_detection_test_images"):

    if img_file == ".DS_Store":
        continue
    images[img_file] = cv2.imread("media/GAN_detection_test_images/" + img_file)

for name, img in images.items():

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        face_x = x
        face_y = y
        face_w = w
        face_h = h

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        # groups of two rectangles that are likely to be a pair of eyes
        eye_pairs = []
        over_laps = []

        for (ex, ey, ew, eh) in eyes:

            eye_rectangle = [ex, ey, ex + ew, ey + eh]

            horizontal_cousins_count = 0

            for (c_ex, c_ey, c_ew, c_eh) in eyes:

                test_rectangle = [c_ex, c_ey, c_ex + c_ew, c_ey + c_eh]
                if eye_rectangle == test_rectangle:
                    # same rectangle
                    continue

                # filter out rectangles that have overlaps. These probably aren't eyes
                if not (eye_rectangle[0] >= test_rectangle[2] or
                        eye_rectangle[2] <= test_rectangle[0] or
                        eye_rectangle[3] <= test_rectangle[1] or
                        eye_rectangle[1] >= test_rectangle[3]):
                    over_laps.append(eye_rectangle)
                    continue

                # filter out rectangles have no or more than one other rectangle on the horizontal plane
                if set(range(eye_rectangle[1], eye_rectangle[3])).intersection(set(range(test_rectangle[1], test_rectangle[3]))):
                    if horizontal_cousins_count > 0:
                        continue
                    sorted_pair = sorted([eye_rectangle, test_rectangle])
                    if sorted_pair not in eye_pairs:
                        eye_pairs.append(sorted_pair)
                    horizontal_cousins_count += 1

        # remove any pairs that have over lapping rectangles that of other "eyes"
        eye_pairs_no_overlap = list(filter(lambda pair: pair[0] not in over_laps and pair[1] not in over_laps, eye_pairs))

        vertical_mid_point = face_h / 2
        delta = -1
        most_likely_eye_pair = None
        for eye_pair in eye_pairs_no_overlap:
            mid = max(eye_pair[0][3] - ((eye_pair[0][3] - eye_pair[0][1]) / 2),
                      eye_pair[1][3] - ((eye_pair[1][3] - eye_pair[1][1]) / 2))
            if delta == -1 or abs(vertical_mid_point - mid) < delta:
                delta = abs(vertical_mid_point - mid)
                most_likely_eye_pair = eye_pair

            #k = min(map(eye_pairs_no_overlap))

        #color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        color = (0,255,0)
        cv2.rectangle(roi_color,
                      (most_likely_eye_pair[0][0], most_likely_eye_pair[0][1]),
                      (most_likely_eye_pair[0][2], most_likely_eye_pair[0][3]),
                      color,
                      2)
        cv2.rectangle(roi_color,
                      (most_likely_eye_pair[1][0], most_likely_eye_pair[1][1]),
                      (most_likely_eye_pair[1][2], most_likely_eye_pair[1][3]),
                      color,
                      2)

        #cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    cv2.imshow(name, img[face_y:face_y+face_h, face_x:face_x+face_w])

cv2.waitKey(0)
cv2.destroyAllWindows()
