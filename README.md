# Final Project at the Data Science Academy
## Self-Driving Car
***Team members***
- Marija Karagonov
- Violeta Trajkova
- Marjan Angeleski

## Intro
What a challenge!! It took us handful of datasets, and different Neural Network models (with a lot of parameters tuning), different technique for preprocessing and augmentation of the data to get here - finally a self-driving car. During this process in our understanding it is a must to have a good machine for collecting good data from the simulator. Also because we did not own a computer with a GPU we had difficulties during the training of the model, such as taking too long to train the model or not been able to continue to training till the end because of the online GPU limit on the kernel that we used. This project can be challenging if you are new to the field of the Machine Learning (as we are), many of the steps during this project may be confusing, but we hope that this notebook will make it easy for someone with basic Python knowledge to implement.

### Files Submitted
Submission includes all required files and can be used to run the simulator in autonomous mode.

**The following resources can be found in this github repository:**

-	[Self_driving_car.ipynb](https://github.com/marija-kara/Self_driving_car/blob/main/Self_driving_car_project.ipynb) containing the script to create and train the model
-	[drive.py](https://github.com/marija-kara/Self_driving_car/blob/main/drive.py) for driving the car in autonomous mode
-	[model.h5](https://github.com/marija-kara/Self_driving_car/blob/main/model.h5) containing a trained convolution neural network
-	[README.md](https://github.com/marija-kara/Self_driving_car/blob/main/README.md) summarizing the results
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
The basic goal was to use data collected from Udacity???s Self Driving Car Simulator to build a model that would predict the steering angles for the vehicle. This problem was well suited for Convolutional Neural Networks (CNNs) that take in the forward-facing images from the vehicle and output a steering angle. ??s part of the model we trained and compared couple of Convolutional Neural Network (CNN) models with largely varying architectures. The results suggest that the choice of CNN architecture for this type of task is less important than the data and augmentation techniques used. Because it is not possible to drive under all possible scenarios on the track, so the deep learning algorithm will have to learn general rules for driving. This challenge can be treated as regression problem. A model's success was measured using the root mean square error (MSE) of the predicted steering versus the actual human steering.

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
    * Another manually created dataset on track 1 where we drive close to the bounds and recover to teach the model how to avoid going out of bounds ??? in the real world this           would be called reckless or drink driving
    * A manually created dataset on track 1 driven in both directions to help our model generalise.
    
![data](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/image%20(1).png)

### Data Collection

First we downloaded the open source Udacity simulator from the following repo:

https://github.com/udacity/self-driving-car-sim

The data collected driving the car around in a simulator on a race track was images (mostly .jpg) from 3 cameras (left, center, right) and steering angles acquired by manually driving the car in the training mode for five rounds. These training images were all from Track 1. The images were of 320 Width by 160 Height. On the images generated by the left and right cameras we apply steering angle calibration offset. Namely, we add positive offset to the left camera (+0.2) and negative offset to the right (-0.2). The main idea being the left camera has to move right to get to center, and right camera has to move left.

21609 images were generated which in the following phase were subject to data processing and augmentation in order to ensure that the dataset was sufficiently enriched. Eventually, we monitor the accuracy of the models by using MSE and regression adjusted thresholding technique.

![data_collection](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/data_collection.png?raw=true)

Namely, the frames captured by the three cameras are fed into the system together with the steering angle generated by the manual steering of the Udacity Car Simulator. Data consists of images and accompanying .csv file containing the paths of the center, left and right camera images and their corresponding steering angle.  

### Data Preprocessing and Augmentation

In this phase, we couple each frame with its corresponding steering angle and, as a result, we produce the feature and the label. 
The functions we use for data preprocessing are as follows:

   - Crop (top 50 pixels and bottom 20 pixels)
   - YUV color
   - Normalization (image/255.0)

By utilizing the said functions, we remove the parts of the image that are unnecessary for the model, such as the sky. We normalize the image and add YUV color scheme. 
We must be very careful while using deep learning models, because they have a tendency to overfit the data. One way to avoid overfitting is to collect a lot of data. For our car example, this will require us to drive the car under different weather, lighting, traffic and road conditions. Other way to avoid overfitting is to use augmentation. Augmentation helps us extract as much information from data as possible. All the training was based on driving on track 1 in one direction alone. The model never saw track 2 in training, but with image augmentation (flipping, changing brightness, adding shadow and noise) and using data from all the cameras (left, right and center) the model was able to learn general rules of driving that helped translate this learning to a different track.

**Augmentation techniques**
1. Change image brightness
   * We will generate images with different brightness to simulate day and night conditions.
2. Image flip 
   * First we flip all images and change the sign of the predicted angle to simulate driving in the opposite direction and ot double our dataset.
3. Random noise
   * With the last we are adding random noise to the image by taking into consideration the unclean conditions by simulating dust or dirt particles and distortions while capturing the image.
4. Random shadow
   * The next augmentation we will add is shadow augmentation where random shadows are cast across the image.

![data_augmentation](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/augmentation.png?raw=true)

### Image Generator

Since we are generating new and augmented images on the fly as we train the model, we create generator to produce new images at each batch. Also this will help for the purposes of ensuring efficiency of the memory used. The generator performs the data augmentation and preprocessing functions in batches. The accompanying histograms of steering angles  from different batches of those augmented images shows much more balance:

![target_batch_after_generator](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/target_batch_after_generator.png?raw=true)
![target_batch_after_generator_2](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/target_batch_after_generator_2.png?raw=true)
![target_batch_after_generator_3](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/target_batch_after_generator_3.png?raw=true)
![target_batch_after_generator_4](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/target_batch_after_generator_4.png?raw=true)

### Model
Firstly we tried many different models (based on AlexNet, VGG or ResNet) but we settled on modified architecture used in the NVIDIA paper as it gave us the best results. We used five Convolutional layers three with stride of 2x2, and the remaining two with stride of 1x1. We flatten the output of the convolutional layers to create a single long feature vector. Then three deeply connected neural network layers with dropout to prevent overfitting.

The model architecture can be seen below:
![model](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/model.png?raw=true)

### Model performance
#### Training loss and validation loss
The training loss indicates how well the model is fitting the training data, while the validation loss indicates how well the model fits new data.
The model is converging quite good in just 32 epochs. Feel free to play with the hyper-parameters for better results.

![image (2)](https://github.com/marija-kara/Self_driving_car/blob/main/pictures/image%20(2).png)

Video below shows the performance of algorithm on the track 1 on which the original data was collected. The car is able to drive around for hours.

[<img src="https://github.com/marija-kara/Self_driving_car/blob/main/pictures/Screenshot%202021-08-10%20012103.png" width="500" height="400"/>](https://youtu.be/EooSwKneu9o "Final project - mistakes")

The performance on the training track was a little off but we think that???s fine as it shows that the car was not merely memorizing the track. It recovered successfully from a few critical situations, even though none of those maneuvers had been performed during training.

[<img src="https://github.com/marija-kara/Self_driving_car/blob/main/pictures/Screenshot%202021-08-10%20010736.png" width="500" height="400"/>](http://www.youtube.com/watch?v=Gl6daRTwBYQ "Final project - Udacity Self Driving Car - full drive")

### Conclusion

Summarizing, this was a really interesting and at the same time challenging project to work on. The models that performed best on 1 track did poorly on Track_2, hence
we probably need to try additional image augmentation and preprocessing functions for better performance.
