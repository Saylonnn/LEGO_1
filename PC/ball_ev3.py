#!/usr/bin/python
import cv2

#cap = cv2.VideoCapture("ball.avi")
cap = cv2.VideoCapture("rtsp://141.46.137.93:8554/mystream")
# ueye_streamer
# Rtsp port 8554
# 1024 x 768 15 fps
# Bitrate 5000000

#initialize green ball
green = cv2.imread('GreenBall.png')

#initialize red ball
red = cv2.imread('RedBall.png')

#initialize yellow ball
yellow = cv2.imread('YellowBall.png')

#initialize blue ball
blue = cv2.imread('BlueBall.png')

#initialize black ball
black = cv2.imread('BlackBall.png')


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
    green_bottom_right = (green_top_left[0] + 17 , green_top_left[1] + 17)
    green_top_left_final = (green_top_left[0] + 17, green_top_left[1] + 17)

#Koordinaten der Mitte des Balls
    print("Green Ball: ", green_top_left_final)

    cv2.rectangle(frame, green_top_left_final, green_bottom_right, 255, 2)


    #red ball tracking

    resRed = cv2.matchTemplate(frame, red, 5)
    red_min_val, red_max_val, red_min_loc, red_max_loc = cv2.minMaxLoc(resRed)

    red_top_left = red_max_loc
    red_bottom_right = (red_top_left[0] + 15, red_top_left[1] + 12)
    red_top_left_final = (red_top_left[0] + 15, red_top_left[1] + 12)

    # Koordinaten der Mitte des Balls
    print("Red Ball: ", red_top_left_final)

    #TODO: wenn Ball im Feld, dann hinfahren
    #TODO: wenn Ball außerhalb vom Feld, dann zum Tor fahren und schießen
    #TODO: dafür alle Ecken ausmessen und roten Ball außerhalb vom Feld legen

    if red_top_left_final[0] > 56 & red_top_left_final[0] < 908 & red_top_left_final[1] > 105 & red_top_left_final[1] < 638:
        print("red ball inside")
    else:
        print("red ball outside")

    cv2.rectangle(frame, red_top_left_final, red_bottom_right, 255, 2)


    # yellow ball tracking

    resYellow = cv2.matchTemplate(frame, yellow, 5)
    yellow_min_val, yellow_max_val, yellow_min_loc, yellow_max_loc = cv2.minMaxLoc(resYellow)

    yellow_top_left = yellow_max_loc
    yellow_bottom_right = (yellow_top_left[0] + 19, yellow_top_left[1] + 20)
    yellow_top_left_final = (yellow_top_left[0] + 19, yellow_top_left[1] + 20)

    # Koordinaten der Mitte des Balls
    print("Yellow Ball: ", yellow_top_left_final)

    cv2.rectangle(frame, yellow_top_left_final, yellow_bottom_right, 255, 2)

    # black ball tracking

    resBlack = cv2.matchTemplate(frame, black, 5)
    black_min_val, black_max_val, black_min_loc, black_max_loc = cv2.minMaxLoc(resBlack)

    black_top_left = black_max_loc
    black_bottom_right = (black_top_left[0] + 13, black_top_left[1] + 14)
    black_top_left_final = (black_top_left[0] + 13, black_top_left[1] + 14)

    # Koordinaten der Mitte des Balls
    print("Black Ball: ", black_top_left_final)

    cv2.rectangle(frame, black_top_left_final, black_bottom_right, 255, 2)

    # blue ball tracking

    resBlue = cv2.matchTemplate(frame, blue, 5)
    blue_min_val, blue_max_val, blue_min_loc, blue_max_loc = cv2.minMaxLoc(resBlue)

    blue_top_left = blue_max_loc
    blue_bottom_right = (blue_top_left[0] + 13, blue_top_left[1] + 15)
    blue_top_left_final = (blue_top_left[0] + 13, blue_top_left[1] + 15)

    # Koordinaten der Mitte des Balls
    print("Blue Ball: ", blue_top_left_final)

    cv2.rectangle(frame, blue_top_left_final, blue_bottom_right, 255, 2)
    cv2.rectangle(frame, (56, 105), (908, 638), 255,2)


    cv2.imshow("Video", frame)  # Anzeige des Videoframes

    if cv2.waitKey(1) == 27:
        break # Wait for Esc

cap.release()
cv2.destroyAllWindows() # Close all windows
