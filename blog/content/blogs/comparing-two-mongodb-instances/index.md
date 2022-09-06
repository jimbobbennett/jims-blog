---
author: "Jim Bennett"
date: 2015-06-18T15:55:12Z
description: ""
draft: false
slug: "comparing-two-mongodb-instances"
title: "Comparing two mongoDB collections"

images:
  - /blogs/comparing-two-mongodb-instances/banner.png
featured_image: banner.png
---


I'm doing some work for a client at the moment that involves storing files on disk and metadata about those files in a MongoDB instance.  The service that manages all this needs to support replication between multiple so that as a file or metadata record gets added/deleted/updated etc., the same changes are applied to all other services that the first on is replicated with.
All fairly simple, and quite a normal use case.

As part of my extensive automated testing I needed to be able to compare the resulting metadata after the replication to ensure that nothing is being missed.  After a quick look round I couldn't find anything to help with this, so I decided to write my own at home and open source it.

It's now on [my GitHub page](https://github.com/jimbobbennett/MongoDBCompare), and on Nuget:
```
PM> Install-Package JimBobBennett.MongoDbCompare
```

It's a simple tool designed to be called from .Net code to compare 2 collections that are based off a known .Net type.  You create the class using the type as the generic argument, passing in the connection details to the two MongoDB instances to compare.  You then call `CompareAsync` passing in a function that returns the unique id for each document so that it can marry up the collections and see if they match.
The comparison is done by using a simple `Equals` on each property in each document.  Properties marked as `BsonIgnore` are ignored, as are properties marked as `BsonId`.  You can also provide a list of names for properties that are also ignored (for example I'm using it to ignore a `LastAccessed` property that stores when the document was last accessed, which is different for each MongoDB instance).
The results that come back provide a list of documents that are only in the first collection, a list of documents that are only in the second, and a list of documents that are different.  At the moment it doesn't say which properties are different, but I'll hopefully be making a change to include this in a later release.

This is not PCL unfortunately, because the MongoDB drivers are not PCL compliant, an only supports .Net 4.5.

Hope it's helpful for someone.  Feel free to raise a PR for anything else you want it to support.

