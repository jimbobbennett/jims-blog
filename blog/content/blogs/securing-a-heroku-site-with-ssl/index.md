---
author: "Jim Bennett"
categories: ["Technology", "moomoo.io", "heroku", "technology", "node", "ssl", "dnsimple"]
date: 2014-08-16T10:12:53Z
description: ""
draft: false
slug: "securing-a-heroku-site-with-ssl"
tags: ["Technology", "moomoo.io", "heroku", "technology", "node", "ssl", "dnsimple"]
title: "Securing a Heroku site with SSL"

images:
  - /blogs/securing-a-heroku-site-with-ssl/banner.png
featured_image: banner.png
---


For my mobile app development work, I've been building a Node.js website with a REST api that my apps can use.  It's hosted at [MooMoo.io](https://www.moomoo.io) and is running using a free [Heroku](https://www.heroku.com/) account - I don't have anything useful on my site or many users of my API at the moment, so their free single dyno is perfect for my needs.  I'm also taking advantage of the free sandbox MongoDB account from [MongoLab](http://mongolab.com/).  It's pretty cool just how much I can get for free, and I only need to pay if my apps take off and I start making money.

One thing I did have to pay for though is SSL.  For my API I don't want unencrypted connections, so the easiest thing to do is to access it only over HTTPS.  It took me a while to get it all set up, so I thought it would be usefull to document the steps in case anyone else is doing the same thing.

First, you need an SSL certificate.  My domains are currently with [DNSimple](http://DNSimple.com), a great company that tries to be simple and honest and not full of the crap that [other sites](http://www.godaddy.com) have.  Assuming you have a DNSimple account holding your domains (and if not, transfer them already!), it's simple to get a certificate from RapidSSL with one click and $20.  All it takes is an approver with an email address that matches your URL (google apps provides 30 days free trial if you don't have email set up) and you get the certificate.
Once you have the certificate, you can view it and the private key on DNSimple - and copy them into 2 files, server.crt for the certificate and server.key for the private key.
For RapidSSL you do need an additional certificate downloaded from their site, but this is easy to get with curl:
```
curl https://knowledge.rapidssl.com/library/VERISIGN/INTERNATIONAL_AFFILIATES/RapidSSL/AR1548/RapidSSLCABundle.txt > bundle.pem
```

Next, upload the keys to Heroku.  You need to enable the [SSL Endpoint add-on](http://addons.heroku.com/ssl) - **This is not free** - it's $20 a month so it's not cheap.
To upload, use the Heroku toolbelt:
```
heroku certs:add server.crt bundle.pem server.key --app <your app name>
```

This will then change the url to your app, so you'll need to update the CNAME record for your custom domain if you are using one to point to the new url.  The output of the `certs:add` command will show the new url:

```
Resolving trust chain... done
Adding SSL Endpoint to <your app name>... done
<your app name> now served by <something>.herokussl.com
Certificate details:
...
```

Heroku implements HTTPS in an interesting way - the connection to Heroku is encrypted and converted to a raw HTTP request that is forwarded to your app.  This means that your app doesn't need to handle HTTPS, just HTTP which makes it easier to develop.  The downside is Heroku has access to the unencrypted data, but with any cloud provider there has to be trust.

The last step if you want to do it is to redirect from HTTP to HTTPS.  Normally you could use `req.secure` in Node to identify secure requests, but this doesn't work with Heroku as all requests to your app are unencrypted HTTP.  Luckily, Heroku adds some custom headers to the request that allows you to identify if the original url was HTTP or HTTPS.  `x-forwarded-proto` is used to indicate the protocol that was used for the request that was forwarded to your app.  If this is set to `https`, you know the request was from HTTPS.  If not, you can redirect:

```
if (env != 'development') // only redirect in prod
{
    app.use(function(req, res, next)
    {
        if (req.headers['x-forwarded-proto'] != 'https')
            res.redirect(['https://', req.get('Host'), req.url].join(''));
        else
            next();
    });
}
```

To see this in action, head to http://www.moomoo.io, and you'll be redirected to https://www.moomoo.io.

