---
title: Online Hosted Instructions
permalink: index.html
layout: home
---

This repository contains the hands-on lab exercises for the [self-paced modules on Microsoft Learn][learn-collection] for building copilots with Azure Cosmos DB. The exercises are designed to accompany the learning materials and enable you to practice using the technologies they describe.

> &#128221; To complete these exercises, you’ll require a Microsoft Azure subscription. You can sign up for a free trial at [https://azure.microsoft.com][azure].

## Labs

{% assign labs = site.pages | where_exp:"page", "page.url contains '/instructions'" %}
| Module | Lab |
| --- | --- |
{% for activity in labs  %}| {{ activity.lab.module }} | [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }}) |
{% endfor %}

[azure]: https://azure.microsoft.com
[learn-collection]: https://learn.microsoft.com/training/browse/?expanded=azure&products=azure-cosmos-db