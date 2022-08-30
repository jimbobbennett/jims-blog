---
title: "Using TinyML to identify farts"
date: 2021-02-22T17:01:05Z
draft: false
featured_image: banner.png
images: 
  - blogs/tiny-ml-farts/banner.png
tags: ["ai", "iot", "tinyml" ,"vscode", "platformio"]
description: Jim built an AI model that runs on a microcontroller to identify different fart sounds. Be warned - this blog post is a stinker!
---

> TLDR; Find a complete hands-on lab to build a TinyML audio classifier at [github.com/microsoft/iot-curriculum/tree/main/labs/tiny-ml/audio-classifier](https://github.com/microsoft/iot-curriculum/tree/main/labs/tiny-ml/audio-classifier).

My 8-year-old daughter bought me "Farts - a spotters guide" - a book with some buttons down the side and when you press them, they make different fart sounds. This is the height of humor for an 8 year old, and still pretty funny as an adult. I thought it would be fun to see if I could distinguish between the different fart noises using machine learning - and not just any machine learning, but seeing as I love IoT, I wanted it to run on a microcontroller!

![Farts, a spotters guide](fart-book.jpg)

## TinyML

TinyML is a relatively new field, and is all about creating tiny machine learning models that can run on microcontrollers. These models are really tiny - in the order of kilobytes instead of the usual megabytes or gigabytes. They need to be this tiny to run on microcontrollers that typically have kilobytes of RAM. These models also draw little power, typically in the single-digit milliwatts or lower.

What are the use cases for TinyML? Well there are loads, anywhere you want to run ML models offline with minimal power draw. You may even have some TinyML models running in your house right now. For example, smart voice controlled devices listen for a wake word, and this needs to be offline and draw minimal power - perfect for a TinyML model. Another use case is in healthcare with devices that can monitor your health that run for years on tiny batteries. It's also being used in animal smart collars and trackers, [using audio to monitor the health of elephants in the wild](https://www.hackster.io/contests/ElephantEdge). So yes - a fart detector has a real world application!

To build a TinyML model you need to decide what type of model to build, gather training data, train the model, then deploy it to your device to handle new data. In this case, I wanted an audio classifier, so decided to use a [support vector machine classifier](https://scikit-learn.org/stable/modules/svm.html).

> Despite this sounding all fancy and like I know what I'm talking about, I actually have no clue what this is - I just learned about them from a great tutorial which I followed to get inspiration for this post! The tutorial is [Better word classification with Arduino Nano 33 BLE Sense and Machine Learning](https://eloquentarduino.github.io/2020/08/better-word-classification-with-arduino-33-ble-sense-and-machine-learning/).

## Building a fart detector

For my fart detector, I needed to build an audio classifier that could run on a microcontroller. Because I'm terrible at electronics and understanding I2C, SPI and all that other stuff, I decided to use an all-in-one Arduino board that has a microphone built in allowing me to use off-the-shelf Arduino libraries to gather audio data. The board of choice was the Arduino Nano 33 Sense BLE board, a small Arduino board with a whole raft of sensors including a microphone, temperature, pressure, humidity, light level and color, gesture and proximity. That's a lot of sensors in such a tiny board!

![An arduino Nano sense 33 BLE IoT board](nano-sense.jpg)

To code this board, I could use the free Arduino IDE, but I prefer to use [Visual Studio Code](https://code.visualstudio.com/), along with the [PlatformIO extension](https://platformio.org/). This allows the creation of standalone microcontroller projects with .ini files that define the board and libraries used. I can check a project into GitHub and someone can clone it and immediately start working with it without the need for instructions on what boards and libraries they need to set up.

### Getting training data

To train TinyML models you not only need the model to by tiny, but you also need small inputs - the more data that goes into training the model or inference (that is running the model), the larger it is. Audio data can be quite large - for example CD quality audio (remember CDs?) is 44.1KHz/16-bit which means it captures 2 bytes of data 44,100 times per second, or 176KB per second! That's a lot of data - if we wanted to use all of it and train our model with 2 seconds worth of data it wouldn't be TinyML any more.

A great trick with audio data is realizing you don't need all of it to classify particular sounds. Instead you can get an average value that represents many samples and use that as the data. In the case of the Arduino, the library that captures audio, [PDM](https://www.arduino.cc/en/Reference/PDM), captures audio at 16KHz in 512 byte buffers, containing 256 2-byte samples. This means each buffer has 1/64th of a second of audio data in it. We can then calculate a root mean square (RMS) of all this data to get a single 4-byte floating point value. If we do this for every buffer, we end up with 64 4-byte floats per second, or 256 bytes per second. Much smaller than raw audio at the PDM sample rate of 16KHz giving 32,000 bytes per second!

```cpp
#define BUFFER_SIZE 512U
...
// Check we have a full buffers worth
if (PDM.available() == BUFFER_SIZE)
{
  // Read from the buffer
  PDM.read(_buffer, BUFFER_SIZE);

  // Calculate the root mean square value of the buffer
  int16_t rms;
  arm_rms_q15((q15_t *)_buffer, BUFFER_SIZE/sizeof(int16_t), (q15_t *)&rms);
  ...
}
```

The RMS value can be checked against a threshold to see if there is actual audio data or not, and if audio data is detected, the next 2 seconds worth can be grabbed. In this case it's output to the serial port so it can be read from the PlatformIO serial monitor in VS Code.

You can find the full code to capture audio samples in the [Microsoft IoT Curriculum resource GitHub repo in the labs folder](https://github.com/microsoft/iot-curriculum/tree/main/labs/tiny-ml/audio-classifier/code/audio-capture).

### Train the model

To train the model, we need a good range of audio data captured from the Arduino device - ideally 15-30 samples per audio we want to classify. A classifier distinguishes the input between multiple labels, so we need to gather data for multiple labels. For example, to classify the farts from my fart book I'd need to gather 15-30 samples for at least 2 different farts.

The audio data sent to the serial monitor from the Arduino can be captured into .csv files, and these can be loaded by a Python script and used to train a model.

The model in question is trained using [Scikit-Learn](https://scikit-learn.org/), a Python Machine Learning library. The audio data is loaded into numpy arrays, then split into training and testing data, the model is trained using the training data, then tested with the testing data to give an idea on the accuracy.

> If you have a nice shiny Apple M1 mac (like I do), then installing Scikit-Learn is currently not as easy. Check out my [guide on how to install it](/blogs/installing-scikit-learn-on-an-apple-m1/)

```cpp
# Split the data into a training and testing set to test the accuracy of the model
# If you are happy with the accuracy of the model, you can remove this split
dataset_train, dataset_test, label_train, label_test = train_test_split(dataset, dataset_labels.ravel(), test_size=0.2)

# Build the support vector classification for our data and train the model
svc = SVC(kernel='poly', degree=2, gamma=0.1, C=100)
svc.fit(dataset_train, label_train)

# Test the accuracy of the model
print('Accuracy:', svc.score(dataset_test, label_test))
```

Once the model has been trained, it can be exported using the rather useful [micromlgen Python library](https://pypi.org/project/micromlgen/) which can convert ML models into raw C++ code to run on microcontrollers.

```cpp
from micromlgen import port
...
# Convert the model to C code and write to the classifier.h file
c_code = port(svc, classmap=label_map)
with open('classifier.h', 'w') as f:
    f.write(c_code)
    f.close()
```

You can find the training code in the [Microsoft IoT Curriculum resource GitHub repo in the labs folder](https://github.com/microsoft/iot-curriculum/tree/main/labs/tiny-ml/audio-classifier/code/model-trainer).

## Classify farts

The C++ code that comes out of the training can then be added to the microcontroller code. Instead of dumping the audio data to the serial port, it can be sent to the classifier code, and the label of the best match is returned.

```cpp
void processSamples()
{
  // Write out the classification to the serial port
  Serial.print("Label: ");
  Serial.println(clf.predictLabel(_samples));
}
```

## Learn more

You can find a complete hands on lab implementing this in the [Microsoft IoT Curriculum resource GitHub repo in the labs folder](https://github.com/microsoft/iot-curriculum/tree/main/labs/tiny-ml/audio-classifier).
