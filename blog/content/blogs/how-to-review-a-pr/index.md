---
title: "How to correctly review a pull request"
date: 2024-04-01
draft: false
featured_image: banner.webp
images: 
  - blogs/how-to-review-a-pr/banner.webp
tags: ["github", "git"]
description: Some tips on how to review a pull request to ensure the best code quality possible
---

One of my popular sayings is that development is a team sport. We don't code in isolation, instead engineers are part of a team that delivers value to users and customers, often made up of software. And for a team to deliver its best code, there needs to be shared ownership of the code. This means that more than one developer is involved in each code change to ensure that it is correct, appropriate, and that the knowledge of this change is shared amongst the team. While there are many techniques for this (such as pair and mob programming), the most popular one is a simple pull request, or PR.

## What is a pull request?

A pull request, or PR, is a git feature that allows you to request that the owner of some code pulls your changes. You make a code change on a fork or branch, and raise a pull request to merge your code into the golden source, origin, or upstream repo. Essentially this is how you get your code published to the team ready to be deployed to production.

The aim of a pull request is to get another set of eyes over your code. Before a PR is merged, it is reviewed. The reviewer can check the code for correctness, style, if it actually implements the feature it's meant to, things like that. This is the opportunity for a second pair of eyes to catch any errors, for knowledge sharing so more than one member of the team understands the new code, and a chance for more senior developers to help guide and upskill more junior developers.

The problem with PRs though, is often the reviews are done badly. The infamous LGTM 👍 (looks good to me). Especially with large PRs that take a lot of time.

![A twitter post from I am developer saying 10 lines of code = 10 issues. 500 lines of code = looks fine.](https://user-images.githubusercontent.com/217029/181068444-9a21be12-9ed3-42cb-95d3-594e75d6192c.png)

## So why are we so bad at reviewing PRs?

The reason is simple - time. Reviewing a 5 line change is potentially quick, so a reviewer can check it, and ask for changes in a short space of time. Give a developer 100 files then the review is often little more than a cursory glace as there isn't enough time to do a full review. After all reviewing code isn't delivering features!

Having seen some very bad PR reviews in my time, and poor code released because of it, I thought I'd scribble down some of my top tips for doing PR reviews right. Add any more thoughts to the comments!

## How to do a better job of reviewing PRs

### 1. Allocate time to do it

This is often something that you as a reviewer can't do, but something you should advocate for and your leadership needs to understand. PR reviews take time. If you expect an engineer to be 100% on feature work, not only do you risk burnout, but it means there is literally no time to review PRs. Everything, no matter how bad will be LGTM 👍, merged and cause problems downstream.

This makes sense for engineers - there's not time to review a PR to catch a bug, but it's easy to get time allocated in a sprint to fix the bugs that get through. Your processes drive poor engineering practice.

Ideally an engineer should be 60% feature work, 20% run the business, 20% spare (vacations, sick time, dealing with weird issues that reduce your ability to work like your OS shitting itself). The 20% run the business should be enough to review PRs, and if not - allocate more time (or move to pair programming, but that takes more to convince management who see people as resources with linear delivery capability).

Now you have time to do a proper PR review, next you need to review the ticket!

### 2. Review the ticket

All good PRs start with a ticket of some description. This is (typically) a ticket in Jira that details the work that is done. But these are not code, so why do you care if you are reviewing a PR? Well the ticket explains the intention of the change. What bug is being fixed, what feature is being added. Without a good detailed ticket, how can you very the code works?

So what makes a good ticket? This is blog post in its own right, but here are some thoughts:

- It exists. Simply having a ticket is a start. No ticket, then no change. All PRs without a ticket should be rejected as how can you ensure the change is correct?
- It explains the why of the change. When you know why you can think about the implementation from the perspective of the end user. Helps when you think about the test cases or ways to test the code.
- It explains the change in as much detail as possible. Move a button? Ok, where, by how much. Add a new API? What endpoint, what is the request and response body?
- It defines some test cases. In a perfect world these should be exhaustive, but it should at least direct some ways to verify the change. Add a feature to calculate X - he are some sample inputs and outputs.
- It defines any impact on other parts of the system. Does it require a downstream change? Should documentation be updated?

Once you are happy with the ticket you can review the code. Not happy - punt it back to the developer or product owner to get it to a good state. Sometimes just by doing this you will catch things the developer missed and get bugs fixed or missing features implemented before you have even looked at the PR.

### 3. Does the code work?

Code should work. The ticket defines the change, and the code should implement it. Before reviewing the code, I like to take it for a spin and see if it actually does what it is meant to do in the context of the whole system. Yes, this usually means some manual testing but again you can catch issues quickly. Not always easy, but there are usually ways and test harnesses to test features in components of a larger system. This is where a good ticket also helps - it can define what you need to test, expected outputs for inputs, and give you a good direction to test edge cases.

But what about unit tests? I'll cover these next, but the presence of unit tests doesn't always mean tha the code works. I've had situations when reviewing a PR where all the tests passed but the code didn't do what was needed when I tested the whole system. Multiple times I showed the engineer the issue, they added unit tests, told me it worked because their unit tests passed, but it didn't work.

For example, if you have an add function and write the following tests: add 2 and 2 to get 4, add 3 and 1 to get 4, and 0 and 4 to get 4. Do these tests show the code works, or that you have a function that always returns 4?

There's no point in reviewing code if it doesn't work.

### 4. Does the code have automated tests?

The next step with testing - what about the automated tests? Does the code have unit test, integration tests, UI tests etc. If not - should it (probably). If yes, do they run, pass, and actually test the code?

I find reviewing the test code first is a good thing to do. If there are obvious test cases missed, edge cases not considered, or poor tests, then you want these fixed before you review the core code.

Can you see in the PR that the tests have run and passed? As above - no point in reviewing code that doesn't work. A PR should run as many unit test as is practical, and there should be guards that block merges if any tests fail.

### 5. Can you understand the code?

Now it is time to review the code. The first thing to review is do you understand it? If you don't understand the code and what it does then you can't review it. It should be reasonably obvious to someone who understands the system and context of the changes. It should also be readable. Does the code have sensible names for variables, functions, and classes? Are there code comments explaining the why of the code?

> Anyone who ways code comments are not needed is wrong. Yes - well named things explain what the code does, but comments explain the why. There is no need to comment a getter to say it gets a value, but you want to explain why you are getting that value in the code and doing things with it

Readability is important in code. I know some developers like to play code golf and solve a problem in as few lines as possible, but sacrificing readability is a terrible thing. You are writing code so humans can understand it, so don't be clever, be clear, concise, and obvious. When reviewing code is it clear to the reader what it is doing and why? Your code should be obvious to the most junior developer on the team - remember code is owned by the team, not the engineer who wrote it, so needs to be accessible to everyone.

### 6. Is the code good?

Lastly is the code 'good' - and by good I mean following team standards. This could include coding standards (tools help here), but also does it follow conventions, is it implemented in a consistent way with the rest of the code base.

For example - if your code writes a message to the user, is this message defined in a constants file with other messages for i18n? Does it conform to a11y standards? Is the naming convention consistent?

This is often subjective, so having a good team agreement with coding standards can help with this.

if it is all good - approve that PR! Any issues, then it's time to leave review comments.

## Commenting on PRs and requesting changes

You've reviewed the code and it's time to leave some comments. Although this post is about reviewing, here are some thoughts on leaving review comments.

- Be kind. Don't be an arse, don't be Linus Torvalds. The person receiving these comments is human and a team mate. Be kind and constructive with all your comments.
- Provide detail in the comments. If something needs to be changed, explain why (e.g. move this to a constants file as per our standards).
- Understand that everyone codes differently and personal opinions have no place. You would have written it differently? Well if the way it is done is ok, then don't impose personal opinions on the implementation. If you ask 20 developers how to do something you'll get 30 responses, not all are wrong.
- For more junior developers, this is an opportunity for learning and growth. Give guidance with changes that help with that growth
- Use things like suggestions for small changes like typos to make it quicker to apply changes

## Go review PRs

This was a quick and dirty post to get some thoughts down on this. Let me know your thoughts in the comments!
