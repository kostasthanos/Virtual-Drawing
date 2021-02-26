#===========================#
#      Virtual Drawing      #
#        with OpenCV        #
#===========================#
#    Konstantinos Thanos    #
#    Mathematician, Msc     #
#===========================#

# Import packages
import numpy as np
import cv2
import imutils
from save_drawing import save_draw
                    
# Video Capture
cap = cv2.VideoCapture(1)

# Define lower and upper detection color (here I chose ~green)
lower_color = np.array([35,46,106])
upper_color = np.array([86,168, 255])

# Sample pallete of colors for the drawing part
black = (0,0,0)         # Black     - b/B
white = (255,255,255)   # White     - w/W
blue = (255,0,0)        # Blue      - b/B
green = (0,255,0)       # Green     - g/G
red = (0,0,255)         # Red       - r/R
yellow = (0,255,255)    # Yellow    - y/Y
khaki = (140, 230, 240) # Khaki     - k/K
olive = (0,128,128)     # Olive     - o/O
cyan = (255,255,0)      # Cyan      - c/C
dgreen = (0, 100, 0)    # Darkgreen - d/D
naive = (128,0,0)       # Naive     - n/N

# Dictionairy of colors
colors = {1:[white, 'w/W', 'white'], 2:[blue, 'b/B', 'blue'], 3:[yellow, 'y/Y', 'yellow'],
          4:[green, 'g/G', 'green'], 5:[red, 'r/R', 'red'], 6:[khaki, 'k/K', 'khaki'], 7:[cyan, 'c/C', 'cyan'],
          8:[olive, 'o/O', 'olive'], 9:[dgreen, 'd/D', 'dark green'], 10:[naive, 'n/N', 'naive']}


# Function to draw rectangles in a specific area (ROI) in frame
# and add text inside each rectangle, all with the corresponding color
def colorings(diction, window, text_color):
    width = 64
    sx, sy = 0, width
    for i in diction.keys():
        cv2.rectangle(window, (sx,0), (sx+width, sy), diction[i][0], 2) # Draw rectangle
        cv2.putText(window, diction[i][1], (sx+15, int(sy/2)+5), font, 0.5, text_color, 2) # Add the corresponding text
        sx += width

'''
Initializations
'''
color = white # Initial drawing color

pts = [] # List of points (drawing line)

canvas = None # New (black) window

cX, cY = "", ""

message = "white"
message_color = white

while True:
    _, frame = cap.read()
    # Flip frame horizontaly
    frame = cv2.flip(frame, 1)

    h, w = frame.shape[:2]
    width = 64

    '''
    Visual settings
    ----------------
    '''
    # Set text font to HERSHEY_COMPLEX
    font = cv2.FONT_HERSHEY_COMPLEX

    # Erase lines in frame   ALL : Delete all,
    #                       [-1] : Delete all previous lines
    cv2.putText(frame, 'ALL', (w-45, h-30), font, .5, white, 2)
    cv2.putText(frame, '[-1]', (w-112, h-30), font, .5, white, 2)
    cv2.putText(frame, 'Delete:', (w-210, h-28), font, .7, white, 2)

    cv2.putText(frame, 'SAVE', (20, h-38), font, .7, white, 2)
    cv2.putText(frame, 'or press s/S', (15, 470), font, 0.6, white, 1)
    cv2.rectangle(frame, (15,420), (85,450), white, 2)
    # cv2.putText(canvas, 'SAVE', (20, h-28), font, 0.7, white, 2)
    # cv2.rectangle(canvas, (15,430), (85,460), white, 2)
    
    cv2.putText(frame, "Color: ", (10,140), font, .6, black, 2)
    cv2.rectangle(frame, (80, 125), (100, 145), message_color, -1)
    cv2.putText(frame, message, (110, 140), font, .6, black, 2)

    # Colored rectangle areas in frame
    for i in colors.keys():
        colorings(colors, frame, black)
        # colorings(colors, canvas, white)

    # Create (canvas) new black window with same dimensions as frame
    if canvas is None:
        canvas = np.zeros_like(frame)
        
    
    # Transform to HSV
    hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)

    # Mask from lower and upper color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply erosion and dilation
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)

    # Find contours in mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        cv2.putText(frame, 'Drawing...', (10,100), font, .7, black, 2)
        
        # Find maximum contour
        max_cnt = max(cnts, key = cv2.contourArea)
        if cv2.contourArea(max_cnt) > 800:
            # Center of max contour
            M = cv2.moments(max_cnt)
            if M["m00"] != 0:
                cX = int(M["m10"]/M["m00"])
                cY = int(M["m01"]/M["m00"])
                cv2.circle(frame, (cX, cY), 4, green, 2)
                center = (cX, cY)
            if cY > h-60 and cY < h-10:
                if cX > w-125 and cX < w-75:
                    canvas = np.zeros((h-64,w,3))
                    pts = pts[:-1]
                elif cX > w-55 and cX < w-5:
                    canvas = np.zeros_like((h-64,w,3))
                    pts = []
            if cY > 64 and ((cX, cY) not in frame[430:460, 15:85]):
                pts.append(center) # Append point to list

            # Check if center point is inside our ROI rectangles and
            # change the line-color to the corresponding
            if cY > 0 and cY < 64:
                for i in range(len(colors)): 
                    if cX > i*64 and cX < (i+1)*64:
                        color = colors[i+1][0]
                        message_color = colors[i+1][0]
                        message = colors[i+1][2]
                    else:
                        continue

            if cY > 420 and cY < 450:
                if cX > 15 and cX < 85:
                    save_draw(canvas) # Save canvas window as jpg image
    else:
        cv2.putText(frame, 'No drawing', (10,100), font, .7, black, 2)
        pts = []

    for i in range(1, len(pts)):
        # Draw line in both frame and canvas windows
        if len(pts)>2:
            cv2.line(canvas, pts[i-1], pts[i], color, 4)
            cv2.line(frame, pts[i-1], pts[i], color, 4)
        else:
            continue

    # Show frame and canvas
    cv2.imshow('Frame', frame)
    cv2.imshow('Canvas', canvas)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

    # Optional
    # Change color when the corresponding letter-key (lower or upper) is pressed
    for i in colors.keys():
        keyword = colors[i][1]
        if key == ord(keyword.split('/')[0]) or key == ord(keyword.split('/')[1]):
            color = colors[i][0]
            # Show selected color on frame
            message = colors[i][2]
            message_color = colors[i][0]
        elif key==ord('S') or key==ord('s'):
            save_draw(canvas) # Save canvas window as jpg image

cap.release()
cv2.destroyAllWindows()
