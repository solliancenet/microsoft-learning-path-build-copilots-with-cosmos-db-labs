---
title: JavaScript SDK labs
nav_order: 2
has_children: true
layout: default
---

# JavaScript SDK labs

Below is a list of the labs for the Azure Cosmos DB JavaScript SDK modules.

{% assign labs = site.pages | where_exp:"page", "page.url contains 'javascript/instructions'" %}
| Module | Lab |
| --- | --- |
{% for activity in labs  %}| {{ activity.lab.module }} | [{{ activity.lab.title }}]({{ site.baseurl }}{{ activity.url }}) |
{% endfor %}
