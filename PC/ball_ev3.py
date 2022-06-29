#!/usr/bin/python
import cv2
from pyueye import ueye
import threading
import socket
import numpy as np
import sys
import pickle


class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def run(self):
        print("connection established")
        while True:
            data = self.conn.recv(1024)
            print("incomming Message: ", data)
            if not data:
                break

    def send(self, corList):
        self.conn.sendall(corList)


class ThreadingServer():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 8485
        self.connections = []
        self.ip = socket.gethostbyname(socket.gethostname())

    def run(self):
        server_thread = threading.Thread(target=self.run_server)
        print("server thread started")
        cam_thread = threading.Thread(target=self.run_cam)
        server_thread.start()
        cam_thread.start()

    def run_server(self):
        print("run server thread")
        self.sock.bind((self.ip, self.port))
        print("socket online")
        while True:
            self.sock.listen()
            print("now listening")
            conn, addr = self.sock.accept()
            connThread = ConnectionThread(conn, addr)
            connThread.start()
            self.connections.append(connThread)
            print(len(self.connections))

    def run_cam(self):
        # Variables
        hCam = ueye.HIDS(0)  # 0: first available camera;  1-254: The camera with the specified camera ID
        sInfo = ueye.SENSORINFO()
        cInfo = ueye.CAMINFO()
        pcImageMemory = ueye.c_mem_p()
        MemID = ueye.int()
        rectAOI = ueye.IS_RECT()
        pitch = ueye.INT()
        nBitsPerPixel = ueye.INT(24)  # 24: bits per pixel for color mode; take 8 bits per pixel for monochrome
        channels = 3  # 3: channels for color mode(RGB); take 1 channel for monochrome
        m_nColorMode = ueye.INT()  # Y8/RGB16/RGB24/REG32
        bytes_per_pixel = int(nBitsPerPixel / 8)
        pParam = ueye.wchar_p()

        # cap = cv2.VideoCapture("ball.avi")
        # cap = cv2.VideoCapture("rtsp://141.46.137.93:8554/mystream")
        # ueye_streamer
        # Rtsp port 8554
        # 1024 x 768 15 fps
        # Bitrate 5000000

        # initialize green ball
        green_1 = cv2.imread('C:\\Users\\User\\PycharmProjects\\Bildverarbeitung\\EV3\\Ball and EV3\\EV3 Ball and EV3\\GreenBall.png', -1)

        # initialize red ball
        red = cv2.imread('RedBall.png', -1)

        # initialize yellow ball
        yellow = cv2.imread('YellowBall.png', -1)

        # initialize blue ball
        blue = cv2.imread('BlueBall.png', -1)

        # initialize black ball
        black = cv2.imread('BlackBall.png', -1)

        '''
        if (cap.isOpened()):
            print("Capturing ...")
        else:
            print("Error open video")
        while(cap.isOpened()):
            ret, frame = cap.read()  # Liefert Erfolgswert und Videoframe
            if not ret:
                print("Error retrieving video frame")
                break
        '''

        print("START")
        print()

        # Starts the driver and establishes the connection to the camera
        nRet = ueye.is_InitCamera(hCam, None)
        if nRet != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")

        # Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
        nRet = ueye.is_GetCameraInfo(hCam, cInfo)
        if nRet != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")

        # You can query additional information about the sensor type used in the camera
        nRet = ueye.is_GetSensorInfo(hCam, sInfo)
        if nRet != ueye.IS_SUCCESS:
            print("is_GetSensorInfo ERROR")

        nRet = ueye.is_ResetToDefault(hCam)
        if nRet != ueye.IS_SUCCESS:
            print("is_ResetToDefault ERROR")

        # Set display mode to DIB
        nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)

        # Set the right color mode
        if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_BAYER: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()

        elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            nBitsPerPixel = ueye.INT(32)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_CBYCRY: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()

        elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()

        else:
            # for monochrome camera models use Y8 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("else")

        # Can be used to set the size and position of an "area of interest"(AOI) within an image
        nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
        if nRet != ueye.IS_SUCCESS:
            print("is_AOI ERROR")

        width = rectAOI.s32Width

        height = rectAOI.s32Height

        # Prints out some information about the camera and the sensor
        print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
        print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
        print("Maximum image width:\t", width)
        print("Maximum image height:\t", height)
        print()

        # ---------------------------------------------------------------------------------------------------------------------------------------
        pParam.value = "1.ini"

        ueye.is_ParameterSet(hCam, ueye.IS_PARAMETERSET_CMD_LOAD_FILE, pParam, 0)

        # Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
        nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
            if nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                nRet = ueye.is_SetColorMode(hCam, m_nColorMode)

        # Activates the camera's live video mode (free run mode)
        nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
        if nRet != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
        if nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
        else:
            print("Press q to leave the programm")

        # Continuous image display
        while (nRet == ueye.IS_SUCCESS):

            # In order to display the image in an OpenCV window we need to...
            # ...extract the data of our image memory
            array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)

            # bytes_per_pixel = int(nBitsPerPixel / 8)

            # ...reshape it in an numpy array...
            frame = np.reshape(array, (height.value, width.value, bytes_per_pixel))

            # ...resize the image by a half
            # frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
            #cv2.imshow('frame', frame)
            # green ball tracking
            resGreen = cv2.matchTemplate(frame, green_1, 5)
            green_min_val, green_max_val, green_min_loc, green_max_loc = cv2.minMaxLoc(resGreen)

            green_top_left = green_max_loc
            green_bottom_right = (green_top_left[0] + 17, green_top_left[1] + 17)
            green_top_left_final = (green_top_left[0] + 17, green_top_left[1] + 17)

            # Koordinaten der Mitte des Balls
            print("Green Ball: ", green_top_left_final)

            cv2.rectangle(frame, green_top_left_final, green_bottom_right, 255, 2)

            # red ball tracking

            resRed = cv2.matchTemplate(frame, red, 5)
            red_min_val, red_max_val, red_min_loc, red_max_loc = cv2.minMaxLoc(resRed)

            red_top_left = red_max_loc
            red_bottom_right = (red_top_left[0] + 15, red_top_left[1] + 12)
            red_top_left_final = (red_top_left[0] + 15, red_top_left[1] + 12)

            # Koordinaten der Mitte des Balls
            print("Red Ball: ", red_top_left_final)

            # TODO: wenn Ball im Feld, dann hinfahren
            # TODO: wenn Ball außerhalb vom Feld, dann zum Tor fahren und schießen
            # TODO: dafür alle Ecken ausmessen und roten Ball außerhalb vom Feld legen

            if red_top_left_final[0] > 56 & red_top_left_final[0] < 908 & red_top_left_final[1] > 105 & \
                    red_top_left_final[1] < 638:
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
            cv2.rectangle(frame, (56, 105), (908, 638), 255, 2)

            #cords = [red_top_left_final[0], red_top_left_final[1], black_top_left_final[0], black_top_left_final[1], blue_top_left_final[0], blue_top_left_final[1], yellow_top_left_final[0], yellow_top_left_final[1],
            #       green_top_left_final[0], green_top_left_final[1], 57, 286, 57, 461, 947, 283, 947, 458, True]
            cords_1 = [str(red_top_left_final[0]),",", str(red_top_left_final[1]),",", str(black_top_left_final[0]),",", str(black_top_left_final[1]),",", str(blue_top_left_final[0]),",", str(blue_top_left_final[1]),",", str(yellow_top_left_final[0]),",", str(yellow_top_left_final[1]),",",
                               str(green_top_left_final[0]),",", str(green_top_left_final[1]), ",",str(57),",", str(286),",", str(57),",", str(461), ",",str(947), ",",str(283),",", str(947),",",str(458),",", str(True)]

            s = ''.join(cords_1)
            print(s)

            #data = pickle.dumps(cords)

           #cords = [red_top_left_final[0],",", red_top_left_final[1],",", black_top_left_final[0],",", black_top_left_final[1],",", blue_top_left_final[0],",", blue_top_left_final[1],",", yellow_top_left_final[0],",", yellow_top_left_final[1],",",
            #         green_top_left_final[0],",", green_top_left_final[1],",", 57,",", 286,",", 57,",", 461,",", 947,",", 283,",", 947,",", 458,",", True]


            '''cords = [red_top_left_final, black_top_left_final, blue_top_left_final, yellow_top_left_final,
                     green_top_left_final, [57, 286], [57, 461], [947, 283], [947, 458], True]'''
            for x in self.connections:
                try:
                    x.send(str.encode(s))
                except:
                    print("connection closed")
                    self.connections.remove(x)
            # cv2.imshow("Video", frame)  # Anzeige des Videoframes

        ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)
        ueye.is_ExitCamera(hCam)
        # cap.release()
        cv2.destroyAllWindows()  # Close all windows


ts = ThreadingServer()
ts.run()
