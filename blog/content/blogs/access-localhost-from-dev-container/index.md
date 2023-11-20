---
author: "Jim Bennett"
date: 2023-11-20
description: ""
draft: false
tags: ["devcontainer", "dev container", "localhost", "vscode"]
slug: "access-localhost-from-dev-container"
title: "Connect to localhost from inside a dev container"

images:
  - /blogs/access-localhost-from-dev-container/banner.jpeg
featured_image: banner.jpeg
---

I do a lot of work in dev containers (for example, using [liblab inside of one](/blogs/liblab-in-a-devcontainer/)), often hosting APIs. One problem I used to often hit is how can I host an API in one container, and access it from another dev container? This post shows you how.

## The problem - 'localhost' in a container

So the issue is this:

- **Dev container A** exposes an API on port 8000, and this is forwarded to localhost
- I can access this port at `localhost:8000` either inside **dev container A**, or from my local machine as the dev container forwards the port
- **Dev container B** needs to access the API

The problem here is **dev container B** has no access to my local machine. Docker forwards the ports from **dev container A** to localhost automatically as soon as I run the API. But ports from my local machine are not forwarded into dev containers.

- If **Dev container A** accesses `localhost:8000`, it gets the API running on **Dev container A**
- If my local machine accesses `localhost:8000`, it gets the API running on **Dev container A** because the port on **Dev container A** is forwarded to localhost, as far as the local machine is concerned, 8000 is open and accepting requests.
- If **Dev container B** accesses `localhost:8000` it will fail, as there is nothing running on port 8000 inside that container.

So how can one dev container access ports exposed by another?

## Enter the host.docker.internal network

Docker has a fix for this! It exposes a 'special' [DNS called `host.docker.internal`](https://docs.docker.com/desktop/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host) that essentially gives to access to the local machines network. Rather than access localhost, you access this named device instead.

So from **Dev container B**, you access `host.docker.internal:8000` and boom! **Dev container B** can access the API from **Dev container A**!

For example, you are testing out an SDK created against an API you are running on port 8000 via a dev container (for example, the [liblab llama store](https://github.com/liblaber/llama-store)), and you want to take advantage of the [dev containers feature of liblab to open our SDK in a container](https://developers.liblab.com/cli/config-file-overview-customizations/#devcontainer). You can set the `baseUrl` in your `liblab.config.json` file to `http://host.docker.internal:8000`, then open the generated SDK in its dev container!

```json
{
  "sdkName": "llama-game",
  "specFilePath": "http://localhost:8000/openapi.json",
  "baseUrl": "http://host.docker.internal:8000",
  "languages": [
    "python"
  ],
  "createDocs": true,
  "customizations": {
    "devContainer": true
  }
}
```

Done! The SDK now defaults to use the docker internal network for testing.

```python
class Environment(Enum):
    """The environments available for this SDK"""

    DEFAULT = "http://host.docker.internal:8000"
```

Don't forget to set it to your production URL once you are ready to publish.
