---
title: "What is edge computing, why do it, why send IoT data to the cloud?"
date: 2020-12-03
draft: false
featured_image: "asaedge-highlevel-diagram.png"
images: 
  - "blogs/what-is-edge-computing/asaedge-highlevel-diagram.png"
tags: ["ai", "iot", "edge" ,"iot-edge", "cloud"]
description: This blog post is a mind dump in the style of I didn't have time to give you a short answer, so I wrote a long blog post instead on the difference between edge computing and just using the cloud, along with the whys and hows.
---

I recently had a student reach out to me with some great questions around Edge computing and how it matches to IoT, and indeed why even use the cloud with IoT. They have to write a paper on the difference between edge computing and just using the cloud, and were researching these terms and trying to understand the whys and hows.

There is currently a lot of confusion around this topic, especially when product pages are full of buzzwords, marketing speak and business decision maker language, not student friendly explanations, so I thought I'd take a moment to try to answer their questions with a blog post and hopefully help others navigate this minefield.

This blog post is a mind dump in the style of I didn't have time to give you a short answer, so I wrote a long blog post instead, so comments and criticism welcome.

## Temperature detection

I'm going to frame all this with the canonical IoT example of temperature detection. It's one of the 'easiest' IoT scenarios in that there are a huge range of devices and examples out there for this. You take an IoT device such as a micro controller (for example an Arduino board) or a single-board computer (for example a Raspberry Pi), attach a temperature sensor, and gather the data.

## What is cloud computing?

Lets start with the cloud. The cloud is someone elses computer - you pay per use for either computing resources or software resources managed by someone else. it allows you to not worry about purchasing hardware, managing cooling, electricity and networking, managing software, security, patching and the other day to day operations, and instead outsources these to experts. The cost comes down - you only pay for what you need when you need it, and speed of delivery goes up as the services are pretty much instant on.

In the IoT space for example, a few clicks brings you a service you can securely send IoT data to, and a well defined way to get the data back out for analysis, all for a modest monthly fee. Running the same setup manually would be highly expensive and a lot of work.

### Why send this data to the cloud?

A great question - why use the cloud when you can just read the data yourself, either by showing it on a screen or even by connecting to a Raspberry Pi and reading the values?

The answer lies in the rise of the smart thermostat. In the house I grew up in, the temperature sensor was a dumb device - it detected the temperature and if it was lower than a value on a thermostat, the heating turned on. The next generation was connected thermostats - sending the data to the cloud. This added a level of usability to these devices - yes you could walk to the thermostat and check the temperature of your house, but you could also get this on your phone. Combine this with the ability to also control the thermostat remotely you have a great advantage of using the cloud. You can check the temperature of your house from anywhere and control it from anywhere. On your way home unexpectedly on a cold day? You can check how cold your house is and turn the heating up if it's set to a colder vacant setting. The cloud starts to take your data and control anywhere.

Yes, if you don't care and just want a wall thermometer then there's no need, but as soon as you want access away from the temperature sensor, the cloud wins.

The next generation of smart thermostats is around analyzing this data in the cloud. A disconnected device relies on manual control, a cloud connected device can use algorithms to make control decisions for you based on a wide variety of data. Your cloud connected thermostat can check your calendar, and if it sees you are on vacation it can turn your heating off. It can also check weather, and if the heating is off but a cold snap is coming it can turn it on to stop pipes freezing. All this comes via having the data and control in the cloud.

This idea can be taken further with temperature monitoring of factories and machinery - sometimes subtle variations in temperature of a machine component can indicate an upcoming failure. By constantly monitoring the temperature, with data sent to AI models, you can be do predictive maintenance, replacing a part early before a costly failure.

### The downside of the cloud

The cloud isn't perfect, and can have a couple of downsides - though these can be mitigated.

* Reliance on the cloud

    Recently one of the big cloud providers had an outage, and social media was full of complaints from people who can't vacuum their house as the cloud was down. If your device relies on the cloud, it also needs to work when the cloud is not there - I don't want a WiFi outage or a data center fire to stop me from having heating, especially if I lived in a really cold location! There are also locations where internet connections are unavailable or expensive, such as oil rigs or deep underground, or even in space.

* Data privacy

    The cloud is secure, and the big clouds have a lot of certifications and approvals for data security, but there might be times when you don't want data in the cloud. For example, some countries insist on personal data remaining in-country (data sovereignty laws). If the cloud doesn't have a data center in your country, you have to store it locally or on a local data center. Some data, such as medical data might need to stay on-site in a hospital.

* Bandwidth and network speed

    Bandwidth isn't free. If you want to run AI models to analyze video from security cameras, sending all that data to the cloud is going to need a lot of bandwidth. That's expensive, and not always available. The internet is also not as fast as internal networks, so if you need the data or results of analysis quickly then it might be faster to have the analytics closer to the data capture.

* Cost

    The cloud brings the cost down, but sometimes you don't want or need to pay for the power of the cloud. It might be that a $99 NVIDIA Jetson Nano can run your AI models fast enough that you don't want to rent a $100 a month GPU-powered VM in the cloud.

This is where Edge computing comes in.

## What is edge computing?

Edge computing is running parts of the cloud on the edge - that is on your own network in your building or data center. You can take advantage of the cloud to build and train workloads, then deploy them to an edge device to run closer to your data. This way you get the benefit of the scalable power of the cloud to train complex models, and the advantage of local compute to:

* Avoid dependency on the internet and the cloud - your models can run offline, so if the cloud or internet goes down, or if you are away from the internet such as at sea, they keep running.
* Keep your data private and local
* Not be limited by external bandwidth and internet speed, only be limited by your internal network bandwidth
* Control costs using existing hardware

Thinking about factory monitoring - you can do this so much better on the edge than in the cloud. You can gather the data you need and train complex AI models for predictive maintenance in the cloud. Once trained, you can download these models to an IoT Edge device built using cheap hardware. This device can be on your local network close to the machinery, and respond to temperature data - instantly alerting someone or even turning the machinery down or off it it detects a possible failure. If the internet or the cloud goes down - the device still works. If you send millions of data points to it for analysis, you are not limited by outgoing internet speeds.

These models running on the edge are not static - you can constantly improve and retrain models in the cloud and deploy them to the edge as required.

You can also use these edge devices as gateways - sending data up to the cloud as needed. This can be filtered data, such as removing duplicate values or data within an allowed range, or they can be used to route data from devices that can't connect to the cloud services directly. They can even shield devices from being connected directly to the internet of these devices are not secure.

To visualize how this works - I'm going to defer to an article from the Microsoft Documentation covering [running Stream Analytics on IoT Edge](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-edge). Stream Analytics is a tool for creating real-time queries against streaming data, outputting the results of the query to other systems. Stream Analytics jobs can be run in the cloud, or downloaded onto an IoT Edge device and run on the edge.

![High-level diagram of IoT Edge](asaedge-highlevel-diagram.png)

This diagram shows IoT Edge devices running Azure Stream Analytics jobs via the IoT Edge runtime, running on-premise in a factory, with data coming in from a variety of devices. The results of the Stream Analytics job are then sent on to Azure IoT Hub for further analytics if needed.

## More resource

If you want to learn more about this topic - here's some great resource:

* [Azure IoT Edge product page](https://azure.microsoft.com/services/iot-edge/)
* [Azure IoT Edge documentation](https://docs.microsoft.com/azure/iot-edge/)
* [Run cognitive services on IoT Edge](https://youtu.be/LaAiyuzPRyY) - a video where I am joined by [Marko Paloski](https://twitter.com/mpaloski) and we talk about running a pre-built AI service on the Edge using Azure IoT Edge
* [AI Edge engineer learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/ai-edge-engineer/?WT.mc_id=academic-11509-jabenn) - a learning path produced in partnership with the [University of Oxford](https://www.conted.ox.ac.uk/courses/artificial-intelligence-cloud-and-edge-implementations) covering AI on the edge
* [Build the intelligent edge learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/build-intelligent-edge-with-azure-iot-edge/) - a learning path covering how to use Azure IoT Edge to build IoT solutions that require having cloud intelligence deployed locally on IoT Edge devices
* [Microsoft IoT Curriculum resource](https://github.com/microsoft/iot-curriculum) - a GitHub repo of resources, curated links and labs for IoT classes, projects and learning
* [Assembly line QA lab](https://github.com/microsoft/iot-curriculum/tree/main/labs/ai-edge/vision/manufacturing-part-check) - a hands-on-lab covering how to use IoT edge to do AI-powered assembly line validation