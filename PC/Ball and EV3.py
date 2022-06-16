import cv2

template = cv2.imread('ball2.jpg')
w = template.shape[0]
h = template.shape[1]

cv2.imshow("Template", template)

img1 = cv2.imread('ev3karol.png',cv2.IMREAD_GRAYSCALE)          # queryImage
w_ev3 = img1.shape[0]

# Initiate SIFT detector
sift = cv2.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)

cap = cv2.VideoCapture("ball.avi")
#cap = cv2.VideoCapture("rtsp://141.46.137.93:8554/mystream")
# ueye_streamer
# Rtsp port 8554
# 1024 x 768 15 fps
# Bitrate 5000000

if (cap.isOpened()):
    print("Capturing ...")
else:
    print("Error open video")
while(cap.isOpened()):
    ret, frame = cap.read()  # Liefert Erfolgswert und Videoframe
    if not ret:
        print("Error retrieving video frame")
        break

    res = cv2.matchTemplate(frame, template, 5)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    top_left_final = (top_left[0]+w_ev3, top_left[1])
    bottom_right = (top_left_final[0] -20, top_left_final[1] + 25)
    top_left_final2 = (top_left[0] + w_ev3 - 20, top_left[1] + 25)


#Koordinaten der Mitte des Balls
    print("Ball: ", top_left_final2)


    kp2, des2 = sift.detectAndCompute(frame, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    good = []
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):

        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]
            good.append(m)
    dst_pt = [kp2[m.trainIdx].pt]
    dst_pt_final = dst_pt[0]
    dst_pt_final2 = dst_pt_final[0] + 100, dst_pt_final[1]
    dst_pt_int = round(dst_pt_final2[0]), round(dst_pt_final2[1])

    #Koordinaten des Roboters
    print("Roboter: ", dst_pt_int)
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv2.DrawMatchesFlags_DEFAULT)
    frame = cv2.drawMatchesKnn(img1, kp1, frame, kp2, matches, None, **draw_params)

    cv2.rectangle(frame, top_left_final2, bottom_right, 255, 2)

    cv2.imshow("Video", frame)  # Anzeige des Videoframes


    if cv2.waitKey(1) == 27:
        break # Wait for Esc

cap.release()
cv2.destroyAllWindows() # Close all windows
