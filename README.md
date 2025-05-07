# Edge Linking (Using Hough Transform)
<h2> Purpose </h2> Link gaps in edges after passing image through any edge detection algorithm (Sobel, Canny, Prewitt, etc). This will allow formation of clear and complete boundaries which will increase accuracy of functions requiring edges of an image as input. The linking process used in this project is highly customizable and allows user to freely test and obtain results exactly as they desire.<br>
<h2> Requirements and Installation </h2> VSCode or Python IDLE, Libraries : numpy, opencv-python, flask. To open run app.py and go to http://127.0.0.1:5000 <br>
<h2> Parameters and their functioning </h2>
  Note -> The equation used for forming lines is : Rho = x.cos Theta + y.sin Theta. where Rho is perpendicular distance between line and origin (0,0) and theta is angle between the perpendicular and x axis.<br>
<ol>
  <li> Divisions : Specifies how many evenly spaced values to take between 0 and π. Higher the value, more distinct the lines will be; improving linking output. </li>
  <li> Max Lines : Specifies how many lines will be drawn. Higher the value, higher the number of linked edges will be.</li>
  <li> Frequency Threshold : Gives a threshold for accumulator matrix frequencies. High value will cause only the highly prominent lines to prevail. </li>
  <li> Theta Threshold : Gives a threshold for angle between lines. All lines with angle less than "Theta Threshold" radians with respect to a line will be removed.  </li>
  <li> Rho Thresold : Gives a threshold for distance between lines. High value ensures that only the lines far from one another remain. </li>
  <li> Max Gap : Gives a threshold for gap (distance) between two edge points to be linked. Higher value causes far away edge points to be connected. </li>
</ol>
