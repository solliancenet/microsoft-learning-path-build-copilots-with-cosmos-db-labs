---
title: Python SDK lab setup
nav_order: 1
has_toc: false
layout: default
---

# Python SDK lab setup

Follow the links below to set up your lab environment for the Python SDK labs.

{% assign labs = site.pages | where_exp:"page", "page.url contains 'python/instructions/00-'" %}
| Setup step |
| --- |
{% for activity in labs  %}| [{{ activity.lab.title }}]({{ site.baseurl }}{{ activity.url }}) |
{% endfor %}