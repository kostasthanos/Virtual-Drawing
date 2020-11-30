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

# Sample pallete of colors for drawing part
black = (0,0,0)
# 1st column
white = (255,255,255)   # White  - w/W
blue = (255,0,0)        # Blue   - b/B
green = (0,255,0)       # Green  - g/G
red = (0,0,255)         # Red    - r/R
yellow = (0,255,255)    # Yellow - y/Y
# 2nd column
khaki = (140, 230, 240) # Khaki     - k/K
olive = (0,128,128)     # Olive     - o/O
cyan = (255,255,0)      # Cyan      - c/C
naive = (128,0,0)       # Naive     - n/N
dgreen = (0, 100, 0)    # Darkgreen - d/D

# List of color dictionairies
colors = [{1:[white, 'w/W', 'white'], 2:[blue, 'b/B', 'blue'], 3:[yellow, 'y/Y', 'yellow'], 4:[green, 'g/G', 'green'], 5:[red, 'r/R', 'red']},
          {1:[khaki, 'k/K', 'khaki'], 2:[cyan, 'c/C', 'cyan'], 3:[olive, 'o/O', 'olive'], 4:[naive, 'n/N', 'naive'], 5:[dgreen, 'd/D', 'dark green']}]

# Function to color a specific roi with the corresponding color
# and add letter defining that color
def colorings(diction, width):
    sx, sy = width-55, 20
    for i in range(len(diction)):
        start_y = sy + i*60
        end_y = start_y + 50
        frame[start_y: end_y, sx: sx + 50] = diction[i+1][0]
        cv2.putText(frame, diction[i+1][1], (width-47, 50 + i*60), font, .5, black, 2)

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

    '''
    Visual settings
    -------------------
    '''
    # Set text font to HERSHEY_COMPLEX
    font = cv2.FONT_HERSHEY_COMPLEX
    
    cv2.putText(frame, "Color: ", (20,80), font, .6, black, 2)
    cv2.rectangle(frame, (90, 65), (110, 85), message_color, -1)
    cv2.putText(frame, message, (120, 80), font, .6, black, 2)

    # Colored areas in frame
    sx, sy = w-55, 20
    for i in range(len(colors)):
        colorings(colors[i], w - i*70)
        
    cv2.putText(frame, 'PRESS', (w-55, 15), font, 0.5, black, 2)
    cv2.putText(frame, 'Press s/S to save', (15, 450), font, 0.6, white, 1)
    
    # Erase lines in frame   ALL : Delete all,
    #                       [-1] : Delete all previous lines
    cv2.putText(frame, 'ALL', (w-45, h-30), font, 0.5, white, 2)
    cv2.putText(frame, '[-1]', (w-112, h-30), font, 0.5, white, 2)
    cv2.putText(frame, 'Delete:', (w-210, h-28), font, 0.7, white, 2)

    # Create (canvas) new black window with same dimensions as frame
    if canvas is None:
        canvas = np.zeros_like(frame)
    
    # Transform to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask from lower and upper color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply erosion and dilation
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)

    # Find contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        draw = True
        cv2.putText(frame, 'Drawing...', (20,40), font, 0.7, (0,0,0), 2)
        
        # Find maximum contour
        max_cnt = max(cnts, key = cv2.contourArea)
        if cv2.contourArea(max_cnt) > 800:
            # Center of max contour
            M = cv2.moments(max_cnt)
            if M["m00"] != 0:
                cX = int(M["m10"]/M["m00"])
                cY = int(M["m01"]/M["m00"])
                cv2.circle(frame, (cX, cY), 4, (0,255,0), 2)
                center = (cX, cY)
            if cX < w-70 or (cX > w-70 and cY > 310):
                # Append point to list
                pts.append(center)
            if cY > h-60 and cY < h-10:
                if cX > w-125 and cX < w-75:
                    canvas = np.zeros_like(frame)
                    pts = pts[:-1]
                elif cX > w-55 and cX < w-5:
                    canvas = np.zeros_like(frame)
                    pts = []
    else:
        cv2.putText(frame, 'No drawing', (20,40), font, .7, black, 2) 
        pts = []

    for i in range(1, len(pts)):
        # Draw line
        if len(pts)>2:
            cv2.line(canvas, pts[i-1], pts[i], color, 4)
        else:
            continue
        frame = cv2.add(frame,canvas)

    # Show frame and canvas side by side
    final_frame = np.hstack((frame, canvas))
    cv2.imshow('Final_Frame', final_frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

    # Change color when the corresponding letter-key (lower or upper) is pressed
    for j in range(len(colors)):
        for i in range(len(colors[j])):
            keyword = colors[j][i+1][1]
            if key == ord(keyword.split('/')[0]) or key == ord(keyword.split('/')[1]):
                color = colors[j][i+1][0]
                # Show selected color on frame
                message = colors[j][i+1][2]
                message_color = colors[j][i+1][0]
            elif key == ord('s') or key == ord('S'):
                save_draw(canvas) # Save canvas window as jpg image

cap.release()
cv2.destroyAllWindows()
