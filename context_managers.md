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
# Context Managers

As you are (hopefully) already accustomed to (at least basic) Python, you've almost certainly encountered those fancy and extremely useful structures with the {code}`with` keyword, called **context managers**. Where does this name come from? Well, context managers define a runtime environment (context) for a given block of code.

````{admonition} Block of code?
:class: tip
I am sure you know it, but block of code is a sequence of Python's statements within the same indentation, e.g. this block of code for the `for` loop contains just a single statement: {code}`print(i)`:

```python
for i in range(10):
    print(i)
```
````

Why do we need such an environment? Well, when you need to configure anything before executing some piece of code (a code block) and/or tear down and clean up afterwards. That's the core idea behind **context managers**: set up before, clean up after, guaranteed.

## Running in context
To run the code within the context managed by , noone else than **context manager**, we use the [`with`](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) statement. If context managers returns any object on setup, you can bind it using the {code}`as` keyword:

```{code-cell} ipython3
:tags: [remove-stderr]

with open("some_dummy_file.txt", "w") as f:
    f.write("1st line\n")
    f.write("2nd line")
```

Context managers can be created two-fold, either as [class-based definiton](#class-based-definition) or [generator-based definition](#generator-based-definition). Both are presented below.


## Class-based definition
````{admonition} welocme OOP
:class: important
To define contetx manager using classes you need to know what a **class** is and how we can define it. If you don't have such a knowledge, get it and return later.
````

The context manager can be created as **a class** which implements two special (**dunder**[^dunder]) methods:

1. `__enter__`
2. `__exit__`.

It is quite clear that the first (`__enter__`) is respondible for setting up execution context (environment) whereas the latter --- for cleaning up.

### `__enter__`
The setting up method is argumentless, namely it takes just an implicit parameter (`self`), but you can return anything. Remmeber that the object returned by `__enter__` methods can be binded to the target variable using the `as` keyword.

```{code-block} python
:lineno-start: 1
:emphasize-lines: 5

class MyContextManager:

    def __enter__(self, arg_1, arg_2): 
        # some logic goes here
        return self # We return an object itself to be able to bind it using `as`
```

````{admonition} Did you know?
:class: tip
If `__enter__` method does not raise the error, `__exit__` method is guaranteed to be invoked {cite}`python:compound_with`, regardless the block inside context manager raise an error or not.
````


### `__exit__`
Unlike the `__enter__`, the `__exit__` method imposes some predefined signature. It always takes three arguments:
1. exception type (type hints: `type[Exception] | None`),
2. exception value (type hint: `Exception`),
3. traceback

It the block of code inside context manager does not rise the error, all those arguments will be `None`. Otherwise, they will be set accordingly. The question is, what to do next with such an error. You have two options:

1. surpass it (silnece it, do not propagte),
2. reraise

To surpass the exception (or manage it on your own inside `__exit__` method), you need to return `True` value. If exception is expected to be propragted, you can return whatever else (or even nothing). Following our above example, let us add `__exit__` dummy implementation:


```{code-block} python
:lineno-start: 7
:emphasize-lines: 3

    def __exit__(self, exc_type: type[Exception] | None, exc_val: Exception, traceback): 
        # some logic goes here
        return True # If we want to surpass the error, we return True
```


As an example, we will try to reimplement a simplified version of [`chdir`](https://docs.python.org/3/library/contextlib.html#contextlib.chdir) context manager to chnage the current working directory.



```{code-block} python
:lineno-start: 1
:emphasize-lines: 7, 10, 11, 16

import os

class ChDir:
    saved_path: str

    def __init__(self, new_path):
        self.new_path = new_path # We save the new dir we move in inside context manager

    def __enter__(self):
        self.saved_path = os.getcwd() # We store this to restore it later
        os.chdir(self.new_path) # We actually change directory here
        print(f"📂 Changed directory to: {self.new_path}")
        return self  # Not needed, but we can use it with `as` keyword

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.saved_path) # We restore the original working directory
        print(f"↩️ Returned to: {self.saved_path}")
```

Let us see, how to works:


## Generator-based definition

````{admonition} Do you know generators?
:class: important
Before you dive into this section, ensure you are accustomed with Python generators. Read 📰 about them in the chapter [Generators](./generators.md).
````

````{admonition} Do you know decorators?
:class: important
You should be alsways aware of decorators before reading this section, You will find them in the chapter [Decorators](./decorators.md).
````

Writing context managers as classes gives us far the most flexibility, however, there is another, quite convenient way, how to create a simple context manager - by using generator function {cite}`python:generator_glossary_misc`, hence the pivotal one is the [`yield`](python:generator_glossary_misc) expression and the decorator `@contextmanager` from the [`contextlib`](https://docs.python.org/3/library/contextlib.html) {cite}`python:contextmanager_doc` to use over the generator function: It has the following structure:


```{code-block} python
:lineno-start: 7
:emphasize-lines: 3, 7

from contextlib import contextmanager

@contextmanager # We need to use decorator to make it context manager
def my_context_manager():
    # here is the logic to run on setup
    try:
        yield # We can yield something to be able to bind to using `as`
    except Exception as e:
        # logic to handle (optionally) exception
    finally:
        # logic to clean up
```


# Usage

```{code-cell} python
:tags: ["remove-input", "remove-output"]

import os

class ChDir:
    saved_path: str

    def __init__(self, new_path):
        self.new_path = new_path # We save the new dir we move in inside context manager

    def __enter__(self):
        self.saved_path = os.getcwd() # We store this to restore it later
        os.chdir(self.new_path) # We actually change directory here
        print(f"📂 Changed directory to: {self.new_path}")
        return self  # Not needed, but we can use it with `as` keyword

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.saved_path) # We restore the original working directory
        print(f"↩️ Returned to: {self.saved_path}")

os.chdir("/home")
```



```{code-cell} python
print("Before context:", os.getcwd())

with ChDir("/tmp"):  # or any folder you have
    print("Inside context:", os.getcwd())
    # do stuff here safely

print("After context:", os.getcwd())
```




[^dunder]: Don't remember what dunder methods are? See [Special Attributes](./special_attributes.md).

