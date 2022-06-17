import cv2

#cap = cv2.VideoCapture("ball.avi")
cap = cv2.VideoCapture("rtsp://141.46.137.93:8554/mystream")
# ueye_streamer
# Rtsp port 8554
# 1024 x 768 15 fps
# Bitrate 5000000

#initialize green ball
green = cv2.imread('ball2.jpg')
wGreen = green.shape[0]
hGreen = green.shape[1]

cv2.imshow("TemplateGreen", green)

#initialize red ball
red = cv2.imread('ball1.jpg')
wRed = red.shape[0]
hRed = red.shape[1]

cv2.imshow("TemplateRed", red)

#initialize black ball
black = cv2.imread('black ball.png')
wBlack = black.shape[0]
hBlack = black.shape[1]

cv2.imshow("TemplateBlack", black)

if (cap.isOpened()):
    print("Capturing ...")
else:
    print("Error open video")
while(cap.isOpened()):
    ret, frame = cap.read()  # Liefert Erfolgswert und Videoframe
    if not ret:
        print("Error retrieving video frame")
        break
    #green ball tracking
    resGreen = cv2.matchTemplate(frame, green, 5)
    green_min_val, green_max_val, green_min_loc, green_max_loc = cv2.minMaxLoc(resGreen)

    green_top_left = green_max_loc
    green_bottom_right = (green_top_left[0] + 25 , green_top_left[1] + 25)
    green_top_left_final = (green_top_left[0] + 25, green_top_left[1] + 25)

#Koordinaten der Mitte des Balls
    print("Green Ball: ", green_top_left_final)

    cv2.rectangle(frame, green_top_left_final, green_bottom_right, 255, 2)


    #red ball tracking

    resRed = cv2.matchTemplate(frame, red, 5)
    red_min_val, red_max_val, red_min_loc, red_max_loc = cv2.minMaxLoc(resRed)

    red_top_left = red_max_loc
    red_bottom_right = (red_top_left[0] + 31, red_top_left[1] + 41)
    red_top_left_final = (red_top_left[0] + 31, red_top_left[1] + 41)

    # Koordinaten der Mitte des Balls
    print("Red Ball: ", red_top_left_final)

    cv2.rectangle(frame, red_top_left_final, red_bottom_right, 255, 2)


    # black ball tracking

    resBlack = cv2.matchTemplate(frame, black, 5)
    black_min_val, black_max_val, black_min_loc, black_max_loc = cv2.minMaxLoc(resBlack)

    black_top_left = black_max_loc
    black_bottom_right = (black_top_left[0] + 15, black_top_left[1] + 15)
    black_top_left_final = (black_top_left[0] + 15, black_top_left[1] + 15)

    # Koordinaten der Mitte des Balls
    print("Black Ball: ", black_top_left_final)

    cv2.rectangle(frame, black_top_left_final, black_bottom_right, 255, 2)

    cv2.imshow("Video", frame)  # Anzeige des Videoframes

    if cv2.waitKey(1) == 27:
        break # Wait for Esc



cap.release()
cv2.destroyAllWindows() # Close all windows
