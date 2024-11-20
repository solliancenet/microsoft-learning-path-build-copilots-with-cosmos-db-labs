---
title: Python SDK labs
nav_order: 2
has_children: true
toc: false
layout: default
---

# Python SDK labs

Below is a list of the labs for the Azure Cosmos DB Python SDK modules.

{% assign labs = site.pages | where_exp:"page", "page.url contains 'python/instructions'" %}
| Module | Lab |
| --- | --- |
{% for activity in labs  %}| {{ activity.lab.module }} | [{{ activity.lab.title }}]({{ site.baseurl }}{{ activity.url }}) |
{% endfor %}
