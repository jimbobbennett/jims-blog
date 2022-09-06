---
author: "Jim Bennett"
categories: ["azure", "technology", "api", "keys"]
date: 2017-12-28T19:35:50Z
description: ""
draft: false
slug: "hiding-api-keys-from-git"
tags: ["azure", "technology", "api", "keys"]
title: "Hiding API keys from Git"

images:
  - /blogs/hiding-api-keys-from-git/banner.png
featured_image: banner.png
---


I've been working on a [Xamarin app using Azure Cognitive Services to do image recognition](/blogs/identifying-my-daughters-toys-using-ai/), and one of the stumbling blocks I've faced is what to do with my API keys. I want to make the app open source as an example of how to use these services, but don't want to check my API keys into Git to be available to all - after all, [bad things can happen](https://www.theregister.co.uk/2015/01/06/dev_blunder_shows_github_crawling_with_keyslurping_bots/).

I hit up twitter, and got a really awesome solution from [Bart Lannoeye](https://twitter.com/bartlannoeye):

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">You can add the file with *your key here* then change locally and git update-index --assume-unchanged .\pathtofile. Shows file as unchanged =&gt; can&#39;t commit by accident. <a href="https://twitter.com/hashtag/protip?src=hash&amp;ref_src=twsrc%5Etfw">#protip</a> We do the same for Kliva.</p>&mdash; Bart Lannoeye (@bartlannoeye) <a href="https://twitter.com/bartlannoeye/status/946437185372413952?ref_src=twsrc%5Etfw">December 28, 2017</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

This is exactly what I did, and it works perfectly. I've created a static class called `ApiKeys` which contains all my keys using "Your Key Here" values:

```
public static class ApiKeys
{
  public static string PredictionKey = "<Your API Key>";
  public static Guid ProjectId = Guid.Parse("<Your Project GUID>");
}
```

I then added this to Git and commited. After my commit I ran:

```
git update-index --assume-unchanged ./ApiKeys.cs
```

Done. I can then change the values to my actual API keys and Git doesn't see the change.

Obviously if I need to add any more keys to this file I'd have to revert this change, remove all keys, add the new one with a "your key" type value, commit, re-run the update-index and put the keys back. A bit of work, but at least no worries about anyone abusing my API limits!

Thanks Bart!

<hr>

__Update - how to tell users what they need to do with this code__

I've just had another great suggestion from [Brandon Minnick](https://developer.microsoft.com/en-gb/advocates/brandon-minnick), a fellow CDA here at Microsoft. He suggests adding a `#error` to the keys file so that when someone grabs the code and builds it they get an error telling them what to do, rather than a crash when the app is run:


```
public static class ApiKeys
{
# error You need to set up your API keys.
  // Start by registering for an account at https://customvision.ai
  // Then create a new project.
  // From the settings tab, find:
  // Prediction Key
  // Project Id
  // and update the values below
  public static string PredictionKey = "<Your Prediction Key>";
  public static Guid ProjectId = Guid.Parse("<Your Project GUID>");
}
```

<hr>

__Update 2 - how to fix it if you forget and add your keys__

Another great tip from [Brandon Minnick](https://developer.microsoft.com/en-gb/advocates/brandon-minnick) is the [BFG Repo-CLeaner](https://rtyley.github.io/bfg-repo-cleaner/). If you accidentally checked in some API keys, this tool can remove them from the Git history. 

Obviously it could be too late by the time you realize, so if you check any API keys in to a public repo you __MUST__ regenerate them as there are [bots that can GitHub for API keys](http://www.timbroder.com/2015/01/my-2375-amazon-ec2-mistake.html). But this is good for a private repo that you are planning to make public or accidentally add personal keys to.

