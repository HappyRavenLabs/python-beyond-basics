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

# Generators

````{admonition} Meet iterators first?
:class: important
To get the most of this chapter, learn about [iterators](./iterators.md).
````


Generators were introduced in Python 2.2 with PEP255 {cite}`pep-0255`. 
The name is already quite self-explanatory: **something that generates**.
In fact, they are a particular kind of **iterators** (see [Iterators](./iterators.md) section):
kind of **resumable functions** able to "remember" their current state so next value can be computed and provided **on demand**. Synthactically, generators
are created as ordinary (`def`) or asynchronous (`async def`) functions having at least one `yield` statement.
So in its simplest form, it can look like below.

```{code-block} python
:lineno-start: 1
:emphasize-lines: 6

def generate_multipier(x):
    i = 1
    print("We have created a generator. Variable 'i' is set to ", i)
    while True:
        print("Let us yield some value")
        yield x * i # Here we yield the multiplier
        i = i + 1
        print("We now increment 'i'. It now has value", i)
```


```{code-cell} python
:tags: ["remove-input", "remove-output"]

def generate_multipier(x):
    i = 1
    print("We have created a generator. Variable 'i' is set to ", i)
    while True:
        print("Let us yield some value")
        yield x * i # Here we yield the multiplier
        i = i + 1
        print("We now increment 'i'. It now has value", i)
   
```



```{code-cell} python
# We first create "an instance" of generator
generator = generate_multipier(5)
# We generate one value
print("We've yielded: ", next(generator))
# ... and another one
print("We've yielded: ", next(generator))
```

As you can see, we have eternal loop (`while True`) inside, that means our generator is infinite.

````{admonition} Definite generator
:class: hint
If you have definite generators (e.g. able to generate only $N$ values, calling $N+1$ will raise `StopIteration` exception)
````



## Asynchronous generator

