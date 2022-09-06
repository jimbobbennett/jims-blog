---
author: "Jim Bennett"
categories: ["xamarin", "Technology", ".NET Core", "dotnet new", "templates"]
date: 2017-10-25T06:42:53Z
description: ""
draft: false
slug: "creating-dotnet-new-and-visual-studio-project-and-solution-templates"
tags: ["xamarin", "Technology", ".NET Core", "dotnet new", "templates"]
title: "Creating Visual Studio project and solution templates - Part 1, dotnet new"

images:
  - /blogs/creating-dotnet-new-and-visual-studio-project-and-solution-templates/banner.png
featured_image: banner.png
---


I've recently updated my [MvvmCross templates](https://github.com/jimbobbennett/MvvmCross-Templates) to support .NET Standard to be ready for the awesome future. Unfortunately this meant a complete rewrite of my templates as the out of the box Visual Studio project template extensions on both Windows and Mac don't support .NET Standard. As it turned out though, this rewrite was a blessing in disguise as there is a new way to do templates, and this can be used with the `dotnet` cli as well as inside extensions for VS on Windows and Mac, meaning I can now create one template and use it on all platforms.

This post shows how to create templates for the .NET cli, and in the next two posts these templates will be ported to Visual Studio, first Windows then Mac.

#### dotnet new
As part of the new .NET Core awesomeness, there is a new cli for .NET. You can install this manually from https://www.microsoft.com/net/core, otherwise you can install it with Visual Studio.

Once you have the .NET cli installed you can use the command line to create new apps based off templates using `dotnet new <template name>`. Some templates come pre-installed, and you can download and install others to provide any kind of project your heart desires. This post is not going to cover the cli, you can read up on that from the previous link, instead we are going to look at creating templates.

#### dotnet new templates
The templates used by `dotnet new` are actually really simple - they are fully working projects or solutions with a config file. If you've ever created a project or solution extension for Visual Studio you've probably had the fun of creating a project then changing namespaces and project references to be `$ProjectName` or other such replacement tokens. These projects then cannot be run, so to change them you have to change the code, build the extension, create a project, find problems, rinse and repeat.  With dotnet new templates you don't have to do this.

###### Step 1 - create a project
The first thing to do is a create a project or solution that you want to create the template from. Add the relevant NuGet packages, add classes, resources, whatever you need. This is a normal project, the same you use every day so you can run it at any time for testing.

###### Step 2 - create a template.config file
At the root of your project or solution, create a folder called `.template.config` and add a json file called `template.json` to that folder. This file defines the structure of the template, including providing a base namespace that you used in your project. When a new project is created using your template, all the files in your source project will be used, with the namespace changed to the namespace passed to dotnet new. 

For example if your project had the namespace `MvvmCrossApp`, you set this in the `template.json` file. If the end user tells dotnet new to use the namespace `Foo`, any occurrences of `MvvmCrossApp` in source files or project files will be replaced with `Foo` automatically - no need to use replacement tokens.

You can read about all the fields in this file at https://blogs.msdn.microsoft.com/dotnet/2017/04/02/how-to-create-your-own-templates-for-dotnet-new/. You can also install an extension to Visual Studio for Windows called [Sidewaffle Creator](https://marketplace.visualstudio.com/items?itemName=Sayed-Ibrahim-Hashimi.SidewaffleCreator2017) that has a wizard to help create these files.

###### Step 3 - create a NuGet package
These templates are packaged as NuGet packages, so you will need to create a `.nuspec` and package up your files. This NuSpec needs to have the usual id, description, version, as well a package type of template set in the metadata. All the source files for your project need to be added as files. You can see an example I use for my MvvmCross templates below:

```
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2012/06/nuspec.xsd">
  <metadata>
    <id>MvvmCross.Templates.CSharp.Native.SinglePage.iOS.Android</id>
    <version>1.0.0</version>
    <description>
      Creates an example single page MvvmCross app for iOS, Android, UWP and WPF.
    </description>
    <authors>Jim Bennett</authors>
    <packageTypes>
      <packageType name="Template" />
    </packageTypes>
  </metadata>
  <files>
    <file src=".\MvvmCrossNativeSinglePage\**" target="content" exclude=".\MvvmCrossNativeSinglePage\packages\**;.\MvvmCrossNativeSinglePage\*.UWP\**;.\MvvmCrossNativeSinglePage\*.WPF\**;.\MvvmCrossNativeSinglePage\.template.config\template.json;**\bin\**;**\obj\**;**\.vs\**;**\*.user;"/>
    <file src=".\MVVMCross.XSAddIn\MvvmCrossNativeSinglePage.template.json" target="content\.template.config\template.json"/>
  </files>
</package>
```

This is packaged up using the NuGet command line to give a standard NuGet package.

###### Step 4 - install the template

Templates can be installed in one of two ways. To test locally, you can install using:

```
dotnet new --install <path_to_nuget_package>
```

Then if you run `dotnet new` you should see your template in the list of available templates. You can then create a new project or solution using your template by using:

```
dotnet new <template_short_name> -o <output_folder_and_namespace_name>
```

###### Step 5 - distribute the template

Once you've verified locally, you can upload your NuGet package to [NuGet.org](https://NuGet.org). From there anyone can install your template using:

```
dotnet new --install <NuGet_package_id>
```

You can see an example of this for my MvvmCross templates at https://github.com/jimbobbennett/MvvmCross-Templates

<hr/>

In the next post we'll look at using this template inside a Visual Studio for Windows extension.

