# Virtual-Drawing
Virtual Drawing with color detection using Python and OpenCV library.

For a full presentation of the working project watch the [video](https://www.youtube.com/watch?v=XUWEyNa0Bcw) in Youtube or click on the image-link below.

[![Virtual-drawing-using-Python-and-OpenCV](http://img.youtube.com/vi/XUWEyNa0Bcw/0.jpg)](https://www.youtube.com/watch?v=XUWEyNa0Bcw "Virtual Drawing using Python and OpenCV | Computer Vision")

## Main Idea
The main idea of this project is to allow user to draw anything "virtually" on screen with the help of a web camera.

### [1] Two project windows
The first window (_Frame_), which is also the main one, shows what the camera "sees" with the addition of shapes (rectangles) in order to define regions of interests from which basic functions are being performed. The second one (_Canvas_) with black background shows only user's drawing. 

### [2] Color settings and color detection
We must define the desired color which we want to be detected. For this project we define as desired color the following one :
```python
lower_color = np.array([35,46,106])
upper_color = np.array([86,168, 255])
```
In order the find the exact values for the above arrays use the trackbars method as in project *[Hand Detection and Finger Counting](https://github.com/kostasthanos/Hand-Detection-and-Finger-Counting)*.

### [3] Maximum contour and center
We find the maximum contour of the selected color. 
```python
# Transform to HSV
hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)

# Mask from lower and upper color range
mask = cv2.inRange(hsv, lower_color, upper_color)

# Find contours in mask
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Find maximum contour
max_cnt = max(cnts, key = cv2.contourArea)
```

Then we find the center of the max contour and check if center is inside any of our regions of interests.
```python
# Center of max contour
M = cv2.moments(max_cnt)
if M["m00"] != 0:
  cX = int(M["m10"]/M["m00"])
  cY = int(M["m01"]/M["m00"])
  cv2.circle(frame, (cX, cY), 4, green, 2)
  center = (cX, cY)
```

### [4] Drawing and save
In order to see our drawing we keep a list of points (x,y)-values from each center.
```python
pts = []
if "(cX, cY) is inside the desired frame regions then" :
  pts.append(center) # Append point to list
```
If we want to save the current drawing we can use **save_draw()** function from file *[save_drawing.py](https://github.com/kostasthanos/Virtual-Drawing-OpenCV/blob/main/save_drawing.py)*. This function saves all drawings from black *Canvas* window in a local file with name **drawings**.
```python
#Name of new drawing : "drawing(number)_day-month-year_hour:minutes.jpg"
new_drawing = 'drawing' + str(number_of_drawings+1) + '_' + date_time + '.jpg'

def save_draw(image):
  cv2.imwrite(dir_name + '/' + new_drawing, image)
```

More details about the code are being exlpained as comments inside the files *[virtual_drawing.py](https://github.com/kostasthanos/Virtual-Drawing-OpenCV/blob/main/virtual_drawing.py)* and *[save_drawing.py](https://github.com/kostasthanos/Virtual-Drawing-OpenCV/blob/main/save_drawing.py)*

For a full presentation of the working project watch the [video](https://www.youtube.com/watch?v=XUWEyNa0Bcw) in Youtube.

## Author
* **Konstantinos Thanos**
