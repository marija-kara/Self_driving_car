# Final Project at the Data Science Academy
## Self-Driving Car

### Objective
The basic goal was to use data collected from Udacity’s Self Driving Car Simulator to build a model that would predict the steering angles for the vehicle. This problem was well suited for Convolutional Neural Networks (CNNs) that take in the forward-facing images from the vehicle and output a steering angle. This challenge can be treated as regression problem. A model's success was measured using the root mean square error (MSA) of the predicted steering versus the actual human steering.

**During the process we applied the following steps:**
-	Use the simulator to collect data of good driving behavior
-	Build a convolution neural network in Keras that predicts steering angles from images
-	Train and validate the model with a training and validation set
-	Test that the model successfully drives around track one without leaving the road
-	Summarize the results with a written report

### Files Submitted
Submission includes all required files and can be used to run the simulator in autonomous mode.

**Our project includes the following files:**
-	model.py containing the script to create and train the model
-	drive.py for driving the car in autonomous mode
-	model.h5 containing a trained convolution neural network
-	README.md summarizing the results
-	requierments.txt containing the needed environment
-	utils.py helper methods
-	dataset_link.txt google drive dataset link

### Requirements
| Library | Version |
|----|---|
| Opencv-python |	4.5.3.56 |
| Pillow |	8.3.1 |
| Sklearn |	0.24.1 |
| Keras |	2.4.3 |
| Python-socketio |	4.2.1 |
| Tensorflow |	2.5.0 |
| Eventlet |	0.31.1 |
