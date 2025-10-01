---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# Preface

## Introduction

Welcome to **"Beyond the Basics: Mastering Advanced Python,"** your guide to unlocking the expert-level capabilities of the Python language. This book is designed to take you on a journey through sophisticated concepts and techniques valuable not only in software engineering but across any domain where high-level Python proficiency is a critical asset. 🐍

Whether your work is in data science, academic research, or cloud infrastructure, the skills you acquire here will empower you to write more efficient, robust, and elegant code.

````{admonition} Who is this book for?
:class: note
This book is intended for those who are already comfortable with programming in general, but also with Python's fundamentals and object oriented programming. If you have a solid grasp of variables, control flow, functions, classes, and objects, you are ready to dive in!
````

## About the Author

```{figure} ./figs/logo_noname.png
---
scale: 50%
align: right
---
```
My name is Jakub Walczak, and I am an academic and artificial intelligence researcher.

My journey in education began in 2019 when I started my doctorate, which I completed in 2022 after graduating from Lodz University of Technology. Since then, I have had the pleasure of teaching students Python fundamentals and delivering advanced courses on machine learning and data science.

Parallel to my academic career, I have been active in the industry since 2016. This practical experience has been invaluable and includes roles such as:
* **Software Developer** at Comarch
* **Scientific Software Developer** at the CMCC Foundation in Italy
* **Cloud System Developer** for AI Operations at OpenNebula Systems

This blend of academic theory and real-world application has shaped my approach to teaching and is the foundation upon which this book is built.

````{admonition} A Note from the Author
:class: tip
My goal is to help you move beyond basic Python knowledge and gain real control over your code. This book focuses on practical techniques, clever tricks, and deep insights that will transform how you approach development. These are the concepts that separate developers who *use* Python from those who truly *master* it. I hope this journey empowers you to write more elegant, efficient, and controlled code. Happy coding!
````


## Prerequisites

As this is a course to master Python, I need to make some assumptions about the knowledge you possess. Before diving in, make sure you're equipped with the right foundation. Here's what you'll need to get the most out of your learning journey. Below, you can find what you should know before starting reading this book.

::::{grid} 1 1 1 3
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:link: basics/organize
:link-type: doc
:class-header: bg-light

Programming Fundamentals ✏️
^^^

- Variables, data types, and operators
- Control flow (loops, conditionals)
- Functions and basic algorithms
- Familiarity with Python syntax
- OOP[^oop] experience

:::

:::{grid-item-card}
:link: content/myst
:link-type: doc
:class-header: bg-light

Technical Setup ✨
^^^

- Computer with internet access
- Python installed[^pythonv]

:::

:::{grid-item-card}
:link: content/executable/index
:link-type: doc
:class-header: bg-light

Learning Mindset 🔁
^^^

- Curiosity and willingness to experiment
- Patience with debugging and errors
- A few hours per week for practice
- Openness to collaborative learning

:::

::::

[^oop]: If you don't know what *OOP* is, this book is not for you yet.
[^pythonv]: I will use the most recent version (as of the time of writing) Python 3.13. However, you can use any version from 3.10 onwards. I will point out important differences where relevant.

## Recommended Preparation
```{admonition} Not quite ready?
:class: tip prereq-tip

If you're missing some prerequisites, don't worry! Here are some resources to help you catch up:

- **Python Basics**: [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- **Software Engineering Basics**: If you can ready in **polish**, my book about software engineering fundamentals in Python may be helpful:
> Walczak, J. (2023). Elementy inżynierii oprogramowania w Pythonie. Helion.
- **Python Bootcamps**: Many online platforms offer intensive Python bootcamps for beginners
- **Python Online Courses**: There is a variety of free online resources that will help you get acquainted with Python
```

## How Is This Book Organized?
At the very beginning of each chapter, I will list specific prerequisites you should satisfy to fully understand the content. Then, I will go through the theory, enriching it with examples. At the end of each chapter, I will include exercises for you to practice and experiment with.


## What Will You Learn from This Book?

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Special Attributes 🏷️
:class-header: bg-light

Those famous `__dunder__` attributes for modules, classes, methods, and other Python objects
:::

:::{grid-item-card} Context Managers 🔒
:class-header: bg-light

Usage of `with` keyword and their potential applications and limits
:::

:::{grid-item-card} Higher-Order Functions 🔄
:class-header: bg-light

Functions that take or return a function
:::

:::{grid-item-card} Decorators 🎨
:class-header: bg-light

Syntactic sugar, preceded by closures
:::

:::{grid-item-card} Metaclasses 🏗️
:class-header: bg-light

A vital element in dynamic programming
:::

:::{grid-item-card} Descriptors 📋
:class-header: bg-light

Including the popular `@property`
:::

:::{grid-item-card} Code Inspection 🔍
:class-header: bg-light

Stack tracing, callable signature management, and more
:::

:::{grid-item-card} Dynamic Code Execution ⚡
:class-header: bg-light

And its pros and cons
:::

:::{grid-item-card} Generic Collections 📦
:class-header: bg-light

Type-safe collection handling
:::

:::{grid-item-card} Weak References 🔗
:class-header: bg-light

For caching and other purposes
:::

:::{grid-item-card} Coroutines ⏭️
:class-header: bg-light

And their applications
:::

:::{grid-item-card} Concurrent & Parallel Execution 🚀
:class-header: bg-light

Mastering multi-threaded and multi-process programming
:::

::::


```{code-cell} ipython3
:tags: ["remove-input"]
import styles
print()

styles.apply_style()
```


