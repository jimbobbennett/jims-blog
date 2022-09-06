---
author: "Jim Bennett"
categories: ["technology", "meetup", "video", "azure", "canon", "mxf", "encoding"]
date: 2019-04-02T09:38:50Z
description: ""
draft: false
images:
  - /blogs/making-video-editing-easier-with-azure-media-services/banner.jpg
featured_image: banner.jpg
slug: "making-video-editing-easier-with-azure-media-services"
summary: "Learn how Jim used Azure Media Services to fix his dumb mistakes when recording video!"
tags: ["technology", "meetup", "video", "azure", "canon", "mxf", "encoding"]
title: "Jim made some dumb mistakes when recording a video. You won't believe how he fixed it with Azure Media Services!"

images:
  - /blogs/making-video-editing-easier-with-azure-media-services/banner.png
featured_image: banner.png
---


I was at a recent [Reading .NET Meetup](https://www.meetup.com/Reading-NET-Meetup/), and wanted to record the event to make it available to members of the group who couldn't attend the event in person. This is part of my aim to [make meetups more accessible](https://github.com/jimbobbennett/MakingMeetupsMoreAccessible).

{{< figure src="IMG_0187.jpg" caption="" >}}

We have a cool box of recording git, courtesy of the [Channel9](https://twitter.com/ch9) team at Microsoft, including a Canon XC10 camera. This camera records using the Canon MXF format, a propriety format that doesn't work with my video editing app of choice, [Camtasia](https://www.techsmith.com/video-editor.html). I also made a basic video recording error, I recorded the video at 30fps, and the audio using a separate recorder at 60fps!

{{< figure src="IMG_0192.jpg" caption="" >}}

This needed to be fixed - I needed to align the frame rates, and convert the MXF files to MP4 to work with Camtasia. And this is where Azure Media services comes in.

[Azure Media Services](https://azure.microsoft.com/services/media-services/?WT.mc_id=azuremedia-blog-jabenn) is a suite of services that can encode and stream media. You create a media services resource, then you can use it to encode video either via the portal, or via [the SDK](https://docs.microsoft.com/azure/media-services/latest/?WT.mc_id=azuremedia-blog-jabenn).

### Getting started

The first thing to do is to launch the [Azure Portal](https://portal.azure.com/?WT.mc_id=azuremedia-blog-jabenn) and create a **Media Service** resource.

{{< figure src="2019-03-29_11-13-38.png" caption="" >}}

Once created, upload an asset - a video file to encode. From the Media Service resource, go to the _Assets_ tab and select _Upload_. Point it to your .MXF file and it will start uploading. You can upload more than one file at once if needed.

{{< figure src="2019-04-02_10-31-09.png" >}}

> Video files are huge - my smallest one was 6GB, so it takes a loooooooong time to upload if like me you have crappy bandwidth. Don't let your computer go to sleep as this interrupts the upload and you have to delete the asset and start again.

Once uploading starts, you will be able to see the video file in the _Assets_ tab. To encode it in the correct format, select the video file, then select _encode_.

From the **Encode an asset** tab, select the preset you want to use. The default is _Content Adaptive Multiple Bitrate MP4_, which provides adaptive streaming, changing the bitrate to match the streaming speed. This is great for content published on the net where viewers will be streaming it using different download speeds, but not so great for just re-encoding to bring into a video editing tool. Select an appropriate preset - I went for H264 Single Bitrate 1080p as I just want the highest bitrate and full size video. You can encode a video that is uploading - it will just queue the encoding job until the video is fully uploaded.

Again, this will take a long time!

Once the job is complete, head to the _Assets_ tab and select the encoded asset. Before you can download the video file you need to publish the asset using a progressive encoder. Click the **Publish** button, set the encoder as _Progressive_ and click **Add**.

{{< figure src="2019-04-02_13-24-13.png" >}}

The files for the asset wil be listed at the bottom, and one file will be a `video/mp4` file. Select this file, and the details on it will expand out the side, including a download link. Use this link to download the encoded file.

{{< figure src="2019-04-02_10-36-48.png" >}}

Done! You can now import this file into tools like Camtasia.

