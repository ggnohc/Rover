## Project: Search and Sample Return
### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[example_rock1]: ./calibration_images/example_rock1.jpg
[example_rock2]: ./calibration_images/example_rock2.jpg
[my_rock]: ./calibration_images/my_rock.jpg
[example_rock1_thresh]: ./calibration_images/example_rock1_thresh.jpg
[example_rock2_thresh]: ./calibration_images/example_rock2_thresh.jpg
[my_rock_thresh]: ./calibration_images/my_rock_thresh.jpg


## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  


### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

* By consulting the following [tutorial](http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html), was able to determine the appropriate color range for yellow.  Tested on "example_rock1.jpg" (rock in open area), "example_rock2.jpg" (rock in shade) and my own recorded data, the thresh hold is showing positive result, i.e. able to detect the whole rock, and rock only.  I used the recommended method and change the color scheme from RGB to HSV.

**Rock sample 1**
![Rock sample 1][example_rock1]
![Rock sample 1 threshed][example_rock1_thresh]

**Rock sample 2**
![Rock sample 2][example_rock2]
![Rock sample 2 thresh][example_rock2_thresh]

**Recorded data rock**
![Recorded data rock][my_rock]
![Recorded data rock thresh][my_rock_thresh]

*  The obstacle detection is relatively simple, i.e. anything other than navigable is considered an obstacle.

#### 2. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

* Utilizing core routine defined in notebook, the picture read by rover went through perspective transform, from which navigable terrain, obstacle and rock is filtered through respective color thresh hold define.  Respective pixels is then converted to rover centric coordintates, and then mapped to world coordinates.

* The 3 color threshold is then overlay and mapped to a world map on RGB color scheme, with red, blue and green channel representing obstable, navigable terrain and rock sample respectively.


### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

* "perception_step()" is basically added by populating routine added earlier in Jupyter Notebook, except we need to make use of the mean direction of navigable terrain, but again this is already defined in the Notebook.

* "decision_step()" is already populated with some basic function, but lack handling exception case such as when the rover is stuck between rock or even one of the wheel is obstructed, it will just keep trying to move forward.  Also the default is to move at the mean angle whereby there are clearest path, although this allow the rock to be detected, the distance is too far away for the rover ("near_sample" variable will almost always set to "0") to allow it to pick up the rock.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  

* The basic function allows the rover to navigate automonously, but to meet the requirement of mapping the terrain of 40% with 60% fidelity more changes is needed
  * Since rock will be scattered randomly around the wall, a "left wall clinging" approach will be utilized by adding a bias variable to the rover steer angle, using "near_wall" variable in code below:
  
    `Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + near_wall, -15, 15)`

  * This works reasonably well, but at some point the rover will hit some nasty wall edge and this shakes the camera causing fidelity to deteriorate over time.  Below approach was used to keep fidelity relatively stable beyond 70%:
* Limit the range of the rover to not update if the view is beyond certain range, I choose 85 meter but this can be much less.
  
  ```python
    def limit_range(xpix, ypix, range = 85):
      dist = np.sqrt(xpix**2+ypix**2)
      return xpix[dist < range], ypix[dist < range]
  ```
  
* Do not update the rover worldmap when the roll and pitch angle is +/- 5 degree, which is basically when the camera is shaky
  
  ```python
      if ((roll < 0.5) or (roll > 355)) and ((pitch < 0.5) or (pitch > 355)):  #only under the map when roll/pitch < 0.5, i.e. when it is not shaky
        # Rover.worldmap[y_obs_world, x_obs_world, 0] += 1
        Rover.worldmap[y_rock_world, x_rock_world, 1] += 1 #Need this to indicate rock detection
        #since we limit the range, should be always trust what we see now.
        Rover.worldmap[y_obs_world, x_obs_world, 0] = 255
        Rover.worldmap[y_nav_world, x_nav_world, 2] = 255
 ``` 
 
* To allow the rover to come out from stuck condition, and new rover attribute called "Rover.snap" is added to record the state of the rover at particular time:
    ```python
    def snap_rover_state(Rover):
    #check for last state since Rover updated
    Rover.snap = (Rover.pos[0], Rover.pos[1], Rover.yaw, time.time())
    print("snap_rover_state -> Rover.snap: {}".format(Rover.snap))

    return Rover
    ```
    
* This attribute is then used to determine if the rover is moving, by checking on rover x,y coordinate and yaw angle changes within certain time period. It is determine to be in "stuck" mode if those parameters has not changed, and it will be instructed to move to the right (since I am using "left wall clinging" approach this will likely move it out from "stuck" mode).

* To help debug the code by determining the state of the rover, I added more text output in "supporting_function.py" so that the variable will be displayed on bottom right of the screen real time:
    ```python
    #GC add Rover state
      cv2.putText(map_add,"  Rover Mode: "+str(Rover.mode), (0, 100),
                 cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
      #GC add near_sample
      cv2.putText(map_add,"  Near Sample: "+str(Rover.near_sample), (0, 115),
                 cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
    ```

##### *Challenges and future improvement*

* Although this approach has help to meet the minimum requirement and beyond, more tweaking can be done to improve the time requirement, maybe by speeding it up when the path is clear, and also keeping another map of visited area so that it will only navigate an area once.
* The rover will only pick up rock occasionally when the rock is near and speed of the rover is slow at corners.  Need to add code to slow down the rover when it detect rock ahead.
