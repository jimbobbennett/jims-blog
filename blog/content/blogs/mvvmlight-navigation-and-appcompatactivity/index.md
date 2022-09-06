---
author: "Jim Bennett"
categories: ["xamarin", "xamarin.android", "mvvmlight", "AppCompat", "nuget", "Technology"]
date: 2016-02-08T00:16:50Z
description: ""
draft: false
slug: "mvvmlight-navigation-and-appcompatactivity"
tags: ["xamarin", "xamarin.android", "mvvmlight", "AppCompat", "nuget", "Technology"]
title: "MVVMLight navigation and AppCompatActivity"

images:
  - /blogs/mvvmlight-navigation-and-appcompatactivity/banner.png
featured_image: banner.png
---


As much as I'm loving [MVVMLight](http://mvvmlight.codeplex.com) it does have some limitations.  The one I've hit recently is how well it doesn't work when you are using AppCompat (though to be honest I think it's more down to how hacky AppCompat seems to be).

I'm using [AppCompatActivity](http://developer.android.com/reference/android/support/v7/app/AppCompatActivity.html) as my base activity class to get an action bar supported on older API versions.  The problem is MVVMLight implements it's own `ActivityBase` which is derived from `Activity`, and it relies on a set of static methods and properties on this to handle things like navigation and dialogs.  If you want to use `AppCompatActivity` you are stuck - navigation will not work.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Seems to get <a href="https://twitter.com/hashtag/mvvmlight?src=hash">#mvvmlight</a> working with AppCompatActivity I have to write my own NavigationService. <a href="https://twitter.com/LBugnion">@LBugnion</a> any thoughts?</p>&mdash; Jim Bennett (@jimbobbennett) <a href="https://twitter.com/jimbobbennett/status/696149246022520833">February 7, 2016</a></blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/jimbobbennett">@jimbobbennett</a> I don&#39;t have a better proposal at this point. Android is severely broken when it comes to launching new activities.</p>&mdash; Laurent Bugnion (@LBugnion) <a href="https://twitter.com/LBugnion/status/696273172937760769">February 7, 2016</a></blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Luckily MVVMLight is really well designed with good separation of concerns, so everything is done via interface.  This means we can write our own implementation of the navigation service and dialog service that will work with `AppCompatActivity` and use it in our code.  Being open source as well we can take the existing source and tweak it slightly to make it work for us.  It's a bit of a hack but it works.

The first thing to do is to define our own base activity class that has the same functionality as the `ActivityBase`, but derived from `AppCompatActivity`.

```
using Android.Support.V7.App;

namespace JimBobBennett.MvvmLight.AppCompat
{
    public abstract class AppCompatActivityBase : AppCompatActivity
    {
        public static AppCompatActivityBase CurrentActivity { get; private set; }

        internal string ActivityKey { get; private set; }

        internal static string NextPageKey { get; set; }
        
        public static void GoBack()
        {
            CurrentActivity?.OnBackPressed();
        }
        
        protected override void OnResume()
        {
            CurrentActivity = this;
            if (string.IsNullOrEmpty(ActivityKey))
            {
                ActivityKey = NextPageKey;
                NextPageKey = null;
            }
            base.OnResume();
        }
    }
}
```

This is identical to the MVVMLight `ActivityBase` except the base class is `AppCompatActivity`.

Now we have our base activity we can use it for the navigation service.  This is identical to the MVVMLight Android `NavigationService` except instead of accessing the statics on `AppCompatActivityBase` instead of on `ActivityBase`.

```
using System;
using System.Collections.Generic;
using Android.Content;
using GalaSoft.MvvmLight.Views;

namespace JimBobBennett.MvvmLight.AppCompat
{
    public class AppCompatNavigationService : INavigationService
    {
        private readonly Dictionary<string, Type> _pagesByKey = new Dictionary<string, Type>();
        private readonly Dictionary<string, object> _parametersByKey = new Dictionary<string, object>();

        private const string RootPageKey = "-- ROOT --";
        private const string ParameterKeyName = "ParameterKey";
        
        public string CurrentPageKey => AppCompatActivityBase.CurrentActivity.ActivityKey ?? RootPageKey;
        
        public void GoBack()
        {
            AppCompatActivityBase.GoBack();
        }
        
        public void NavigateTo(string pageKey)
        {
            NavigateTo(pageKey, null);
        }
        
        public void NavigateTo(string pageKey, object parameter)
        {
            AppCompatActivityBase.CurrentActivity.RunOnUiThread(() =>
            {
                if (AppCompatActivityBase.CurrentActivity == null)
                    throw new InvalidOperationException("No CurrentActivity found");

                lock (_pagesByKey)
                {
                    if (!_pagesByKey.ContainsKey(pageKey))
                        throw new ArgumentException($"No such page: {pageKey}. Did you forget to call NavigationService.Configure?", nameof(pageKey));

                    var intent = new Intent(AppCompatActivityBase.CurrentActivity, _pagesByKey[pageKey]);
                    if (parameter != null)
                    {
                        lock (_parametersByKey)
                        {
                            var guid = Guid.NewGuid().ToString();
                            _parametersByKey.Add(guid, parameter);
                            intent.PutExtra(ParameterKeyName, guid);
                        }
                    }

                    AppCompatActivityBase.CurrentActivity.StartActivity(intent);
                    AppCompatActivityBase.NextPageKey = pageKey;
                }
            });
        }

        public void Configure(string key, Type activityType)
        {
            lock (_pagesByKey)
            {
                if (_pagesByKey.ContainsKey(key))
                    _pagesByKey[key] = activityType;
                else
                    _pagesByKey.Add(key, activityType);
            }
        }

        public object GetAndRemoveParameter(Intent intent)
        {
            if (intent == null)
                throw new ArgumentNullException(nameof(intent), "This method must be called with a valid Activity intent");

            var stringExtra = intent.GetStringExtra(ParameterKeyName);
            if (string.IsNullOrEmpty(stringExtra))
                return null;

            lock (_parametersByKey)
                return _parametersByKey.ContainsKey(stringExtra) ? _parametersByKey[stringExtra] : null;
        }
        
        public T GetAndRemoveParameter<T>(Intent intent)
        {
            return (T)GetAndRemoveParameter(intent);
        }
    }
}
```

We then do the same for the dialog service:

```
using System;
using System.Threading.Tasks;
using Android.App;
using Android.Content;
using GalaSoft.MvvmLight.Views;

namespace JimBobBennett.MvvmLight.AppCompat
{
    public class AppCompatDialogService : IDialogService
    {
        public Task ShowError(string message, string title, string buttonText, Action afterHideCallback)
        {
            var afterHideCallbackWithResponse = (Action<bool>) (r =>
            {
                if (afterHideCallback == null)
                    return;
                afterHideCallback();
                afterHideCallback = null;
            });

            var dialog = CreateDialog(message, title, buttonText, null, afterHideCallbackWithResponse);
            dialog.Dialog.Show();
            return dialog.Tcs.Task;
        }

        public Task ShowError(Exception error, string title, string buttonText, Action afterHideCallback)
        {
            var afterHideCallbackWithResponse = (Action<bool>)(r =>
            {
                if (afterHideCallback == null)
                    return;
                afterHideCallback();
                afterHideCallback = null;
            });

            var dialog = CreateDialog(error.Message, title, buttonText, null, afterHideCallbackWithResponse);
            dialog.Dialog.Show();
            return dialog.Tcs.Task;
        }
        
        public Task ShowMessage(string message, string title)
        {
            var dialog = CreateDialog(message, title);
            dialog.Dialog.Show();
            return dialog.Tcs.Task;
        }
        
        public Task ShowMessage(string message, string title, string buttonText, Action afterHideCallback)
        {
            var afterHideCallbackWithResponse = (Action<bool>)(r =>
            {
                if (afterHideCallback == null)
                    return;
                afterHideCallback();
                afterHideCallback = null;
            });

            var dialog = CreateDialog(message, title, buttonText, null, afterHideCallbackWithResponse);
            dialog.Dialog.Show();
            return dialog.Tcs.Task;
        }
        
        public Task<bool> ShowMessage(string message, string title, string buttonConfirmText, string buttonCancelText, Action<bool> afterHideCallback)
        {
            var afterHideCallbackWithResponse = (Action<bool>)(r =>
            {
                if (afterHideCallback == null)
                    return;
                afterHideCallback(r);
                afterHideCallback = null;
            });

            var dialog = CreateDialog(message, title, buttonConfirmText, buttonCancelText ?? "Cancel", afterHideCallbackWithResponse);
            dialog.Dialog.Show();
            return dialog.Tcs.Task;
        }
        
        public Task ShowMessageBox(string message, string title)
        {
            return ShowMessage(message, title);
        }

        private static AlertDialogInfo CreateDialog(string content, string title, string okText = null, string cancelText = null, Action<bool> afterHideCallbackWithResponse = null)
        {
            var tcs = new TaskCompletionSource<bool>();
            var builder = new AlertDialog.Builder(AppCompatActivityBase.CurrentActivity);
            builder.SetMessage(content);
            builder.SetTitle(title);
            var dialog = (AlertDialog)null;
            builder.SetPositiveButton(okText ?? "OK", (d, index) =>
            {
                tcs.TrySetResult(true);
                if (dialog != null)
                {
                    dialog.Dismiss();
                    dialog.Dispose();
                }
                if (afterHideCallbackWithResponse == null)
                    return;
                afterHideCallbackWithResponse(true);
            });

            if (cancelText != null)
            {
                builder.SetNegativeButton(cancelText, (d, index) =>
                {
                    tcs.TrySetResult(false);
                    if (dialog != null)
                    {
                        dialog.Dismiss();
                        dialog.Dispose();
                    }
                    if (afterHideCallbackWithResponse == null)
                        return;
                    afterHideCallbackWithResponse(false);
                });
            }

            builder.SetOnDismissListener(new OnDismissListener(() =>
            {
                tcs.TrySetResult(false);
                if (afterHideCallbackWithResponse == null)
                    return;
                afterHideCallbackWithResponse(false);
            }));

            dialog = builder.Create();

            return new AlertDialogInfo
            {
                Dialog = dialog,
                Tcs = tcs
            };
        }

        private struct AlertDialogInfo
        {
            public AlertDialog Dialog;
            public TaskCompletionSource<bool> Tcs;
        }

        private sealed class OnDismissListener : Java.Lang.Object, IDialogInterfaceOnDismissListener
        {
            private readonly Action _action;

            public OnDismissListener(Action action)
            {
                _action = action;
            }

            public void OnDismiss(IDialogInterface dialog)
            {
                _action();
            }
        }
    }
}
```

To use these all we need to do is derive all our activities from `AppCompatActivityBase` and register the `AppCompatNavigationService` and `AppCompatDialogService` in our IoC container as implementations of `INavigationService` and `IDialogService`.

The code for this is up on GitHub here: https://github.com/jimbobbennett/JimBobBennett.MvvmLight.AppCompat

I've also created a NuGet package available here: https://www.nuget.org/packages/JimBobBennett.MvvmLight.AppCompat/ or searchable from the Package Manager as `JimBobBennett.MvvmLight.AppCompat`.

<hr/>

#### Update
Thanks to [Samuel Debruyn](http://sa.muel.be) for adding an update to this package.  

MVVMLight has a helper class to aid in running code on the UI thread called [DispatcherHelper](http://www.mvvmlight.net/help/SL5/html/5af6dede-4a22-2eb2-d0fa-5af0f2fe4fe5.htm).  This will verify the current activity and use that to run the specified action on the UI thread using the `RunOnUIThread` method.

Unfortunately for us this relies on the `CurrentActivity` property on `ActivityBase`, something we are not using.  Sam has added an `AppCompatDispatcherHelper` which mimics the logic of the `DispatcherHelper` but using the `AppCompatActivityBase.CurrentActivity` instead.

The [code on GitHub](https://github.com/jimbobbennett/JimBobBennett.MvvmLight.AppCompat) and [NuGet package](https://www.nuget.org/packages/JimBobBennett.MvvmLight.AppCompat/) have both been updated with these changes.

