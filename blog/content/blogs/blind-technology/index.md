---
author: "Jim Bennett"
categories: ["Technology", "technology", "binaural", "microsoft", "blind", "navigation"]
date: 2014-11-18T21:45:01Z
description: ""
draft: false
slug: "blind-technology"
tags: ["Technology", "technology", "binaural", "microsoft", "blind", "navigation"]
title: "Blind technology"

images:
  - /blogs/blind-technology/banner.png
featured_image: banner.png
---


Busy, busy, busy.  In the last month I've relocated form Thailand to the UK with my family, got my UK company up and running (more coming on this in a later post), lined up one client, fought with the Apple app store to get my developer account set up right so I can sell apps (still not done), found a new place to live and been fighting with overbearing bureaucracy.  I've also found loads of time to spend playing with my daughter before work becomes too overbearing, and the upshot of this is little time for technology.  My [Udemy course](/blogs/time-to-teach/) is still nowhere near finished, my apps are not on the Apple app store yet and I don't even have a working Windows 10 VM (mind you, from what I hear not many others do either).

Hey ho, back to the grindstone from now on.

One cool thing I did have time to do is head to Microsoft's Future Decoded conference in London.  It was a great day, some fantastic speakers (including that [drummer guy from D'Ream](http://bit.ly/14GyJJz)) and the chance to hear about some awesome technology.

The one piece that really caught my eye surprisingly wasn't the announcement that Microsoft have [open sourced .Net](http://blogs.msdn.com/b/dotnet/archive/2014/11/12/net-core-is-open-source.aspx) and released [new Visual Studio goodies](http://blogs.msdn.com/b/visualstudio/archive/2014/11/12/visual-studio-2015-preview-visual-studio-community-2013-visual-studio-2013-update-4-and-more.aspx).  It was in fact a software/hardware solution from [Microsoft Services work with Future Cities](https://futurecities.catapult.org.uk/project-full-view/-/asset_publisher/oDS9tiXrD0wi/content/project-cities-unlocked/) in conjunction with [Guide Dogs for the Blind](http://www.guidedogs.org.uk) to help blind people navigate.  A very good friend of mine is almost totally blind so I'm very interested in technology that helps people in his situation.  The history of the project is that they were asked to help people navigate around a new city, and seeing as one of their team is blind they decided it would be a good place to start - the needs of the sighted are a lot less than those of people who are visually impaired in a new city so solving for the harder case will also help ensure you cover as much as possible for the easy case.

The basic idea behind the project is to provide visually impaired people with the ability to navigate around a city.  For us sighted people it's easy - we whip out our smartphone and load up google maps.  If you're blind, this is impossible.  The Microsoft guys have come up with what is almost like turn by turn navigation using audio clues to guide you around.  Dogs are great for stopping you walking out in front of cars but can't distinguish between Starbucks and a dry cleaners.

The first part of the technology uses [binaural](http://en.wikipedia.org/wiki/Binaural_recording) sound processing - the ability to make a sound seem like it is coming from somewhere in 3D space using normal headphones.  Unlike normal stereo, this allows sounds to be behind, in front, above, or anywhere instead of simply left/right positioned.  Combine this with a smartphone with a built in compass and you have the ability to put sound in a particular location regardless of which way the user is facing (assuming the smartphone is facing the same way relative to the user of course).

The downsides for this as a navigation tool are that, as mentioned, the smartphone has to always be facing in the same direction as the user, as well as the user having to wear headphones.  A blind person would never want this as their ears are vital to navigating around.  If you can't hear traffic for example then you couldn't safely walk the streets.
The solution to both of these is a special headset.  It's based around bone conductivity headphones (these transmit sound by vibrating the bones in your skull allowing your ears to be free from blockages) with a box of electronics on the back that contains a compass, accelerometer and a bluetooth connection to the phone.  This means the headset can always be in the same relative direction to the user to allow the sound to be positioned accurately.

So now we have a tool that can track which way you are facing an provide audio clues at a given compass point.  So the next step is to combine this with GPS, map data and a speach interface.  For basic city walking it is able to name shops that you are interested in with the name being in the right direction to where you are facing.  It can also navigate you to a given destination using a simple sound in the direction you need to turn - so if the place you want is 100 yards ahead on the current street, then right for 50 yards then right again for 20 it will sound in front of you whilst you walk, then turn right when you should turn, then right again when you should turn then announce when you are at your destination.  All without being intrusive.

It sounds like such a simple solution and having tried it out I can say it is really well done.  I'm hoping they are going to open source the binaural technology so I can have a play at creating something similar.

Good work Microsoft!

