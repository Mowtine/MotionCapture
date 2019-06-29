
import numpy as np
import math
import pickle

finalarray = np.load('SpaceBattles/positions.npy')

finalarray = finalarray.tolist()

with open("SpaceBattles/positions.txt", "wb") as fp:
    pickle.dump(finalarray, fp, protocol=2)


# Move through the finalarray and ready the array for processing

# pCenter = [100,100]
# pPos = []
#
# # snap distance
# snapD = 30
#
# gameReady = []
#
# for i in range(len(finalarray)):
#
#     print(str(i) + " of " + str(len(finalarray)))
#     # Remove excess lines
#     if len(finalarray[i]) < 2:
#         break
#
#     xcent = 0
#     ycent = 0
#     #Get the center of the monkey
#     for point in finalarray[i]:
#         xcent += point[0]
#         ycent += point[1]
#     xcent = xcent//len(finalarray[i])
#     ycent = ycent//len(finalarray[i])
#
#     # Go through and find each hand
#     rl = [0,0]
#     ll = [0,0]
#     rh = [0,0]
#     lh = [0,0]
#     ct = [0,0]
#     Pos = []
#
#     # if 5 positions then all correct and find them
#     if len(finalarray[i]) == 5:
#         # find bottom two:
#         b2 = [[0,0],[0,0]]
#         for point in finalarray[i]:
#             if b2[0][1] < point[1]:
#                 if b2[0][1] > b2[1][1]:
#                     b2[1] = b2[0]
#                 b2[0] = point
#             elif b2[1][1] < point[1]:
#                 b2[1] = point
#         # find right and left leg
#         if b2[0][0] > b2[1][0]:
#             rl = b2[0]
#             ll = b2[1]
#         else:
#             rl = b2[1]
#             ll = b2[0]
#
#         # find top 3
#         t3 = []
#         for point in finalarray[i]:
#             if point != b2[0] or point != b2[1]:
#                 t3.append(point)
#         t3.sort(key=lambda x: x[0])
#         lh = t3[0]
#         ct = t3[1]
#         rh = t3[2]
#         Pos = [rl, ll, rh, lh, ct]
#
#     # if not 5 positions, then predict and snap to close points
#     else:
#         predPos = []
#         resPos = []
#         for point in pPos:
#             predPos = [point[0]-pCenter[0]+xcent,point[1]-pCenter[1]+ycent]
#             for circle in finalarray[i]:
#                 if math.sqrt((predPos[0]-circle[0])**2+(predPos[1]-circle[1])**2) < snapD:
#                     Pos.append(circle)
#                 else:
#                     Pos.append(predPos)
#
#
#
#
#
#
#
#     # Set previous
#     pCenter = [xcent,ycent]
#     pPos = Pos
#     gameReady.append(Pos)

# Save gameReady
# np.save("GamePositions",gameReady)
