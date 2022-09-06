---
author: "Jim Bennett"
categories: ["Technology", "javascript", "moomoo.io", "technology", "node", "css", "minify", "performance"]
date: 2014-09-13T10:52:26Z
description: ""
draft: false
slug: "performance-tuning-a-website"
tags: ["Technology", "javascript", "moomoo.io", "technology", "node", "css", "minify", "performance"]
title: "Performance tuning a website"

images:
  - /blogs/performance-tuning-a-website/banner.png
featured_image: banner.png
---


Despite the rise in fast home broadband, tuning your website for performance is still just as important as it was in the days of dial up.  Although home connections can be fast in most first world countries (I used to have a 1Gb connection in Hong Kong), there are stil a lot of people in developing countries who only have slower speeds, as well as a huge increase in mobile users who have either limited speed or usage caps (or in my current case, are in a country whose main cables have been cut by a typhoon so the internet is now at dial up speeds until they fix it in a weeks time).

Today as part of working on [MooMoo.io](https://www.moomoo.io) I decided to have a look at the performance and see what I could do to improve it.
Profiling is important to see what can be improved, but there are some tricks that apply to all websites that should be done as a matter of course.  The basic principle is to reduce the amount of data sent over the wire and the number of requests made.

### Minification
[Minification](http://en.wikipedia.org/wiki/Minification_%28programming%29) is the act of taking js or css files and reducing their size - removing comments, white space and other unnecessary characters, renaming variables to smaller  names, that sort of thing.  The downside to this is it makes the code unreadable, so the normal process is to write JavaScript or CSS normally, then create a minified version (usually named <filename>.min.js) as part of a build step.  A lot of third party libraries will already provide minified versions of their code, so in general you should always use these where available.

For MooMoo.io I decided to add some code to my Node.js server to automatically minify my CSS and js files during startup, then change my HTML to refer to the minified versions.  This means I can develop using the full versions and they are converted when needed.  At the same time, I will concatenate all my js files into one.  This means the browser only has to make one server request to load all js code instead of one request per file, reducing the bandwidth used.

**CSS**

For CSS minification, I am using [minifier](https://www.npmjs.org/package/minifier).
```
$ npm install minifier --save
```

In my code I already use compass to compile SASS giving me one css file, so I just need to minify that one.

```js
var minifier = require('minifier');
  
minifier.minify(__dirname + '/public/stylesheets/site.css', {})
```

This will spit out `/public/stylesheets/site.min.css`.  One quick change to my HTML head code and it's using the minified version.

**js**

For js minification, I am using [uglify-js](https://www.npmjs.org/package/uglify-js).
```
$ npm install uglify-js --save
```

This can take multiple js files and spit out minified code, which can then be saved to a file.

```js
var fs = require('fs');
var uglify = require("uglify-js");

var jsFiles = [
  __dirname + '/../public/vendor/jquery/dist/jquery.min.js',
  __dirname + '/../public/vendor/foundation/js/vendor/fastclick.js',
  __dirname + '/../public/vendor/foundation/js/foundation.min.js',
  __dirname + '/../public/vendor/angular/angular.min.js',
  __dirname + '/../public/vendor/angular-resource/angular-resource.min.js',
  __dirname + '/../public/vendor/angular-route/angular-route.min.js'
];

var uglified = uglify.minify(jsFiles);

fs.writeFile(__dirname + '/public/js/concat.min.js', uglified.code, function (err){
  if(err) {
    console.log(err);
  } else {
    console.log("Script generated and saved:", 'concat.min.js');
  }
});
```

As mentioned above, uglify creates an object containing the minified code in the `code` property, so this needs to be saved to a file using `fs`, the Node file module.  In this example, 6 files are concatenated into one minified file not only reducing the soze but also reducing the server hits.

### Reducing image sizes
Images can take up a lot of bandwidth.  JPEGs have compression built in so reducing the size of these is easy.  PNGs are not so easy.  They are useful for web sites because they allow transparency, but this comes with a cost of larger file sizes.  There are tools to compress PNGs by reducing the colours though.  The one I used is [TinyPNG](https://tinypng.com/) - just drop in your images and it spits out compressed versions.  I manged to get a 70% reduction in file size across all my images this way.

### Compressing resources
The last step is to compress as much as possible when sending data.  Modern browsers will request gzipped files where possible to reduce bandwidth.  With Node and Express it's easy to enable gzipping of all content using the [Compression middleware](https://www.npmjs.org/package/compression).

```
$ npm install compression --save
```

This middleware can then be inserted right at the start to compress as much as possible - every request that goes through this middleware will be compressed.

```js
var app = express();
app.use(compression({
  threshold: 512
}));
```
In this example I've set the compression to compress anything below 512 bytes.  Below this there is not much point as the zip headers will be bigger than any space you save.

### Result
The end result of doing this for me was a much faster page  I've been using [GTMetrix](http://gtmetrix.com/) to profile my page and it's reduced in size from over 600Kb to 200Kb, and is currently rated A by PageSpeed and B by Y Slow - up from F for both when I started.

The only thing I fall down on is browser caching.  Seeing as the site is still very mch in development I don't want to turn this on until it settles down a bit.

