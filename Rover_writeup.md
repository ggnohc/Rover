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

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

##### 1.1 By consulting the following [tutorial](http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html), was able to determine the appropriate color range for yellow.  Tested on "example_rock1.jpg" (rock in open area), "example_rock2.jpg" (rock in shade) and my own recorded data, the thresh hold is showing positive result, i.e. able to detect the whole rock, and rock only.  I used the recommended method and change the color scheme from RGB to HSV.

**Rock sample 1**
![Rock sample 1][example_rock1]
![Rock sample 1 threshed][example_rock1_thresh]

**Rock sample 2**
![Rock sample 2][example_rock2]
![Rock sample 2 thresh][example_rock2_thresh]

**Recorded data rock**
![Recorded data rock][my_rock]
![Recorded data rock thresh][my_rock_thresh]

##### 1.2  The obstacle detection is relatively simple, i.e. anything other than navigable is considered an obstacle.

#### 2. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
And another! 

##### 2.1 
Utilizing core routine defined in notebook, the picture read by rover went through perspective transform, from which navigable terrain, obstacle and rock is filtered through respective color thresh hold define.  Respective pixels is then converted to rover centric coordintates, and then mapped to world coordinates.

The 3 color threshold is then overlay and mapped to a world map on RGB color scheme, with red, blue and green channel representing obstable, navigable terrain and rock sample respectively.

![alt text][image2]
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  



![alt text][image3]


