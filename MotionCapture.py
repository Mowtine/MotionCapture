
# coding: utf-8

import sys
import os
import cv2
import numpy as np
import imageio
import math
import pickle
# Set file for motion detection.
path_to_video = './monkey.mov'

# Set red location range
ch_range = 50

print("Capturing")
# Capture Video and set it to cap
cap = cv2.VideoCapture(path_to_video)
# Check whether video is captured correctly
if not cap.isOpened():
    print('{} not opened'.format(path_to_video))
    sys.exit(1)
# Fetch video variables
time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

# Create output file
out = cv2.VideoWriter('JointRecognition.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (int(frame_width), int(frame_height)))
predict = cv2.VideoWriter('CorrectionAlgorythem.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (int(frame_width), int(frame_height)))

# prepare variables for correction array
pCenter = [100,100]
pPos = []

# snap distance
snapD = 40
# maximum movement for prediction
maxD = 30

gameReady = []

# Prep initial frame
prev_frame = None


# Create matrix for hand positions L hand, R hand, L foot, R foot, body
dotPos = [[] for time in range(time_length)]
frame_count = 0


previousPos = [0,0],[0,0],[0,0],[0,0],[0,0]
# Move through each frame
while(1):
    reture_flag, frame = cap.read()  # reture_flag=False when the video ends
    if not reture_flag:
        print('Video Reach End')
        break

    frame2 = frame.copy()

    # peform position recognition
    # find red dots and group them into locations
    # Find center point of those locations
    # Find centerpoint of whole monkey
    # Predict positions of other sections
    # Make a probability on the 5 locations and predicted position
    # Match the locations with markers.
    # r = 2, g = 1, b = 0
    redGrouping = []
    for x in range(frame_width):
        for y in range(frame_height):
            if (frame[y][x][2] > 150 and frame[y][x][1] < 70) or (frame[y][x][2] > 230 and frame[y][x][1] < 110):

                # check if within range of existing saved group
                newGroup = True
                for group in redGrouping:

                    if math.sqrt((group[0][0]-x)**2+(group[0][1]-y)**2) < ch_range:
                        newGroup = False
                        group.append([x,y])
                        break
                if newGroup:
                    redGrouping.append([[x,y]])
    for i in range(len(redGrouping)):
        pointx = 0
        pointy = 0
        for point in redGrouping[i]:
            pointx += point[0]
            pointy += point[1]
        dotPos[frame_count].append([int(pointx/len(redGrouping[i])),int(pointy/len(redGrouping[i]))])
        cv2.circle(frame, (int(pointx/len(redGrouping[i])),int(pointy/len(redGrouping[i]))), ch_range//2, (0,0,255))
    print(str(frame_count) + " out of " + str(time_length))


    # prev_frame = np.uint8(prev_frame)
    frame = np.uint8(frame)
    #
    # Write video to file
    out.write(frame)

    # Find the corrected location

    # Remove excess lines
    if len(dotPos[frame_count]) < 2:
        break

    xmax = 0
    xmin = frame_width
    ymax = 0
    ymin = frame_height

    #Get the center of the monkey
    for point in dotPos[frame_count]:
        if point[0] > xmax:
            xmax = point[0]
        if point[0] < xmin:
            xmin = point[0]
        if point[1] > ymax:
            ymax = point[1]
        if point[1] > ymin:
            ymin = point[1]
    xcent = xmax - xmin
    ycent = ymax - ymin


    # Go through and find each position
    rl = [0,0]
    ll = [0,0]
    rh = [0,0]
    lh = [0,0]
    ct = [0,0]
    Pos = []

    # if 5 positions then all correct and find them
    if len(dotPos[frame_count]) == 5:
        # find bottom two:
        b2 = [[0,0],[0,0]]
        for point in dotPos[frame_count]:
            if b2[0][1] < point[1]:
                if b2[0][1] > b2[1][1]:
                    b2[1] = b2[0]
                b2[0] = point
            elif b2[1][1] < point[1]:
                b2[1] = point
        # find right and left leg
        if b2[0][0] > b2[1][0]:
            rl = b2[0]
            ll = b2[1]
        else:
            rl = b2[1]
            ll = b2[0]

        # find top 3
        t3 = []
        for point in dotPos[frame_count]:
            if point != b2[0] and point != b2[1]:
                t3.append(point)
        t3.sort(key=lambda x: x[0])
        lh = t3[0]
        ct = t3[1]
        rh = t3[2]
        Pos = [rl, ll, rh, lh, ct]

    # if not 5 positions, then predict and snap to close points
    else:

        # re-set center if it displaces too far
        if abs(pCenter[0] - xcent) > maxD:
            xcent = pCenter[0]
        if abs(pCenter[1] - ycent) > maxD:
            ycent = pCenter[1]

        predPos = []
        resPos = []
        for point in pPos:
            predPos = [point[0]-pCenter[0]+xcent,point[1]-pCenter[1]+ycent]
            notcircled = True
            for circle in dotPos[frame_count]:
                if math.sqrt((predPos[0]-circle[0])**2+(predPos[1]-circle[1])**2) < snapD:
                    Pos.append(circle)
                    notcircled = False
                    break
            if notcircled:
                Pos.append(predPos)




    # drawing coloured circles
    cv2.circle(frame2, (Pos[0][0],Pos[0][1]), ch_range//2, (255,0,50), 5)
    cv2.circle(frame2, (Pos[1][0],Pos[1][1]), ch_range//2, (255,0,200), 4)
    cv2.circle(frame2, (Pos[2][0],Pos[2][1]), ch_range//2, (50,255,0), 3)
    cv2.circle(frame2, (Pos[3][0],Pos[3][1]), ch_range//2, (150,255,0), 2)
    cv2.circle(frame2, (Pos[4][0],Pos[4][1]), ch_range//2, (0,0,255), 1)

    # record second Video
    predict.write(frame2)

    # Set previous
    pCenter = [xcent,ycent]
    pPos = Pos
    gameReady.append(Pos)

    if len(dotPos[frame_count]) != 5:
        name = "frame%d.jpg"%frame_count
        name2 = "frame%dCorrection.jpg"%frame_count
        cv2.imwrite(name, frame)
        cv2.imwrite(name2, frame2)

    frame_count += 1
    # prev_frame = frame
    # print(frame_count)
    #
    # Main Content - End

    #cv2.waitKey(30) - delay for 30 milliseconds and return a value to indicate whether this step is successful
    #0xff == ord('q') - out of scope of this course. Don't worry.
    if cv2.waitKey(30) & 0xff == ord('q'):
        break

# Save array

saving = np.array(gameReady)
np.save('SpaceBattles/positions', saving)
with open("SpaceBattles/positions.txt", "wb") as fp:
    pickle.dump(gameReady, fp, protocol=2)
# Securely release video and close windows
cap.release()
out.release()
predict.release()
cv2.destroyAllWindows()
