# Final Project at the Data Science Academy
## Self-Driving Car

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

### Objective
The basic goal was to use data collected from Udacity’s Self Driving Car Simulator to build a model that would predict the steering angles for the vehicle. This problem was well suited for Convolutional Neural Networks (CNNs) that take in the forward-facing images from the vehicle and output a steering angle. This is a very interesting problem because it is not possible to drive under all possible scenarios on the track, so the deep learning algorithm will have to learn general rules for driving. This challenge can be treated as regression problem. A model's success was measured using the root mean square error (MSA) of the predicted steering versus the actual human steering.

**During the process we applied the following steps:**
-	Use the simulator to collect data of good driving behavior
-	Build a convolution neural network in Keras that predicts steering angles from images
-	Train and validate the model with a training and validation set
-	Test that the model successfully drives around track one without leaving the road
-	Summarize the results with a written report

![Steps](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/fazi.png?raw=true)

### Datasets

We tried using three different datasets:
* A manually created dataset on track 1 driven only in one direction
* Another manually created dataset on track 1 where we drive close to the bounds and recover to teach the model how to avoid going out of bounds — in the real world this would be called reckless or drink driving
* A manually created dataset on track 1 driven in both directions to help our model generalise.

### Data Collection

First we downloaded the open source Udacity simulator from the following repo:

https://github.com/udacity/self-driving-car-sim

The data collected driving the car around in a simulator on a race track was images (mostly .jpg) from 3 cameras (left, center, right) and steering angles acquired by manually driving the car in the training mode for five rounds. These training images were all from Track 1. The images were of 320 Width by 160 Height. On the images generated by the left and right cameras we apply steering angle calibration offset. Namely, 🔴🔴we add positive offset to the right camera (+0.25) and negative offset to the left (-0.25)🔴🔴The main idea being the left camera has to move right to get to center, and right camera has to move left.

🔴🔴26037🔴🔴 images were generated which in the following phase were subject to data processing and augmentation in order to ensure that the dataset was sufficiently enriched. Eventually, we monitor the accuracy of the models by using MSE and regression adjusted thresholding technique.

![data_collection](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/data_collection.png?raw=true)

Namely, the frames captured by the three cameras are fed into the system together with the steering angle generated by the manual steering of the Udacity Car Simulator. Data consists of images and accompanying .csv file containing the paths of the center, left and right camera images and their corresponding steering angle.  

### Data Preprocessing and Augmentation

In this phase, we couple each frame with its corresponding steering angle and, as a result, we produce the feature and the label. 
The functions we use for data preprocessing are as follows:
- Crop ( top 50 pixels and bottom 20 pixels)

🔴- YUV color
- Normalization (image/255.0)

By utilizing the said functions, we remove the parts of the image that are unnecessary for the model, such as the sky. We normalize the image and add YUV color scheme. 
We must be very careful while using deep learning models, because they have a tendency to overfit the data. One way to avoid overfitting is to collect a lot of data. For our car example, this will require us to drive the car under different weather, lighting, traffic and road conditions. Other way to avoid overfitting is to use augmentation. Augmentation helps us extract as much information from data as possible. All the training was based on driving on track 1 in one direction alone. The model never saw track 2 in training, but with image augmentation (flipping, changing brightness, adding shadow and noise) and using data from all the cameras (left, right and center) the model was able to learn general rules of driving that helped translate this learning to a different track.

**Augmentation techniques**
1. Image flip 
   * First we flip all images and change the sign of the predicted angle to simulate driving in the opposite direction and ot double our dataset.
2. Change image brightness
   * We will generate images with different brightness to simulate day and night conditions.
3. Random shadow
   * The next augmentation we will add is shadow augmentation where random shadows are cast across the image.
4. Random noise
   * With the last we are adding random noise to the image by taking into consideration the unclean conditions by simulating dust or dirt particles and distortions while capturing the image.

![data_augmentation](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/augmentation.png?raw=true)
