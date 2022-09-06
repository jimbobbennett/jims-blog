---
author: "Jim Bennett"
categories: ["technology", "mxchip", "IoT", "Iot Hub", "azure"]
date: 2020-02-12T02:02:48Z
description: ""
draft: false
images:
  - /blogs/setting-an-mxchip-connection-string-in-code/banner.jpg
featured_image: banner.jpg
slug: "setting-an-mxchip-connection-string-in-code"
summary: "Learn how to set the Azure IoT Hub connection string on an MXChip board in code."
tags: ["technology", "mxchip", "IoT", "Iot Hub", "azure"]
title: "Setting an Azure IoT Hub connection string in code on an MXChip"

images:
  - /blogs/setting-an-mxchip-connection-string-in-code/banner.png
featured_image: banner.png
---


I was recently asked if there was a way to set the Azure IoT Hub connection string for an MXChip board in code. Normally you'd push this to the EEPROM using the tooling in VS code, or from a terminal using SSH as described [here](https://microsoft.github.io/azure-iot-developer-kit/docs/use-configuration-mode/). In this situation, this was for students and was needed for two reasons:

* The students would be sharing lab PCs and MXChip boards so would need to constantly log in and out of the Azure extensions in VS Code and re-configure boards - something they would probably forget to do every now and again causing a support headache.
* The lecturer would need to be able to take their code and run it on their own board to test, so would need their connection string. To save time configuring boards and looking up connection strings, it would be better to have it in code. Again, it could easily be forgotten!

> **NOTE** - this is potentially a **very bad thing** as you can end up essentially putting secrets in code. **DO NOT** do this for public code, code then ends up on GitHub or anything like this, this only makes sense for private code submitted internally for something like a students assessment using a hub on a free tier so cannot cause any cost if it gets flooded.

Out of the box there are no APIs available to do this. However, there is a way!

When connecting to Azure IoT Hub over MQTT, you call _`DevKitMQTTClient_Init`_ and this loads the connection string from EEPROM and uses it for the connection. As it turn out, as well as being able to read from EEPROM in code, you can also [write to the EEPROM](https://microsoft.github.io/azure-iot-developer-kit/docs/apis/eeprom-interface/#write), meaning you can set the value before it is read.

Using this, it wasn't too hard to write the code to set this value:

```c
# include "EEPROMInterface.h"
# include "SerialLog.h"

...

void setup() {
  ...
  
  if (WiFi.begin() == WL_CONNECTED)
  {
    // Write the connection string to EEPROM as an array of uint8_t
    EEPROMInterface eeprom;
    char connString[] = "<my connection string>";
    int ret = eeprom.write((uint8_t*)connString, 
                           strlen(connString), 
                           AZ_IOT_HUB_ZONE_IDX);
                           
    // Check the write worked - 0 means it was written
    // Less than 0 is an error
    if (ret < 0)
    {
        LogError("Unable to get the connection string from EEPROM.");
        return;
    }

    // Connect as normal, this will read the new value
    // for the connection string
    DevKitMQTTClient_Init();
    ...
}
```

Replace `<my connection string>` in the above code with your connection string. It will then be written to the EEPROM before the call to `DevKitMQTTClient_Init`.

If you read the [EEPROM write documentation](https://microsoft.github.io/azure-iot-developer-kit/docs/apis/eeprom-interface/#write), you will see _zones_ listed. These are defined areas in the EEPROM and you can use these to write the WiFi SSID and Password as well as the connection string. This is useful if you want to build a solution that downloads new WiFi details.

