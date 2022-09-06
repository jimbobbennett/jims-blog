---
author: "Jim Bennett"
categories: ["xamarin", "xamarin.forms", "AI", "computer vision"]
date: 2018-05-30T16:05:41Z
description: ""
draft: false
slug: "describing-a-photo-in-a-mobile-app-using-azure-computer-vision"
tags: ["xamarin", "xamarin.forms", "AI", "computer vision"]
title: "Describing a photo in a mobile app using Azure Computer Vision"

images:
  - /blogs/describing-a-photo-in-a-mobile-app-using-azure-computer-vision/banner.png
featured_image: banner.png
---


I recently gave an introduction to Xamarin talk at [Imperial College, London](http://www.imperial.ac.uk) and wanted to build a cool app to show off what you can do on mobile using the awesome Cognitive Services available on Azure. I only had about 30-40 minutes to not only introduce Xamarin, but build an app so I decided to throw together a simple app to take a photo and describe it using the [Azure Computer Vision](https://docs.microsoft.com/azure/cognitive-services/computer-vision/home/?WT.mc_id=imperial-blog-jabenn) service.

It really is simple to set up and use this service. Head to the [Computer Vision cognitive services site](https://azure.microsoft.com/services/cognitive-services/computer-vision/?WT.mc_id=imperial-blog-jabenn), click the big __Try the Computer Vision API__ button. Log in with an appropriate provider, and get an API key, noting the region the key is for.

From inside your Xamarin app, install the pre-release [Microsoft.Azure.CognitiveServices.Vision.ComputerVision](https://www.nuget.org/packages/Microsoft.Azure.CognitiveServices.Vision.ComputerVision/) NuGet package into all the projects. Then install the [Xam.Plugin.Media](https://www.nuget.org/packages/Xam.Plugin.Media/) NuGet package and follow the instructions in the `readme.txt` that is auto-opened to enable permissions and other gumpf.

Add some code to take a photo using the media plugin:

```cs
var opts = new Plugin.Media.Abstractions.StoreCameraMediaOptions();
var photo = await Plugin.Media.CrossMedia.Current.TakePhotoAsync(opts);
```

Next, set up the Computer Vision API by creating an `ApiKeyServiceClientCredentials` with your API key, then constructing an instance of `ComputerVisionAPI` using these credentials, not forgetting to set the region.

```cs
    var creds = new ApiKeyServiceClientCredentials("<your key here>");
    var visionApi = new ComputerVisionAPI(creds)
    {
        AzureRegion = AzureRegions.Westeurope
    };
```

Finally, get a stream containing the image and pass it to the computer vision API.

```cs
var desc = await _visionApi.DescribeImageInStreamAsync(photo.GetStream());
```

You can then access a description for the image using the `Captions` property on the `ImageDescription` that is returned. You can also get a list of tags for the image using the `Tags` property. The image below shows my app using this to caption an image.

<div class="image-div" style="max-width:320px;">
    
![The app running showing an image and its description](IMG_7078.jpg)
    
</div>


You can find the code for this on [my GitHub](https://github.com/jimbobbennett/PhotoDescriber), and you can read more on the computer vision service in the [docs](https://docs.microsoft.com/azure/cognitive-services/computer-vision/home/?WT.mc_id=imperial-blog-jabenn).

