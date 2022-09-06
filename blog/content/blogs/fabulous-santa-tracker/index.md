---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.forms", "f#", "fabulous", "santa"]
date: 2018-12-24T00:00:00Z
description: ""
draft: false
images:
  - /blogs/fabulous-santa-tracker/banner.png
featured_image: banner.png
slug: "fabulous-santa-tracker"
tags: ["Technology", "xamarin", "xamarin.forms", "f#", "fabulous", "santa"]
title: "Fabulous Santa Tracker"

images:
  - /blogs/fabulous-santa-tracker/banner.png
featured_image: banner.png
---


> _'Twas the night before Christmas,
and all through the house..._

For millions of people worldwide, Christmas eve is a time of magic. Children are excited and unable to sleep because...

Santa is coming tonight!!!!

<div class="image-div" style="max-width:600px;">
    
![Santa](srikanta-h-u-51975-unsplash-1.jpg)
    
</div>

This is the one night of the year you want a stranger to come into your house whilst you sleep. He'll magic his way in (cos who has a chimney these days, right?), and leave presents under your tree. 

> _He know if you are sleeping,
He knows if you're awake..._

But - and this is important, he only comes if you are asleep. So children, you need to be asleep early. But how early? How do you know when you need to be asleep by?

For this - you need a Santa tracker mobile app. And not just any Santa tracker, a Fabulous one!

<div class="image-div" style="max-width:400px;">
    
![Screenshot of Santa tracker app](Simulator-Screen-Shot---iPhone-8---2018-12-05-at-11.31.25-1.png)
    
</div>

This app is pretty simple. It knows where Santa is at any given time on Christmas eve, and based on the current time displays the location of Santa on a map, along with a running count of how many presents he's delivered so far to all the good girls and boys.

The code is all on [GitHub](https://github.com/jimbobbennett/FabulousSantaTracker) if you want to check it out.

### Building the Santa tracker

To build this app I needed a source of data, and a mobile app.

##### Where did the data come from?

Every year for the past decade or so, NORAD has been [tracking Santa online](https://www.noradsanta.org) every Christmas eve. Unfortunately they don't seem to have a public API that I could find to use. Luckily Google has [got in on the action](https://santatracker.google.com/village.html), and provides [an undocumented API](https://storage.googleapis.com/santa/route-v1/santa_en.json) to download a JSON file containing Santas coordinates from last year. I simply downloaded that JSON document to use. The structure is pretty simple, and I've shown a snippet of it below showing only the bits I'm interested in.

```json
{
  "destinations": [
    {
      "arrival": 31536000000,
      "presentsDelivered": 0,
      "city": "Santa's Village",
      "region": "North Pole",
      "location": {
        "lat": 84.6,
        "lng": 168
       }
    },
    {
      "arrival": 1514110140000,
      "presentsDelivered": 46415,
      "city": "Provideniya",
      "region": "Russia",
      "location": {
        "lat": 64.436249,
        "lng": -173.233337
      }
    ...
  ]
}
```

This gives a city and region name for each stop, total presents delivered, the latitude and longitude of the location and the arrival time. This arrival time is the number of milliseconds since the UNIX epoch - 1 Jan 1970.

##### Creating the mobile app

For the mobile app, I wanted to use F#, and there is a great F# mobile framework called Fabulous!

**Fabulous?**

If you haven't heard of Fabulous yet, its an F#-based MVU framework (so like Elm) for building cross-platform mobile apps, built on top of the Xamarin.Forms platform. You can read all about it [in the docs](https://fsprojects.github.io/Fabulous/guide.html). There's even an [awesome-fabulous list](https://github.com/jimbobbennett/Awesome-Fabulous) containing cool projects that use it and some great resources.

You can create a new Fabulous app using the `dotnet` CLI. You install the template using:

```sh
dotnet new -i Fabulous.Templates
```

The create the app using:

```sh
dotnet new fabulous-app -n FabulousSantaTracker
```

This will create an F# solution with an Android app, an iOS app and a .NET standard library containing all the cross platform business logic and UI code.

##### Reading the JSON

Processing the JSON file is easy. First I added the downloaded JSON file to the core project, setting the build action to `EmbeddedResource`. Once I had this, I added a new F# source file and declared some new types to store the data.

```cs
type Location = { Lat : float; Lng : float }

type Destination = 
    {
        Arrival : float
        PresentsDelivered : int64
        City : string
        Region : string
        Location : Location
    }

type Destinations = array<Destination>

type SantaData = { Destinations : Destinations }
```

To read the JSON data I needed to read the embedded resource, then use Newtonsoft.JSON to deserialize it (the NuGet for this is included in the Fabulous template, so nothing extra to install).

```cs
let GetResourceString fileName = 
    let assembly = IntrospectionExtensions.GetTypeInfo(typedefof<Destination>).Assembly
    use stream = assembly.GetManifestResourceStream(fileName)
    use reader = new StreamReader (stream)
    reader.ReadToEnd()

let AllDestinations =
    let santaData = JsonConvert.DeserializeObject<SantaData>(GetResourceString "FabulousSantaTracker.santa_en.json")
    santaData.Destinations
```

The `GetResourceString` function loads the assembly and extracts the resource string from it. The name of these resource strings needs to be namespace qualified. For example the file in my project is called `santa_en.json`, and my namespace is `FabulousSantaTracker`, so the full resource name is `FabulousSantaTracker.santa_en.json`.

The last bit I needed was to convert the arrival date from milliseconds after epoch. These arrival dates are for last year (2017), so I needed to update them to the current year.

```cs
let convertFromEpoch ms =
    let d = epoch.AddMilliseconds (ms)
    d.AddYears(DateTime.UtcNow.Year - d.Year)
```

Now I have my data, it's time to display this on a map. Fabulous uses an MVU architecture, so I need to define a model, some messages, an update function to process these messages, and a view function.

###### Defining the model

The model is simple - it just needs Santa's current location by finding the latest destination in the list with an arrival time before now by working backwards through the list of destinations loaded from the JSON file. If Santa hasn't arrived anywhere yet then the first destination is used - this is Santa's workshop at the North Pole.

```cs
let currentDestination () =
    let current = TrackingData.AllDestinations |> Array.tryFindBack (fun i -> i.ArrivalDateTime < DateTime.UtcNow)
    match current with
    | Some d -> d
    | None -> TrackingData.AllDestinations |> Array.item 0

type Model = 
    {
        CurrentDestination : Destination
    }

let init () = { CurrentDestination = currentDestination() }, Cmd.none
```

###### Updating the map when Santa moves

The easiest way to update the current destination when Santa moves is a simple timer - fire a timer every few seconds and update the current destination. This can be implemented by defining a message for a timer tick, and when this is handled in the `update` function, update the models `CurrentDestination` on every tick.

```cs
type Msg = 
    | TimerTick

let update msg model =
    match msg with
    | TimerTick -> { model with CurrentDestination = currentDestination() }, Cmd.none
```

This message can then be fired using a subscription to a timer. These subscriptions are functions that take the Fabulous dispatcher and are called when setting up the program.

```cs
let timerTick dispatch =
        let timer = new Timer(TimeSpan.FromSeconds(10.).TotalMilliseconds)
        timer.Elapsed.Subscribe (fun _ -> dispatch TimerTick) |> ignore
        timer.Enabled <- true
        timer.Start()

let runner = 
    App.program
    |> Program.withSubscription (fun _ -> Cmd.ofSub App.timerTick)
```

Once this subscription is called, the timer is started and every 10 seconds the `TimerTick` message is dispatched. This causes the models `CurrentDestination` to be re-evaluated and the view then gets updated.

###### Drawing the view

Drawing the view is pretty simple. Fabulous uses a virtual UI, so your `view` function always returns a complete UI, and the internals of Fabulous compare the current with the result of the `view` call and applies the deltas to the real UI.

My view starts with a navigation page containing a content page with some emoji in the title:

```cs
let view (model: Model) dispatch =
    View.NavigationPage(
        pages = [
            View.ContentPage(
                title = "🎅 Tracker"
        ...
        ]
```

It then contains a grid with 3 rows. First row for the current location, second for the number of presents, third is a map.

The label to show the location has the text set like this:

```cs
View.Label(text = model.CurrentDestination.City,
```

This is one of the ways MVU differs from MVVM (the canonical design pattern for Xamarin.Forms apps) - the value for the location isn't bound to anything, it's just set using the value from the model. Updates to this value can only come from the `update` function, and after updating, the `view` function is called and the label is created with the new text. The differential update in the Fabulous framework will see this value change and update the UI.

To show the position on a map, we can use the `Fabulous.Maps` NuGet package which contains a wrapper for the Xamarin.Forms Map element. These wrappers are the way that Fabulous can provide a virtual UI, so is needed for each component you want to use in your `view` function. Once this NuGet is added, the map can be added to the view function.

```cs
View.Map(
    hasZoomEnabled = true,
    hasScrollEnabled = true,
    requestedRegion = MapSpan.FromCenterAndRadius(model.CurrentDestination.Position, Distance.FromKilometers(1000.0)),
    pins = [ 
        View.Pin(
            model.CurrentDestination.Position,
            label = "Santa",
            pinType = PinType.Place
        )
    ]
)
```

This code creates a map, sets the region to the position of the current destination (the position is an instance of the Xamarin.Forms `Position` class using the latitude and longitude from the JSON file) and zooms out to show a radius of 1,000Km. It will also add a pin at the position so that the user can see the position more accurately.

###### Using a custom map pin

This code so far shows where Santa is, and updates the UI when he moves, but doesn't look the best as the pin is, well just a map pin. It would be better to show Santa himself.

To do this I added some images to the iOS and Android apps of Santa, drawn by using the Santa emoji. To show these as a custom pin means I need to dive down into some platform specific code. One of the upsides of Xamarin.Forms, the underlying technology for Fabulous, is that you have access to the native UI components, so can update them as if your app was a fully native swift/java app.

<div class="image-div" style="max-width:68px;">
    
![Santa map pin image](Santa.png)
    
</div>

Accessing this native code involves the use of custom renderers - custom code to help Fabulous renderer the native controls. Customizing the map means creating my own `SantaMap` class that derives from the Forms `Map` class. 

```cs
type SantaMap() =
    inherit Xamarin.Forms.Maps.Map()
```

You can see the full implementation of this on [GitHub](https://github.com/jimbobbennett/FabulousSantaTracker/blob/master/FabulousSantaTracker/SantaMap.fs). There is a lot of code here, but is lifted from the original maps implementation so was minimal work. Hopefully in the future this will be easier!

Once this was in place, I needed to create the custom renderers to draw different pins. The Android one is:

```cs
type SantaMapRenderer(context : Context) =
    inherit MapRenderer(context)

    override this.CreateMarker(pin : Pin) =
        (new MarkerOptions()).SetPosition(new LatLng(pin.Position.Latitude, pin.Position.Longitude))
                             .SetTitle(pin.Label)
                             .SetIcon(BitmapDescriptorFactory.FromResource(Resources.Drawable.Santa))

module Export_SantaMapRenderer =
    [<assembly: ExportRenderer(typeof<SantaMap>, typeof<SantaMapRenderer>) >]
    do ()
```

Pretty simple - it uses the existing renderer and overrides the code to create the pins to use my Santa image. These renderers need to be registered with the framework to be used, and this can be done using the `ExportRenderer` attributes.

##### Fin!

That's all there is to this - a Santa tracker built using Fabulous. You can find all the code on GitHub here: https://github.com/jimbobbennett/FabulousSantaTracker

To build this app for iOS, just build it and run it and on Christmas eve watch for where Santa is. Android is a bit more effort as it needs a Google Maps key. You can find instructions on getting one in the [Xamarin Docs](https://docs.microsoft.com/xamarin/android/platform/maps-and-location/maps/obtaining-a-google-maps-api-key?WT.mc_id=santa-blog-jabenn). Once you have your key, add it to the `AndroidManifest.xml` file and track Santa!

Merry Christmas!

