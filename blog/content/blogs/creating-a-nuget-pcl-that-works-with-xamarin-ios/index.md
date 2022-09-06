---
author: "Jim Bennett"
categories: ["Technology", "iOS", "xamarin", "nuget", "xamarin.ios", "pcl", "nuspec", "httpclient", "portable class library"]
date: 2014-08-07T06:33:27Z
description: ""
draft: false
slug: "creating-a-nuget-pcl-that-works-with-xamarin-ios"
tags: ["Technology", "iOS", "xamarin", "nuget", "xamarin.ios", "pcl", "nuspec", "httpclient", "portable class library"]
title: "Creating a NuGet PCL that works with Xamarin.ios"

images:
  - /blogs/creating-a-nuget-pcl-that-works-with-xamarin-ios/banner.png
featured_image: banner.png
---


I've been playing with Xamarin.Forms recently to develop an iOS app.  The aim is to use my [portable open source Plex API](https://github.com/jimbobbennett/ComPlexion) in the app (more details of the app will come later once it's ready to release).

The basic concept of [Xamarin.Forms](http://xamarin.com/forms) is to have a core portable class library containing all the application code, and very thin platform specific libraries that wrap the core code in an application that targets the relevant platform.

In principle - all very easy.  The problem comes when you want to use other libraries with it.  These libraries must be portable class libraries - PCLs.  Again in principle, very easy.  But the devil is in the details...

The main stumbling block I hit was HttpClient.  The Microsoft PCL I use to access the Plex REST API.  In principle this is a PCL so should work on all platforms.  But it doesn't.
The issue is actually with Xamarin.ios.  This doesn't support the Microsoft HTTP client, instead it uses the Mono version.  This means my Plex API has to target both the MS and Mono versions - which is a problem as the namespaces are the same, and my iOS app project can't have a dependency to the MS version, and the Windows Phone project can't have a dependency to the Mono version.

My solution was to do the following:

* Change my code library code to not access the HTTPClient directly, but have an interface to a wrapper class.
* Create a Xamarin.ios class library project that has an implementation of the interface using the Mono HTTPClient library.
* Create a Windows PCL project (Windows 8, Windows Phone and Windows Phone Silverlight) that links to the source of the iOS implementation (the namespaces are the same so the source can be shared) that references the MS PCL HTTPClient NuGet package.

This will spit out 3 dlls - one PCL for the core with no HTTP access, an iOS class library using the Mono HTTPClient and a Windows PCL that uses the MS HTTPClient.

Next challenge was to get this into a NuGet package.  The more recent versions of NuGet have full PCL support which makes the whole thing easier.
To install the dlls into the correct targets I just had to ensure the target of the files was set to the correct location:

```
<files>
  <!-- portable -->
  <file src="..\Complexion.Portable\bin\$Configuration$\Complexion.Portable.dll" target="lib\portable-net45+win+wp80+MonoAndroid10+MonoTouch10\Complexion.Portable.dll" />
    
  <!-- ios -->
  <file src="..\Complexion.Portable\bin\$Configuration$\Complexion.Portable.dll" target="lib\MonoTouch10\Complexion.Portable.dll" />
  <file src="..\Complexion.ios\bin\iPhone\$Configuration$\Complexion.ios.dll" target="lib\MonoTouch10\Complexion.ios.dll" />
    
  <!-- Win -->
  <file src="..\Complexion.Portable\bin\$Configuration$\Complexion.Portable.dll" target="lib\portable-net45+win+wp80\Complexion.Portable.dll" />
  <file src="..\Complexion.Win\bin\$Configuration$\Complexion.Win.dll" target="lib\portable-net45+win+wp80\Complexion.Win.dll" />
</files>
```

The core portable library is output to a fully portable target, as well as to individual targets for iOS and Windows.  The individual platform specifi dlls are then output to specific targets.  Using this setup, if I install this package to a portable project, just Complexion.Portable is installed.  If it's for iOS (MonoTouch) then Complexion.Portable and Complexion.ios is installed.  Similarly for Windows 8/Windows Phone Complexion.Portable and Complexion.Win gets installed.

The final addition was dependencies.  For the portable dll there are no other dependencies.  For ios there are also no additional dependencies as the Mono HTTPClient is available in the default Xamarin.iOS references.  Windows is different though - it needs the Microsoft HTTPClient NuGet package installed.
Thankfully [NuGet now supports dependencies by different targets](http://docs.nuget.org/docs/reference/nuspec-reference#Specifying_Dependencies_in_version_2.0_and_above).  Groups can be defined with a target attribute and these are only installed into projects that match the target.  This means I can add groups for the different windows targets that have the Microsoft HTTPClient dependency, and nothing will be installed for other platforms.

```
<dependencies>
  <group targetFramework="net45">
    <dependency id="Microsoft.Bcl" version="1.1.9" />
    <dependency id="Microsoft.Bcl.Build" version="1.0.14" />
    <dependency id="Microsoft.Net.Http" version="2.2.22" />
  </group>
  <group targetFramework="win">
    <dependency id="Microsoft.Bcl" version="1.1.9" />
    <dependency id="Microsoft.Bcl.Build" version="1.0.14" />
    <dependency id="Microsoft.Net.Http" version="2.2.22" />
  </group>
  <group targetFramework="wp80">
    <dependency id="Microsoft.Bcl" version="1.1.9" />
    <dependency id="Microsoft.Bcl.Build" version="1.0.14" />
    <dependency id="Microsoft.Net.Http" version="2.2.22" />
  </group>
</dependencies>
```

Check out [my GitHub project](https://github.com/jimbobbennett/ComPlexion) for the full API code nuspec file.

