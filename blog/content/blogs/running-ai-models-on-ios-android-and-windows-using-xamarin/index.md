---
author: "Jim Bennett"
categories: ["xamarin.forms", "AI", "windows", "iOS", "Android", "onnx", "nuget", "technology", "xamarin"]
date: 2018-07-20T16:59:01Z
description: ""
draft: false
slug: "running-ai-models-on-ios-android-and-windows-using-xamarin"
tags: ["xamarin.forms", "AI", "windows", "iOS", "Android", "onnx", "nuget", "technology", "xamarin"]
title: "Running AI models on iOS, Android and Windows using Xamarin"

images:
  - /blogs/running-ai-models-on-ios-android-and-windows-using-xamarin/banner.png
featured_image: banner.png
---


I created a [NuGet package](https://www.nuget.org/packages/Xam.Plugins.OnDeviceCustomVision/) a while ago to allow you  to run models exported from the [Azure Custom Vision](https://customvision.ai) service on iOS and Android in Xamarin apps from your cross-platform code. You can read about this [here](/blogs/identifying-my-daughters-toys-using-ai-part-5-plugin-for-on-device-models/).

Since then, the Custom Vision service has added [ONNX export](/blogs/running-custom-vision-models-on-a-windows-device/), meaning you can now run these models on-device on Windows as well. This meant it was time to update my plugin to support Windows.

This was released in v2.0 of the plugin - I thought I'd be a good developer and bump the major version number as I've broken the API.

#### API changes

The main change is that the `IImageClassifier.Init` method has now gone. When I wrote this it was a bit of a fudge - it took a single model name and a model type. The model type was only needed on Android as some image adjustments needed to be made based on the model type used. It also meant that there was no way to use a different TensorFlow labels file, it had to be called `labels.txt`. With Windows, the `Init` call would need a list of labels, so it made sense to strip it down and have platform-specific calls to allow each platform to be passes just what is needed.

##### Initialization on iOS

Models can be compiled before being used, or compiled on the device. To use a pre-compiled model, compile the downloaded model using:

```sh
xcrun coremlcompiler compile <model_file_name>.mlmodel <model_name>.mlmodelc
```

Add the model (compiled or uncompiled) to the `Resources` folder in your iOS app. Then initialize the plugin using:

```cs
iOSImageClassifier.Init("<model_name>");
```

Passing in the name of the model without the `mlmodel` or `mlmodelc` extension. If the model is uncompiled, it will be compiled before use.

##### Initialization on Android

Add the `model.pb` and `labels.txt` files to the `Assets` folder of your Android app. Then initalize the plugin using:

```cs
AndroidImageClassifier.Current.Init("model.pb", "labels.txt", ModelType.General);
```

These values are actually defaults, so you can leave these off and just use `AndroidImageClassifier.Current.Init()` if you want.

> A note about model types. You needed the model type because the original TensorFlow export created models that needed image adjustments for some model types to work correctly. Since 7th May 2018 then models have a layer that adjusts for this automatically. The plugin will detect this and only make image adjustments if needed, so the model type is only relevant for models created before this date. It is ignored for models created after.

##### Initialization on Windows

Add the `<model>.onnx` file to the `Assets` folder of your Windows app. A `<model>.cs` file will be created to process the model in the root of your UWP app. The wrapper will have a class called `<model>ModelOutput` and in the constructor for this class will be some code to create a dictionary called loss:

```cs
this.loss = new Dictionary<string, float>()
{
    { "<label 1>", float.NaN },
    { "<label 2>", float.NaN },
    ...
};
```

This defines the labels in the correct order for the model. These labels will need to be passed to the `Init` method in the correct order.

The `Init` method on Windows is also an async method, so will need to be called from another async method, such as by overriding `OnNavigatedTo` on a page and marking it as `async`. Await the init method passing the model name and labels like this:

```cs
await WindowsImageClassifier.Init("Currency", new[] { "<label 1>", "<label 2>", ... });
```

<hr/>

I'm sure this can be improved, including adding code to detect the labels from the ONNX model, so feel free to raise a PR with any improvements. All the code is on [GitHub here](https://github.com/jimbobbennett/Xam.Plugins.OnDeviceCustomVision).

