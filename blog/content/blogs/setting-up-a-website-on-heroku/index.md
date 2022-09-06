---
author: "Jim Bennett"
categories: ["Technology", "moomoo.io", "heroku", "web site"]
date: 2014-06-26T00:32:41Z
description: ""
draft: false
slug: "setting-up-a-website-on-heroku"
tags: ["Technology", "moomoo.io", "heroku", "web site"]
title: "Setting up a website on Heroku"

images:
  - /blogs/setting-up-a-website-on-heroku/banner.png
featured_image: banner.png
---


Now that I'm (almost) out of the rat race and working on my own apps, I though it was time to create a website to host my work.  I haven't got a company set up yet (that's coming soon) but I've been watching a rather excellent [Pluralsight training course on the MEAN stack](http://pluralsight.com/training/Courses/TableOfContents/building-angularjs-nodejs-apps-mean).  In this course they use [Heroku](http://www.heroku.com/home) to host a Node.js application, so I though I'd try it myself.

The advantages of Heroku that I can see are:

* Price - for 1 dyno, enough for a small load there's nothing to pay, no need to even give a credit card.  All free.  Great for development or a small site.  Scaling up is easy as well, just hand over the credit card and increase the number of dynos.
* Ease of setup - once you have an account, you just install the developer toolbelt, link your git repo to a remote Heroku repo and push the code.  You can push to an app you create on the Heroku site, or it'll even create the app for you.
* Simple configuration - getting things like a domain name set up is trivial.
* Loads of add ons - admitedly you have to hand over a credit card for verification first, but there are loads of easily available add ons like MongoDB, analytics, email, the list goes on.  All seem to have free tiers as well, again ideal for development.

I started with a basic node express app, nothing too fancy, just a 'coming soon' page using bootstrap.  Once this was running locally, I uploaded it to my private GitHub repo. This was my starting point.
The total time to get it running in Heroku was about an hour, and this is coming from never having done it before - and half of that was trying to figure out why it wasn't picking up the port from the environment variables (turned out I pushed the wrong branch).  I won't go into the details of how to do it, the [Heroku documentation](http://devcenter.heroku.com/articles/getting-started-with-nodejs) is excellent and the Pluralsight course mentioned earlier goes through the details as well.  DRY should apply to blogs as well you know!

Overall I was very impressed at how simple and easy it was.  I think I'll continue using Heroku for my website, especially when I add more features such as MongoDB.  Seeing as it runs Node.js as well, I should be able to create the servers for the apps I'm planning to write on it with ease.

Check out my website so far - not much but more is coming soon.

[MooMoo.io](http://www.moomoo.io)

![](Ducky.svg)

