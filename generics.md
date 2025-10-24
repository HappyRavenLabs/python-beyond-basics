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

# Generics


````{admonition} This chapter is not ready yet?
:class: important
Writing a book takes time and for that chapter I did not have enough of it. Please, return later.
````


## Variance types
Let us explain slightly here the type of type variance we have in Python what was explained in PEP483 {cite}`pep-0483`. In general, types can be:
1. covariant,
2. contravariant,
3. invariant