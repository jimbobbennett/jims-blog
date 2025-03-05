---
title: "Can AI help with user personas"
date: 2025-03-04
draft: false
featured_image: banner.png
images: 
  - banner.png
tags: ["ai", "testing", "user", "qa", "product"]
description: Can AI help generate user personas for helping to define a product strategy, and to test the user experience of an app
---

I recently recorded an episode of the [Pieces AI productivity podcast](https://youtube.com/playlist?list=PL3ufX1Aqkp14nCfVUrDjLD3_GTFN0bo95&si=I721SMH3kncXMe2c) with [Jason Arbon](https://www.linkedin.com/in/jasonarbon/), the CEO of [Testers.ai](https://testers.ai/) and [Checkie.ai](https://www.checkie.ai/).

{{< youtube jCB_Xp-MdDs >}}

During this podcast we were discussing how well AI can do at replicating hte actions of humans, and I made the claim that AI will never be as good as humans as it lacks basic empathy. When we consider designing and testing a product, my position was that an AI will never be able to provide those human-level decisions that consider the needs of the individual users.

## Example - a mobile app for truck drivers

I gave an example of a mobile app I built at a company many years ago designed for truck drivers to inspect vehicles. The first ideas for the app failed to take into consideration the UX requirements of the audience. Truck drivers in New Zealand and the US (our audience) are typically:

- Older as this is not a career young people want to get into
- Larger than average due to a sedentary job with poor food choices available at truck stops
- Less tech savvy

> This is the typical user, and doesn't represent the entire user base, but we should always design for the least able users

The initial design for our app was sleek and modern, with small UI controls and an experience that used up to date mobile UI experiences. Which was great for the young, healthy, designers and developers, but would fall down when it hit our users.

We got to these considerations by discussing the app with some of the more customer focused members of the company, folks who were former truck drivers themselves, or folks who meet and work with drivers every day. These are the best people to work with - the ones who have access to the lived experience of the customer. This took days to get the data, with many meetings and discussions to drill down to a set of statements that we could verify the UI designs against.

**Our users are typically older** - which means more potential for poor eyesight. Small controls and text are hard to read.

**Our users are typically larger than average** - which means larger fingers. A tight UI makes it hard to select the right buttons.

**Our users are typically less tech savvy** - which means they are not as used to mobile patterns as the young, tech friendly development team. The experience needs to be intuitive and guide them through the actions they need to do.

So it was back to the drawing board with these thoughts in mind, designing a UI that had larger controls, larger, shorter text, and a simpler flow guiding uses through it step by step.

## Can an AI empathize like this?

Now in my discussion with Jason, I argued that an AI would not make these design choices. It would not have enough empathy about the user to be able to consider aspects like larger fingers, or poorer eyesight. Jason on te other had disagreed - his experience shows that AI is surprisingly good at building user personas. It has access to such a huge corpus of information around many different characteristics of humans, that it is able to reason across these details and come up with recommendations that are accurate and detailed. AI also has the advantage that it can do this at scale, so when you are considering systems that might have multiple types of users, it can create multiple user personas much faster than a human would. You can then feed these personas into AI testing tools to quickly validate the UX of apps for these different users.

## What considerations are there for creating user personas?

When you use an AI to create a user persona, the key point that Jason made was it is better to be vague rather than explicit. The more you guide the AI, the more bias you put into the system. You want an unbiased view, allowing the AI to consider areas you didn't.

For example, if you prompt an AI with:

"I need to build a UI for an app for truck drivers. What design considerations should I have for the user experience based off truck drivers typically having poor eyesight and large fingers?"

You are going to get a response that focuses on poor eyesight and large fingers. Which is great, as you need to know what UX considerations there are for these situations, but misses out on any other situations you might consider.

Instead it is better to do some prompt chaining. Start by asking what design considerations I should have for the user interface first. Then when you have the list prompt again to get more information on each consideration. This way the AI is not biased by your thoughts in what is important, and it can add its own ideas.

## Let's put it to the test

So based on Jason's theory, I decided to put this to the test. Let's see if an AI can help with user personas.

### Prompt 1 - get the UX considerations

Prompt 1: "I need to build a UI for an app for truck drivers. What design considerations should I have for an optimal user experience?"

This is a very generic statement. Let's see how GPT-4o Mini handles this.

> When designing a UI for an app aimed at truck drivers, there are several key considerations to ensure an optimal user experience. Here are some important design considerations:
> 
> 1. **Simplicity and Clarity**:
>    - Use a clean and straightforward layout. Avoid clutter and ensure that the most important features are easily accessible.
>    - Use clear and concise language. Truck drivers may be on the road and need to quickly understand what to do.
> 
> 2. **Large Touch Targets**:
>    - Ensure buttons and interactive elements are large enough to be easily tapped while driving. This reduces the risk of accidental touches and improves usability.
> 
> 3. **Voice Commands**:
>    - Incorporate voice command functionality to allow drivers to interact with the app without taking their hands off the wheel or eyes off the road.
> 
> 4. **Offline Functionality**:
>    - Truck drivers may travel through areas with poor connectivity. Ensure that critical features of the app can function offline and sync data when a connection is available.
> 
> 5. **Navigation and Mapping**:
>    - Integrate reliable navigation features that provide real-time traffic updates, route optimization, and truck-specific routing (considering height, weight, and restrictions).
> 
> 6. **Notifications and Alerts**:
>    - Use non-intrusive notifications to alert drivers about important updates (e.g., delivery reminders, route changes) without being distracting.
> 
> 7. **Customization**:
>    - Allow users to customize their dashboard or main screen to prioritize the features they use most often.
> 
> 8. **Accessibility**:
>    - Ensure the app is accessible to all users, including those with disabilities. Consider color contrast, text size, and screen reader compatibility.
> 
> 9. **Safety Features**:
>    - Include features that promote safety, such as a "Do Not Disturb" mode while driving, which can limit notifications and interactions.
> 
> 10. **User Feedback**:
>     - Provide a way for users to give feedback easily. This can help you improve the app based on real-world usage and needs.
> 
> 11. **Consistent Design Language**:
>     - Maintain a consistent design language throughout the app to help users navigate intuitively. Use familiar icons and terminology.
> 
> 12. **Testing in Real-World Scenarios**:
>     - Conduct usability testing with actual truck drivers to gather insights on how they interact with the app in real-world conditions.
> 
> By focusing on these design considerations, you can create a user-friendly app that meets the needs of truck drivers while ensuring their safety and efficiency on the road.

So far this is pretty good. The focus is more around considerations when driving - so large touch targets because the user may be driving so can't devote attention to looking at the app. It also highlighted connectivity - "Truck drivers may travel through areas with poor connectivity. Ensure that critical features of the app can function offline and sync data when a connection is available". This is something that wasn't considered initially, so bonus points to the AI.

So we have some good things here, and some we didn't think off. But we can now take this and dig in further with more prompts.

### Prompt 2 - get accessibility considerations

The first response focused on driving, so let's try a prompt that focuses more on accessibility.

"For this app, what accessibility considerations are there? What are the typical physical characteristics of a truck driver that may impact the design of the app."

> When designing an app for truck drivers, it's essential to consider accessibility to ensure that all users, including those with disabilities, can effectively use the app. Here are some key accessibility considerations:
> 
> ### Accessibility Considerations:
> 
> 1. **Color Contrast**:
>    - Ensure sufficient contrast between text and background colors to aid users with visual impairments. Use tools to check color contrast ratios.
> 
> 2. **Text Size and Scalability**:
>    - Allow users to adjust text size for better readability. Use scalable fonts that maintain clarity when resized.
> 
> 3. **Screen Reader Compatibility**:
>    - Ensure that all elements of the app are compatible with screen readers. Use semantic HTML and ARIA (Accessible Rich Internet Applications) roles to provide context.
> 
> 4. **Alternative Text for Images**:
>    - Provide descriptive alt text for images and icons to assist users who rely on screen readers.
> 
> 5. **Keyboard Navigation**:
>    - Ensure that all interactive elements can be accessed and operated using a keyboard. This is crucial for users with mobility impairments.
> 
> 6. **Voice Control**:
>    - Incorporate voice control features to allow users to navigate the app without needing to use touch controls.
> 
> 7. **Clear and Simple Language**:
>    - Use plain language and avoid jargon to make the app more understandable for users with cognitive disabilities.
> 
> 8. **Feedback Mechanisms**:
>    - Provide clear feedback for user actions (e.g., button presses, form submissions) to help users understand the results of their interactions.
> 
> 9. **Customizable UI**:
>    - Allow users to customize the interface to suit their needs, such as changing color schemes or layouts.
> 
> ### Typical Physical Characteristics of Truck Drivers:
> 
> 1. **Age Range**:
>    - Truck drivers can vary widely in age, which may affect their comfort with technology. Older drivers may prefer larger text and simpler interfaces.
> 
> 2. **Physical Stamina**:
>    - Truck drivers often spend long hours on the road, which can lead to fatigue. The app should minimize cognitive load and provide quick access to essential features.
> 
> 3. **Hand Dexterity**:
>    - Some drivers may have reduced dexterity due to age or physical conditions. Ensure that touch targets are large enough and spaced adequately to prevent accidental touches.
> 
> 4. **Visual Impairments**:
>    - Some drivers may experience vision issues, such as reduced acuity or color blindness. The app should accommodate these conditions through adjustable settings.
> 
> 5. **Hearing Impairments**:
>    - Consider drivers who may have hearing impairments by providing visual alerts and notifications in addition to audio cues.
> 
> 6. **Cognitive Load**:
>    - Truck drivers need to manage multiple tasks while driving. The app should be designed to minimize distractions and present information clearly and concisely.
> 
> By addressing these accessibility considerations and understanding the physical characteristics of truck drivers, you can create an app that is inclusive and user-friendly for a diverse audience.

Now we have more good stuff here. The AI has considered age and dexterity, focusing on large text, simpler interfaces, large targets, and adjustable text. The small worry is the AI is recommending thoughts for folks who use screen readers - unlikely to be the typical truck driver, if your eyesight is bad enough to use a screen reader it is unlikely you would be driving.

It also had recommendations around cognitive load - reducing the impact on drivers who are focusing on the road. Distractions are a major cause of accidents, so anything the app can do to reduce these is a benefit.

## Who wins, AI or humans?

So who is the better at empathizing about the human? Are humans better, or as the AI the winner.

As much as it pains me to say it, I think in this case the AI wins. We humans put together a small set of considerations in a matter of days with many back and forth discussions between teams. The AI however was able to replicate what we decided and more in only 2 prompts. About 1 minutes work.

Does this mean we should discount the human and go all in on AI? Absolutely not. AI makes mistakes. In this example the mistakes are few, just references to users who's visual impairments need accommodations such as screen readers, far outside what is needed legally to drive.

Is this a great contribution? Very much so. To me if I was doing a similar exercise again I would run multiple prompts through the AI, gather data, then work through these with humans to build a final set of design considerations in a very short space of time, saving days.

Please let me know your thoughts? Have you used AI to design a product? Did it have the right design considerations for your user personas? Let me know in the comments.
