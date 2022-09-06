---
author: "Jim Bennett"
categories: ["fsharp", "f#", "azure", "functions", "technology"]
date: 2018-06-19T15:59:44Z
description: ""
draft: false
slug: "what-the-fixing-weirdness-in-return-json-from-azure-functions-using-f"
tags: ["fsharp", "f#", "azure", "functions", "technology"]
title: "What the @ - fixing weirdness in return JSON from Azure functions using F#"

images:
  - /blogs/what-the-fixing-weirdness-in-return-json-from-azure-functions-using-f/banner.png
featured_image: banner.png
---


I've been playing a lot with [F#](https://docs.microsoft.com/en-us/dotnet/fsharp/?WT.mc_id=fsharp-blog-jabenn) recently, both to build Xamarin apps using [Elmish.XamarinForms](https://github.com/fsprojects/Elmish.XamarinForms) and for some [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-fsharp/?WT.mc_id=fsharp-blog-jabenn). Whilst building an HTTP trigger I came across some weirdness when serializing a record type to JSON.

This is the relevant parts of my code:

```
type Output = { TotalBalance : float }

let Run(req: HttpRequestMessage, boundTable: IQueryable<Transaction>, log: TraceWriter) =
    async {
        // stuff
        return req.CreateResponse(HttpStatusCode.OK, { TotalBalance = sum })
    } |> Async.RunSynchronously
```

Now it's normal to assume the `Output` type would be serialized to JSON correctly, leading to something like:

```json
{
  "balance" : 100
}
```

Unfortunately not - what I actually get is:

```json
{
  "Balance@" : 100
}
```

Note the weird __@__ symbol on the property name.

So I went spelunking around Google and SO for a fix. The first suggestion was to add the `[<CLIMutable>]` attribute to my `Output` type, but this didn't actually work, the __@__ symbol was still there.

In the end I found the fix here: https://stackoverflow.com/questions/43118406/return-an-f-record-type-as-json-in-azure-functions/48718297#48718297. You can pass a different JSON formatter to the `CreateResponse` call, and configure that to return the correct property names:

```
let jsonFormatter = Formatting.JsonMediaTypeFormatter()
jsonFormatter.SerializerSettings.ContractResolver <- CamelCasePropertyNamesContractResolver()

return req.CreateResponse(HttpStatusCode.OK, { TotalBalance = sum }, jsonFormatter)
```

Done!

