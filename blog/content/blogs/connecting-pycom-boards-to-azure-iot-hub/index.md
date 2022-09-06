---
author: "Jim Bennett"
categories: ["technology", "Pycom", "Pymakr", "WiPy", "IoT", "azure", "Iot Hub", "Visual Studio Code", "vscode", "Python"]
date: 2019-04-10T12:38:16Z
description: ""
draft: false
images:
  - /blogs/connecting-pycom-boards-to-azure-iot-hub/banner.jpg
featured_image: banner.jpg
slug: "connecting-pycom-boards-to-azure-iot-hub"
summary: "Learn how to connect a PyCom board to Azure IoT Hub"
tags: ["technology", "Pycom", "Pymakr", "WiPy", "IoT", "azure", "Iot Hub", "Visual Studio Code", "vscode", "Python"]
title: "Connecting Pycom boards to Azure IoT Hub"

images:
  - /blogs/connecting-pycom-boards-to-azure-iot-hub/banner.png
featured_image: banner.png
---


I'm supporting an IoT hackathon over the weekend of April 27th/28th 2019. It will be a cool event, where you can win six months free business support from [SETsquared](https://twitter.com/setsquared) – the world’s leading university business incubator. If you are interested, sign up here:

[eventbrite.com/e/the-big-iothack-tickets-58111865153](https://www.eventbrite.com/e/the-big-iothack-tickets-58111865153)

As a part of this hackathon, [PyCom](https://pycom.io) are providing a load of devices. These are tiny IoT development boards that run MicroPython, and can connect over WiFi, BLE, [LoRa](https://lora-alliance.org) or [SigFox](https://www.sigfox.com/). PyCom have a service called PyBytes that can take data from the devices, and this can be integrated into [Azure IoT Hub](https://azure.microsoft.com/services/iot-hub/?WT.mc_id=pycom-blog-jabenn). To prepare for this event, I grabbed a board and started to play.

> You will need an Azure subscription to work thorough this. If you don't have one, you can sign up for free at [azure.microsoft.com/free](https://azure.microsoft.com/free/?WT.mc_id=pycom-blog-jabenn). This will give you $200 of credit, access to free services for 12 months, and other services free forever. You will need a credit card, but this is only for validation - you will **NOT** be billed unless to choose to upgrade your subscription.

## Getting started

### Unpack the board

We were given a big box of kit to try out before the hackathon. It had a range of boards and shields inside.

{{< figure src="IMG_0290.jpg" >}}

I grabbed a WiPy and a Pysense board.

The [WiPy](https://pycom.io/product/wipy-3-0/) is a WiFi and BLE enabled board running an ESP32 micro controller. It doesn't have any sensors or USB connectivity, it needs to be added to an expansion board.

{{< figure src="IMG_0286.jpg" >}}

The [PySense](https://pycom.io/product/pysense/) is an expansion board that the WiPy plugs into. It has a load of sensors as well as a USB port you can use to program the micro controller.

{{< figure src="IMG_0287.jpg" >}}

### Plug it in

The boards fit together, with the WiPy plugging into the socket on the Pysense. It took a bit of research to determine which way round to plug it in. Next I connected a WiFi antenna. Once it was all plugged together I connected the USB port to my Mac and an LED started flashing! Everyone loves blinking LEDs.

{{< figure src="IMG_0293.jpg" >}}

I then did the usual dance to upgrade the firmware by following the [PyCom docs](https://docs.pycom.io/gettingstarted/installation/firmwaretool.html). As a heads up, if you are using a Mac, unplug everything from the USB ports first otherwise you'll get errors as it tried to push the firmware to the wrong device!

### Configure the software

Like a lot of developers, I love [Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=pycom-blog-jabenn)! PyCom provides an [extension for Code](https://marketplace.visualstudio.com/itemdetails?itemName=pycom.Pymakr&WT.mc_id=pycom-blog-jabenn) that can talk to their boards.

{{< figure src="2019-04-10_10-39-54.png" >}}

### Write some code!

These boards run [MicroPython](https://www.micropython.org), an implementation of Python designed to run on micro controllers. MicroPython projects have the following structure:

```
Project folder
|-lib
|  |- some_library.py
|- boot.py
|- main.py
```

Inside the project folder, there is an optional `lib` folder and two `.py` files. `boot.py` is optional and contains any code that you want run when the board boots up, such as connecting to WiFi. You can think of this as the same as the `setup` function in an Arduino C project. `main.py` is not optional, and contains the main code that will run on the device, analogous to the `loop` function in Arduino. It isn't a loop as such, it won't be called continuously, instead you will need to add your own processing loop. The `lib` folder is where you can put other `.py` files. This is the only directory that MicroPython will look in, you can't put files in other directories or sub-directories of `lib`.

I created a new folder, and added `main.py` file. The code for this file  is:

```python
import pycom
import time

pycom.heartbeat(False)      # Turn off the heartbeat

while True:
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)           # Sleep for 1 second
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)           # Sleep for 1 second
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)           # Sleep for 1 second
```

This code imports the `pycom` module containing code to interact with the board, and a  [`time` module](https://docs.python.org/3/library/time.html) to provide access to code to sleep.

The code starts by turning off the heartbeat - this is a regular pulse of the on-board LED that shows you the board is powered on.

Next it runs a loop - using a `while True:` loop to always run the code. The suite inside this loop sets the LED to red, sleeps for a second, then green, sleep, then blue, sleep.

> Python is different to a lot of other languages in that `sleep` takes a time in seconds, not milliseconds.

To deploy the code, launch the command palette and select _Pymakr->Run current file_. This will compile the code and run it to the device. Once done, the LED will start to flash red, then green, then blue.

{{< figure src="2019-04-10_11-06-04.png" >}}

This only runs the code on the device, it doesn't store it permanently, so once the device is rebooted, the code is wiped. To upload the code so that it is maintained between reboots, use _Pymakr -> Upload project_.

## Send data to the cloud using PyBytes

Getting an LED flashing is cool, but what is cooler is getting data and sending it to the cloud. PyCom has a service called [PyBytes](https://pybytes.pycom.io/) that takes in data from PyCom devices.

### Connect to PyBytes

PyBytes makes it easy to configure your device. You add a new device from their Web dashboard, set up a unique name for it and the WiFi details for the WiFi you want the PyCom device to connect to. You then get an activation token that you can use when flashing the firmware to push these details to the device.

Flash the firmware, and configure it for PyBytes, setting the activation token.

Once the firmware is updated, the device will appear in the PyBytes dashboard.

{{< figure src="2019-04-10_11-30-17.png" >}}

### Set up the dashboard to receive some data

PyBytes manages data as signals. A signal is data sent from the device, identified by a unique number. The PyBytes dashboard takes the signal data, enriches it with a name and unit and allows it to be displayed on a dashboard.

From the **Data** tab on the dashboard, I defined a new signal called **Temperature** for ID `0`, with the unit set to °C.

{{< figure src="2019-04-10_11-34-34.png" >}}

### Send some data

Once the signal was created, I needed to send data to it from the PySense temperature sensor. There are libraries for accessing the PyBytes API, and the PySense board, and these need to be grabbed from the [PyCom GitHub repo](https://github.com/pycom/pycom-libraries) and dropped in the `lib` folder. I grabbed the `[pysense.py](https://github.com/pycom/pycom-libraries/blob/master/pybytes/pysense/lib/pysense.py)` and `[pycoproc.py](https://github.com/pycom/pycom-libraries/blob/master/pybytes/pysense/lib/pycoproc.py)` libraries to talk to the PySense board, and the `[SI7006A20.py](https://github.com/pycom/pycom-libraries/blob/master/pybytes/pysense/lib/SI7006A20.py)` library to access the temperature sensor.

The code I used to send the data is:

```python
import pycom
import _thread
from pysense import Pysense
from SI7006A20 import SI7006A20
from time import sleep

pycom.heartbeat(False)

py = Pysense()         # Connect to the PySense board
si = SI7006A20(py)     # Connect to the temperature sensor

while True:
    pycom.rgbled(0x0000FF)         # Flash the LED blue
    temp = si.temperature()        # Get the temperature
    pybytes.send_signal(0, temp)   # Send the temperature using signal 0
    pycom.rgbled(0x000000)         # Turn off the LED
    sleep(5)                       # Sleep for 5 seconds
```

This uses the `SI7006A20` temperature sensor to get the temperature, then sends a signal to PyBytes, using a signal id of `0`. This data then appears on the PyBytes dashboard.

{{< figure src="2019-04-10_12-04-12.png" >}}

## Integrate PyBytes with IoT Hub

PyBytes supports integrations with [Azure IoT Hub](https://azure.microsoft.com/services/iot-hub/?WT.mc_id=pycom-blog-jabenn), and it can push the data received from the device into IoT Hub.

### Create an IoT Hub

I created a new IoT Hub instance to send the data to. I've got the [Azure IoT Device Workbench extension](https://marketplace.visualstudio.com/itemdetails?itemName=vsciot-vscode.vscode-iot-workbench/?WT.mc_id=pycom-blog-jabenn) installed in Visual Studio Code, and this provides capabilities to configure IoT services from inside Code.

From the command palette, selecting _Azure IoT Hub -> Create IoT Hub_ allows you to create a new IoT Hub. Follow the instructions, and you get a new IoT Hub set up.

### Integrate the IoT Hub into PyBytes

When the IoT Hub is running, open it up in the [Azure Portal.](https://portal.azure.com/?WT.mc_id=pycom-blog-jabenn) Head to _Settings -> Shared Access Policies_, select the _registryReadWrite_ policy and copy the _Connection string - Primary key_. PyBytes needs read and write permissions on the registry to register devices for you - each device configured in PyBytes becomes a device in IoT Hub.

{{< figure src="2019-04-10_12-31-07.png" >}}

From PyBytes, select _Integrations -> New Integration_. Select _Microsoft Azure_, then paste the connection string and select _Login_. Give the integration a name, enter a topic for the messages and select the devices you want to include. Then select **Create**. Once the integration is created, you can send a test message, then check for this in the IoT Hub.

{{< figure src="2019-04-10_13-01-16.png" >}}

You will also be able to see the device in the devices list both in the IoT Hub list, and in the _Azure IoT Hub Devices_ section in the explorer. You can right-click on the device in the explorer and select _Start monitoring D2C messages..._ to see a stream of the messages in the output window.

{{< figure src="2019-04-10_13-02-35.png" >}}

The data is raw, unenriched data showing the signal id and value.

## Next steps

Now that the data is flowing into IoT Hub, you can do anything you want with it - enrich it using [stream analytics](https://azure.microsoft.com/services/stream-analytics/?WT.mc_id=pycom-blog-jabenn) or an [Azure function](https://azure.microsoft.com/services/functions/?WT.mc_id=pycom-blog-jabenn), do [time series insights](https://azure.microsoft.com/services/time-series-insights/?WT.mc_id=pycom-blog-jabenn) on it, anything you want!

---

All the code for this project is available on GitHub here: [github.com/jimbobbennett/PyCom-AzureIoTHub](https://github.com/jimbobbennett/PyCom-AzureIoTHub)

