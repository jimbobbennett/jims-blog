---
author: "Jim Bennett"
categories: ["technology", "azure", "IoT", "Iot Hub", "cosmos db", "stream analytics"]
date: 2019-12-05T23:17:04Z
description: ""
draft: false

slug: "storing-iot-data-in-a-database"
summary: "Learn how to use Stream Analytics to stream data from an IoT hub to a database such as Cosmos DB"
tags: ["technology", "azure", "IoT", "Iot Hub", "cosmos db", "stream analytics"]
title: "Storing IoT Data in a database"

images:
  - /blogs/storing-iot-data-in-a-database/banner.png
featured_image: banner.png
---


One question that comes up a lot when getting started with IoT is 'How do I store all this data?'. This is an important question - IoT creates a _LOT_ of data, some of which can be analyzed on the fly, but there are a large number of cases where you want to run analytics later, or have access to historical raw data to run new analytics later.

IoT typically involves ingesting a large number of messages through a single hub, and these hubs are typically dumb - in that they provide a single point to ingest the messages but don't do anything with them. That's the responsibility of the developers building out the IoT solution.

One area that is powerful with Azure IoT is [Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/?WT.mc_id=streamanalytics-blog-jabenn). This is a service that can be connected to any event stream, such as an IoT Hub, and take the live stream of data and do something with it, such as filter, manipulate and output to other systems. You can even wire up ML based anomaly detection to be alerted when unexpected values are received.

In this post we will see how to use Stream Analytics to stream IoT data into a database. This assumes you already have an IoT hub receiving data.

# Create a database

The first thing you need is a database to put the data into. Stream analytics works with both [Azure Cosmos DB](https://azure.microsoft.com/services/cosmos-db/?WT.mc_id=streamanalytics-blog-jabenn) and [Azure SQL Database](https://azure.microsoft.com/services/sql-database/?WT.mc_id=streamanalytics-blog-jabenn), as well as many other storage solutions, so it's up to you which one you want to use. In this post I'll use Cosmos DB, but the concepts apply to all data stores.

* Launch the [Azure Portal](https://portal.azure.com/?WT.mc_id=streamanalytics-blog-jabenn)
* Select **+ Create a resource** from the menu on the left or the dashboard
* Search for _Azure Cosmos DB_, select it and select **Create**
* Select your subscription, select or create a new resource group and name your account.
* Set the API to _Core (SQL)._ Stream Analytics only supports the SQL API.
* Set the location closest to you, then select **Review + create**, then select **Create**
* This will take a few minutes to create, so once done load it in the portal
* Create a new collection to store the data. From the Cosmos DB resource, head to the **Data Explorer** tab
* Select **New Container**
* Give the database a name
* Set the throughput. You can find a discussion around throughput in [the documentation](https://docs.microsoft.com/azure/cosmos-db/set-throughput/?WT.mc_id=streamanalytics-blog-jabenn). For a simple test setup, set this to be 400 (the minimum).
* Give the container a name
* Set a partition key. You can read more on partition keys in [the documentation](https://docs.microsoft.com/azure/cosmos-db/partitioning-overview/?WT.mc_id=streamanalytics-blog-jabenn)
* Select **OK**

# Create a Stream Analytics resource

Once you have the database, you need to create a Stream Analytics resource.

* Launch the [Azure Portal](https://portal.azure.com/?WT.mc_id=streamanalytics-blog-jabenn)
* Select **+ Create a resource** from the menu on the left or the dashboard
* Search for _Stream Analytics job_, select it and select **Create**

{{< figure src="2019-12-05_14-28-07.png" >}}

* Give the job a name, select your subscription, select or create a new resource group and set the location closest to you.
* Stream Analytics jobs can be hosted in the cloud, or run on the edge via an IoT Edge Gateway device. For now, select _Cloud_, but you can learn more about running on the edge in [the documentation](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-edge/?WT.mc_id=streamanalytics-blog-jabenn).
* Set the number of Streaming units you need - the more data coming in, the larger the number of streaming units you need. You can read more about streaming units in [the documentation](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-streaming-unit-consumption/?WT.mc_id=streamanalytics-blog-jabenn), and learn about pricing on our [pricing page](https://azure.microsoft.com/pricing/details/stream-analytics/?WT.mc_id=streamanalytics-blog-jabenn). For now leave this as the default of 3.

{{< figure src="2019-12-05_14-37-25-1.png" >}}

* Select **Create**.

# Connect the dots

Stream analytics allows you to define inputs, outputs and queries. Queries query inputs and can push data into outputs, so you can query all items from an IoT Hub and select them into a Cosmos DB database. These queries run on the stream as data is received, and output as each item is processed - these are not like traditional SQL queries that run synchronously against a static set of data.

## Adding the IoT Hub as an input

* Select the stream analytics job in the Azure portal
* Head to the **Inputs** tab
* Select **+ Add stream input**, then select _IoT Hub_

{{< figure src="2019-12-05_14-47-41.png" >}}

* Give the input an alias - this is the name you will use in your queries
* Ensure _Select IoT Hub from your subscription_ is selected, and select your IoT Hub. Leave the rest of the values as the defaults.
* Select **Save**

## Adding Cosmos DB as an output

* Head to the **Outputs** tab
* Select **+ Add**, then select _Cosmos DB_

{{< figure src="2019-12-05_14-52-46.png" >}}

* Give the output an alias - this is the name you will use in your queries
* Ensure _Select Cosmos DB from your subscriptions_ is selected, and select your Cosmos DB account, database and container.
* Set the **Document id** field to be the unique key field for the records you will be inserting. If you are inserting directly from IoT Hub without any translation then use what ever unique id is set on each message.
* Select **Save**

## Building the query

* Head to the **Query** tab
* Change the query to be:

```sql
SELECT
  *
 INTO
   [cosmos-db]
 FROM
   [iot-hub]
```

* Set `[cosmos-db]` to be the alias you used for your Cosmos DB database. This needs to be inside square brackets, so if you used `myCosmosDB` as the alias, you would use `[myCosmosDB]`.
* Set `[iot-hub]` to be the alias of the IoT hub, again inside square brackets
* Select **Save query**

## Start the query

* Head the the **Overview** tab
* Select **Start**
* The query will start listening to data coming in the input, and send it to the output

Once data comes in, you will be able to see it appear in Cosmos DB.

# Learn more

* Create a free [Azure account](https://azure.microsoft.com/free/?WT.mc_id=streamanalytics-blog-jabenn)
* Check out the [Stream Analytics documentation](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-introduction/?WT.mc_id=streamanalytics-blog-jabenn).
* Browse the [Stream Analytics modules on Microsoft Learn](https://docs.microsoft.com/learn/browse/?term=stream analytics&WT.mc_id=streamanalytics-blog-jabenn) and grow your skills via hands on learning.

