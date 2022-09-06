---
author: "Jim Bennett"
categories: ["Technology", "jimlib.xamarin", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "extendedentry", "renderer", "control", "xamarin.forms.labs"]
date: 2014-08-27T05:02:19Z
description: ""
draft: false
slug: "setting-the-font-for-an-entry-control-using-xamarin-forms-2"
tags: ["Technology", "jimlib.xamarin", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "extendedentry", "renderer", "control", "xamarin.forms.labs"]
title: "Setting the font for an Entry control using Xamarin.Forms"

images:
  - /blogs/setting-the-font-for-an-entry-control-using-xamarin-forms-2/banner.png
featured_image: banner.png
---


[Xamarin.Forms](http://xamarin.com/forms) depsite being very cool is stil a bit lacking when it comes to not only a good range of controls, but also to the abilities of those controls.
One example of this is the Entry control - a simple text box.  One thing you can't do with the out of the box implementation is to set the Font.  Such a normal thing to do, but not supported.

Luckily, it's reasonably easy to roll your own controls.
Due to the platform independent nature of Xamarin.Forms, to create a control you have to actually create 2 pieces - a portable control, then platform specific renderers to draw the control on each device.  I don't have an android subscription, and can't be bothered with WinPhone at the moment, so will only be showing how to do this for iOS.

First, we need the control inside a portable project.  These can be derived from an existing control - here we derive from Entry as we want to extend its functionality.

```
public class ExtendedEntry : Entry
{
}
```

Then we add the bindable properties.  These are Xamarins version of dependency properties - they have a static field declaring the property then an instance property to get/set the value.

```
public class ExtendedEntry : Entry
{
	public static readonly BindableProperty FontProperty =
            BindableProperty.Create("Font", typeof(Font), 	
            typeof(ExtendedEntry), new Font());
            
    public Font Font
    {
        get { return (Font)GetValue(FontProperty); }
        set { SetValue(FontProperty, value); }
    }
}
```

This is all we need for our control.  Next up is the renderer.  This wraps platform specific controls to provide the necessary functionality.
In the case of the Entry control on iOS, the UITextField control is wrapped.  To set our font we need to pass the value from the control to the UITextField in the renderer.

First we create our renderer deriving from the existing entry renderer:

```
public class ExtendedEntryRenderer : EntryRenderer
{
}
```

The we override a few methods - `OnElementChanged` to handle the creation of the control and `OnElementPropertyChanged` to handle any updates to the properties on the control.  In these methods we need to set the font on the UITextView.  The Control property of the renderer refers to the underlying UITExtField, the Element property is the ExtendedEntry control.

```
public class ExtendedEntryRenderer : EntryRenderer
{
    protected override void OnElementChanged(ElementChangedEventArgs<Entry> e)
    {
        base.OnElementChanged(e);
        var view = (Labs.Controls.ExtendedEntry)Element;
        SetFont(view);
    }

    protected override void OnElementPropertyChanged(object sender, PropertyChangedEventArgs e)
    {
        base.OnElementPropertyChanged(sender, e);

        var view = (Labs.Controls.ExtendedEntry)Element;

        if (string.IsNullOrEmpty(e.PropertyName) || 
            e.PropertyName == "Font")
            SetFont(view);
    }

    private void SetFont(Labs.Controls.ExtendedEntry view)
    {
        UIFont uiFont;
        if (view.Font != Font.Default && 
            (uiFont = view.Font.ToUIFont()) != null)
            Control.Font = uiFont;
        else if (view.Font == Font.Default)
            Control.Font = UIFont.SystemFontOfSize(17f);
    }
}
```

As you can we, the Xamarin.Forms Font class provides a nice converter to UIFont to make our life easier, and if the font is not supported we resort to a default system font and size.  For the property change we just update the font if the property that changes is the font, or if a property change is raised for an empty string - this saves updating when not required and the empty string check is because raising with an empty string as the property name is the way to say all properties have been updated.

If we keep it like this, then the font is changed, but there is a bug - the height of the control doesn't change to match the height of the font, we make the font larger and the top/bottom of the text is missing.  The final step is to set the height.  Luckily UITextField will work out the required height based on the font that is set, so we can create a dummy UITextField, set it's font, get the required height and apply it to both our control and the UITextField hosted in it:

```
private void ResizeHeight()
{
    if (Element.HeightRequest >= 0) return;

    var height = Math.Max(Bounds.Height,
        new UITextField 
        {
            Font = Control.Font
        }.IntrinsicContentSize.Height);

    Control.Frame = new RectangleF(0.0f, 
                                   0.0f, 
                                   (float) Element.Width, 
                                   height);

    Element.HeightRequest = height;
}
```

This method uses the HeightRequest property of the Entry control to request a large/smaller height as necessary.  This causes the layout to adjust the size to fit if possible.  If the HeightRequest is already set (it is -1 if not set), then we do nothing as the user has already decided on what height is needed.  All we need to do is just call this after setting the font and everything now works.


The full source for EnhancedEntry including other properties is available as part of [JimLIb.Xamarin](https://github.com/jimbobbennett/JimLib.Xamarin).  I've also raised a PR to add this to [Xamarin.Forms.Labs](https://github.com/XForms/Xamarin-Forms-Labs).

