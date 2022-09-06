---
author: "Jim Bennett"
categories: ["technology", ".net", "docs", "c#"]
date: 2019-06-04T10:27:34Z
description: ""
draft: false
images:
  - /blogs/trying-out-try-net/banner.png
featured_image: banner.png
slug: "trying-out-try-net"
tags: ["technology", ".net", "docs", "c#"]
title: "Trying out Try .NET"

images:
  - /blogs/trying-out-try-net/banner.png
featured_image: banner.png
---


[Try .NET](https://github.com/dotnet/try?WT.mc_id=trydotnet-blog-jabenn) is a new thing to come from the .NET teams that allows you to, well, try .NET. In a browser. You can think of it as a way to create interactive .NET documentation using .NET Core.

## What is Try .NET

The experience or writing code in a browser itself isn't new, developers have been able to try out C# coding snippets [in the browser](https://dotnet.microsoft.com/learn/dotnet/in-browser-tutorial/1/?WT.mc_id=trydotnet-blog-jabenn) for a while but this is different. Try .NET is different, as it allows you to:

* Mix code and markdown which then gets run as a web page where you can read the markdown and edit and run the code in place
* Create projects with code, NuGet package dependencies, whatever is needed, then only surface the bits you want people to focus on

> Note - Try .NET only supports C# at the moment, but F# is the most requested enhancement, obviously.

### Mix code and markdown

Imagine you wanted to create a tutorial project to show how to do something in C#. In the past, you would write the instructions and provide code snippets for the reader to run by creating a project, then adding the code to a `.cs` file in that project, then running it from the command line.

With Try .NET, you can create a markdown file that links to a piece of code in an existing project. The reader can then run that code from inside the browser. They can also edit the code with full intellisense, get compiler errors if something isn't write and generally play with the code.

{{< figure src="TryDotNetRunMarkdownAndCode.png" >}}

### Only surface what you need

When running code, you normally need some boiler plate stuff - a `main` method, some `using` directives, that sort of thing. If you want to run more advanced code that relies on external packages or setup code you need a way to bring those packages in or run the setup code. This can be complex, and fill up the code window with code that really isn't relevant to what you want to teach.

Try .NET fixes this by having a C# project behind the scenes that you can set up how you want. You then write all the code you need, then surface just the bit you want to show in the markdown using `#region` directives - yup, finally a good reason for them.

## Creating your first Try .NET project

Try .NET is a global .NET tool, and you can install it from a terminal or command line using:

```sh
dotnet tool install --global dotnet-try
```

It supports .NET Core 2.1, but for all the best stuff it's worth [installing 3.0](https://dotnet.microsoft.com/download/dotnet-core/3.0/?WT.mc_id=trydotnet-blog-jabenn).

You can spin up a demo project using:

```sh
dotnet try demo
```

but I thought it would be fun to walk through creating a project from scratch and go through how it all runs.

### Create a dotnet project

Start with a simple dotnet console app:

```sh
dotnet new console -o TryDotNetDemo
```

In my case I've called my app `TryDotNetDemo`. Open this project in [Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=trydotnet-blog-jabenn), then add a new file to the project called `README.MD`. This is a standard read me markdown file, the same as you would use in GitHub.

Add some markdown to this file to display a simple header and intro:

```markdown
# A try .NET demo

This is a demo of Try .NET.

Run the code below to see some code being run.

```

From the Visual Studio Code terminal run the following:

```sh
dotnet try
```

Your code will be compiled, and launched in a browser where you will see your markdown rendered.

{{< figure src="TryDotNetFirstRun-1.png" >}}

### Add some code

Now we have some markdown, lets add some code. A simple _Hello World_ will do for now.

Open the `Program.cs` file. The default `main` method will have a single line to write `Hello World` to the console.

```cs
using System;

namespace TryDotNetDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }
}
```

We want the `Console.WriteLine` call in the markdown, but not the rest of the code, so what do we do?

Well we add a region! Wrap the line in a named region block, using a name that makes sense.

```cs
# region HelloWorld
Console.WriteLine("Hello World!");
# endregion HelloWorld
```

Next, add an empty code block to your markdown:

```markdown
```cs --region HelloWorld --source-file .\Program.cs --project .\TryDotNetDemo.csproj
```
```

Lets break this markdown block down:

```markdown
``` cs
```
```

These are the open and closing sections of the code block, shown by three back ticks. The closing set of three back ticks needs to be on a new line. The `cs` part tells the markdown renderer that the code in this block is C# code.

```markdown
--region HelloWorld
```

This tells Try .NET to look for a region called `HelloWorld` and put all the code inside this region into the rendered markdown.

```markdown
--source-file .\Program.cs
```

This tells Try .NET to look for this region in the `Program.cs` code file.

```markdown
--project .\TryDotNetDemo.csproj
```

This final option tells Try .NET that the code comes from the `TryDotNetDemo.csproj` file, so this project needs to be compiled and run.

Kill the running session in the Visual Studio Code terminal if it is still running, and relaunch it.

```sh
dotnet try
```

You will now see your code in the browser, and you can run it using the purple run button.

{{< figure src="TryDotNetFirstRunWithCode.png" >}}

This is cool - but what's even cooler is you can edit this code. Have a play - you get full intellisense and _ctrl+space_ autocomplete, and if your code doesn't compile you get proper compiler errors - with line numbers based off the code in the browser, not in the `.cs` file.

{{< figure src="TryDotNetRunMarkdownAndCodeAndError.png" >}}

### What's happening

When your code runs, it will compile the console app with any code changes you've made included. If it fails to compile, you see the errors, otherwise the console app runs as normal - the `main` method is run and any output to the console is shown below your code.

## Creating a more advanced project

This first example runs one bit of code, but what if you wanted to have multiple methods that can be edited, for example in a multi part or multi page tutorial? How would that work as the `main` method is run every time?

The answer comes in the form of command line parameters. When Try .NET runs your console app, it passes  the region name, source file and project file as command line parameters to the app. To see this in action you can dump the parameters to the console and relaunch the code.-

```cs
Console.WriteLine(string.Join(' ', args));
```

{{< figure src="TryNetCommandLIneParams.png" >}}

You will see 6 parameters:

```sh
--region HelloWorld --source-file .\Program.cs --project .\TryDotNetDemo.csproj

```

These are the additional parameters added to the `cs` code block in the markdown.

You can use these to direct your code. A good pattern is to switch on the region in your `main` method, then call a different method.

```cs
static void Main(string[] args)
{
    switch (args[1])
    {
        case "HelloWorld":
            HelloWorld();
            break;
        case "Addition":
            Addition();
            break;
    }
}

static void HelloWorld()
{
    #region HelloWorld
    Console.WriteLine("Hello World!");
    #endregion HelloWorld
}

static void Addition()
{
    #region Addition
    int a = 1;
    int b = 2;
    int c = a + b;
    Console.WriteLine($"{a} + {b} = {c}");
    #endregion Addition
}
```

You can then surface both methods in the markdown:

```markdown
# A try .NET demo

This is a demo of Try .NET.

Run the code below to see some code being run.

```cs --region HelloWorld --source-file .\Program.cs --project .\TryDotNetDemo.csproj
```

The code below shows addition:

```cs --region Addition --source-file .\Program.cs --project .\TryDotNetDemo.csproj
```
```

When the `HelloWorld` region is run, the console app is called and `"HelloWorld"` is passed as the second argument to the app (the first argument is the `--region` parameter). The `switch` statement in the `main` method picks this up and runs the `HelloWorld` method only. Similarly the `Addition` region passes `"Addition"` to the app, and only the `Addition` method is run.

This allows you to break your app down into many methods that can be called in isolation inside your markdown.

## What about adding packages?

This is totally supported! Just add the package to your C# project as normal and use it in your code.

```cs
static void Json()
{
    #region Json
    var x = new { name = "Try .NET", status = "Awesome" };
    var json = JsonConvert.SerializeObject(x);
    Console.WriteLine(json);
    #endregion Json
}
```

```markdown
The code below shows some JSON handling with Newtonsoft JSON:

```cs --region Json --source-file .\Program.cs --project .\TryDotNetDemo.csproj
```
```

When you run this code in the browser it will use `Newtonsoft.Json.JsonConvert` to serialize an anonymous object to a string. You even get full intellisense for this package in the editor.

{{< figure src="JsonHandling.png" >}}

---

All the code for this is available on GitHub here - [github.com/jimbobbennett/TryDotNetDemo](https://github.com/jimbobbennett/TryDotNetDemo).

You can also read more on the [.NET blog](https://devblogs.microsoft.com/dotnet/creating-interactive-net-documentation/?WT.mc_id=trydotnet-blog-jabenn).

