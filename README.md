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

🔴-	model.py containing the script to create and train the model
-	[drive.py](https://github.com/marija-kara/Self_driving_car/blob/main/drive.py) for driving the car in autonomous mode

🔴-	model.h5 containing a trained convolution neural network
-	README.md summarizing the results
-	[requierments.txt](https://github.com/marija-kara/Self_driving_car/blob/main/requirements.txt) containing the needed environment
-	[utils.py](https://github.com/marija-kara/Self_driving_car/blob/main/utils.py) helper methods
-	[dataset_link.txt](https://github.com/marija-kara/Self_driving_car/blob/main/dataset_link.txt) google drive dataset link

### Requirements
| Library | Version |
|---|---|
| Opencv-python |	4.5.3.56 |
| Pillow |	8.3.1 |
| Sklearn |	0.24.1 |
| Keras |	2.4.3 |
| Python-socketio |	4.2.1 |
| Tensorflow |	2.5.0 |
| Eventlet |	0.31.1 |

### Data Collection

First we downloaded the open source Udacity simulator from the following repo:

https://github.com/udacity/self-driving-car-sim

Select Windows installation to download version 2 and follow the instruction in the repo.

The data collected from the Udacity’s Self Driving Car Simulator was images (mostly .jpg) from 3 cameras (left, center, right) and steering angles acquired by manually driving the car in the training mode for five rounds. On the images generated by the left and right cameras we apply steering angle calibration offset. Namely, 🔴🔴we add positive offset to the right camera (+0.25) and negative offset to the left (-0.25)🔴🔴

🔴🔴26037🔴🔴 images were generated which in the following phase were subject to data processing and augmentation in order to ensure that the dataset was sufficiently enriched. Eventually, we monitor the accuracy of the models by using MSE and regression adjusted thresholding technique.
![data_collection](https://drive.google.com/file/d/1Gs8qbosLs8GZ5ikUdL8DmNxkhhctrJpL/view?usp=sharing/data_collection.png)
