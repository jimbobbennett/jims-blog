---
author: "Jim Bennett"
categories: ["technology", "Python", "azure", "cognitive services", "speech"]
date: 2019-07-02T11:39:24Z
description: ""
draft: false
images:
  - /blogs/building-a-live-caption-tool/banner.png
featured_image: banner.png
slug: "building-a-live-caption-tool"
summary: "Learn how to build a live captioner using Python and the Azure Cognitive Services"
tags: ["technology", "Python", "azure", "cognitive services", "speech"]
title: "Building a live caption tool - part 1"

images:
  - /blogs/building-a-live-caption-tool/banner.png
featured_image: banner.png
---


I've started a [Twitch stream where I'm learning Python](https://twitch.tv/jimbobbennett) every Wednesday at 12pm UK time. One way I'd like to make my stream more accessible is by having live captions whilst I'm speaking.

What I need is a tool that will stream captions to something I can add to my OBS scenes, but also be customizable. A lot of off the shelf speech to text models are great, but I need something I can tune to my voice and accent, as well as any special words I am using such as technical tools and terms.

The [Azure Cognitive Services](https://azure.microsoft.com/services/cognitive-services/directory/speech/?WT.mc_id=livecaption-blog-jabenn) have such a tool - as well as using a standard speech to text model, you can customize the model for your voice, accent, background noise and special words.

In this part, I'll show how to get started building a live captioner in Python. In the next part, I'll show how to customize the output.

## Create the speech resource

To get started, you first need to create a Speech resource in Azure. You can do it from the Azure Portal by following [this link](https://portal.azure.com/?WT.mc_id=twitchcaptions-blog-jabenn#create/Microsoft.CognitiveServicesSpeechServices). There is a free tier which I'm using - after all we all love free stuff!

> If you don't have an Azure account you can create a free account at [azure.microsoft.com/free](?WT.mc_id=twitchcaptions-blog-jabenn) and get $200 of free credit for the first 30 days and a host of services free for a year. Students and academic faculty can sign up at [azure.microsoft.com/free/students](https://azure.microsoft.com/free/students/?WT.mc_id=livecaption-blog-jabenn) and get $100 that lasts a year as well as 12 months of free services, and this can be renewed every year that you are a student.

{{< figure src="2019-07-02_11-21-40.png" caption="" >}}

When the resource is created, note down the first part of the endpoint from the **Overview** tab. The endpoint will be something like `https://uksouth.api.cognitive.microsoft.com/sts/v1.0/issuetoken`, and the bit you want is the part before `api.microsoft.com`, so in my case `uksouth`. This will be the name of the region you created your resource in. You all also need to grab a key from the **Keys** tab.

Once you have your Speech resource the next step is to use it to create captions.

## Create a captioner

Seeing as my stream is all about learning Python, I thought it would be fun to build the captioner in Python. All the Microsoft Cognitive Services have [Python APIs](https://azure.microsoft.com/resources/samples/cognitive-services-python-sdk-samples/?WT.mc_id=livecaption-blog-jabenn) which makes them easy to use.

I launched VS Code (which has excellent Python support thanks to the [Python extension](https://code.visualstudio.com/docs/languages/python/?WT.mc_id=livecaption-blog-jabenn)), and created a new Python project. The Speech SDK is available via `pip`, so I installed via the Terminal it using:

```sh
pip install azure-cognitiveservices-speech
```

To recognize speech you need to create a `speechRecognizer`, telling it the details of your resource via a `speechConfig`.

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
```

In the code above, replace `speech_key` with the key from the Speech resource, and replace `service_region` with the region name.

> This will create a speech recognizer using the default microphone. If you want to change the microphone you will need to know the device id and use this to create an `AudioConfig` object which is used to create the recognizer. You can read more about this in [the docs](https://docs.microsoft.com/azure/cognitive-services/speech-service/how-to-select-audio-input-devices/?WT.mc_id=twitchcaptions-blog-jabenn).

The speech recognizer can be run as a one off and listen for a single block of speech until a break is found, or it can run continuously providing a constant stream of text via events. To detect continuously, an event needs to be wired up to collect the text.

```python
def recognizing(args):
    # Do something
    
speech_recognizer.recognizing.connect(recognizing)
speech_recognizer.start_continuous_recognition()
```

In the above code, the `recognizing` event is fired every time some text is recognized. This event is fired multiple times for the same set of words, building up the text over time as the model refines the output. After a break it will reset and send new text.

The `args` parameter is a `SpeechRecognitionEventArgs` instance with a property called `result` that contains the result of the recognition. This result has a property called `text` with the recognized text.

For example, if you run this and say "Hello and welcome to the speech captioner", this event will be called probably 7 times:

```
hello
hello and
hello and welcome
hello and welcome to
hello and welcome to the
hello and welcome to the speech
hello and welcome to the speech captioner
```

If you then pause and say "This works" it will be called 2 more times, with just the new words.

```
this
this works
```

The text is refined as the words are analyzed, so the text can change over time. For example if you say "This is a live caption test", you may get back:

```
this
this is
this is alive
this is a live caption
this is a live caption text
```

Notice in the third result there is the word "alive", which gets split into "a live" as more context is understood by the model.

The model doesn't understand sentences, and in reality humans rarely speak in coherent sentences with a structure that is easy for the model to break up, hence why you won't see full stops or capital letters.

The `start_continuous_recognition` call will run the recognition in the background, so the app will need a way to keep running, such as a looping sleep or an app loop using a GUI framework like Tkinter.

I've created a GUI app using Tkinter using this code. My app will put a semi-opaque window at the bottom of the screen that has a live stream of the captions in a label. The label is updated with the text from the `recognizing` event, so will be updated as I speak, then cleared down after each block of text ends and a new one begins.

You can find it on [GitHub](https://github.com/jimbobbennett/TwitchCaptioner), to use it add your key and region to the _config.py_ file, install the `pip` packages from the _requirements.txt_ file and run _captioner.py_ through Python.

In the next part, I'll show how to customize the model to my voice and terms I use.

