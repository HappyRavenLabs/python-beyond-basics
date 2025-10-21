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

## Introduction

As you are (hopefully) already accustomed to (at least basic) Python, you've almost certainly encountered those fancy and extremely useful structures with the {code}`with` keyword, called **context managers**. Where does this name come from? Well, context managers define a runtime environment (context) for a given block of code.

````{admonition} Block of code?
:class: tip
I am sure you know it, but a block of code is a sequence of Python statements within the same indentation, e.g., this block of code for the `for` loop contains just a single statement: {code}`print(i)`:

```python
for i in range(10):
    print(i)
```
````

Why do we need such an environment? Well, when you need to configure anything before executing some piece of code (a code block) and/or tear down and clean up afterwards. That's the core idea behind **context managers**: set up before, clean up after, guaranteed.

## Running in context
To run code within the context managed by a **context manager**, we use the [`with`](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) statement. If the context manager returns any object on setup, you can bind it using the {code}`as` keyword:

```{code-cell} ipython3
:tags: [remove-stderr]

with open("some_dummy_file.txt", "w") as f:
    f.write("1st line\n")
    f.write("2nd line")
```

Context managers can be created in two ways: either as a [class-based definition](#class-based-definition) or a [generator-based definition](#generator-based-definition). Both are presented below.


## Class-based definition
````{admonition} Welcome OOP
:class: important
To define a context manager using classes, you need to know what a **class** is and how we can define it. If you don't have such knowledge, learn about it and return later.
````

A context manager can be created as **a class** which implements two special (**dunder**[^dunder]) methods:

1. `__enter__`
2. `__exit__`

It is quite clear that the first (`__enter__`) is responsible for setting up the execution context (environment), whereas the latter is responsible for cleaning up.

### `__enter__`
The setup method is argumentless, namely it takes just an implicit parameter (`self`), but you can return anything. Remember that the object returned by the `__enter__` method can be bound to the target variable using the `as` keyword.

```{code-block} python
:lineno-start: 1
:emphasize-lines: 5

class MyContextManager:

    def __enter__(self): 
        # some logic goes here
        return self # We return the object itself to be able to bind it using `as`
```

````{admonition} Did you know?
:class: tip
If the `__enter__` method does not raise an error, the `__exit__` method is guaranteed to be invoked {cite}`python:compound_with`, regardless of whether the block inside the context manager raises an error or not.
````


### `__exit__`
Unlike `__enter__`, the `__exit__` method imposes three parameters:
1. exception type (type hint: `type[Exception] | None`),
2. exception value (type hint: `Exception | None`),
3. traceback (type hint: `types.TracebackType | None`)

If the block of code inside the context manager does not raise an error, all those arguments will be `None`. Otherwise, they will be set accordingly. The question is, what to do next with such an error? You have two options:

1. suppress it (silence it, do not propagate),
2. reraise it

To suppress the exception (or manage it on your own inside the `__exit__` method), you need to return the value `True` explicitly or any expression evaluated to `True` {cite}`python:stdtypes_truth`. Otherwise, the exception will be propagated. Following our above example, let us add a dummy `__exit__` implementation:


```{code-block} python
:lineno-start: 7
:emphasize-lines: 3

    def __exit__(self, exc_type: type[Exception] | None, exc_val: Exception | None, traceback): 
        # some logic goes here
        return True # If we want to suppress the error, we return True
```


As an example, we will try to reimplement a simplified version of the [`chdir`](https://docs.python.org/3/library/contextlib.html#contextlib.chdir) context manager from [`contextlib`](https://docs.python.org/3/library/contextlib.html) standard library to change the current working directory.



```{code-block} python
:lineno-start: 1
:emphasize-lines: 7, 10, 11, 16

import os

class ChDir:
    saved_path: str
    new_path: str

    def __init__(self, new_path):
        self.new_path = new_path # We save the new directory we move into inside the context manager

    def __enter__(self):
        self.saved_path = os.getcwd() # We store this to restore it later
        os.chdir(self.new_path) # We actually change directory here
        print(f"📂 Changed directory to: {self.new_path}")
        return self  # Not required, but we can use it with the `as` keyword

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.saved_path) # We restore the original working directory
        print(f"↩️ Returned to: {self.saved_path}")
```

````{admonition} Asynchronous generator-based context managers
:class: attention
To create asynchronous context manager (see section below [Asynchronous Context Managers](#asynchronous-context-managers)) {cite}`python:datamodel_asynccontext`, you need to use [`__aenter__`](https://docs.python.org/3/reference/datamodel.html#object.__aenter__) and [`__aexit__`](https://docs.python.org/3/reference/datamodel.html#object.__aexit__) asynchronous dunder methods. Their signature is the same as their synchronous counterparts.
````

## Generator-based definition

````{admonition} Do you know [**generators**](./generators.md)?
:class: important
Before you dive into this section, ensure you are familiar with Python generators. Read 📰 about them in the chapter [Generators](./generators.md).
````

````{admonition} Do you know [**decorators**](./decorators.md)?
:class: important
You should be aware of decorators before reading this section. You will find them in the chapter [Decorators](./decorators.md).
````

Writing context managers as classes gives us the most flexibility; however, there is another, quite convenient way to create a simple context manager—by using a generator function {cite}`python:generator_glossary_misc`. The pivotal element is the [`yield`](https://docs.python.org/3/reference/simple_stmts.html#yield) statement and the [`@contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) decorator from the [`contextlib`](https://docs.python.org/3/library/contextlib.html) {cite}`python:contextmanager_doc` module, which is used to decorate the generator function. It has the following structure:


```{code-block} python
:lineno-start: 1
:emphasize-lines: 3, 7

from contextlib import contextmanager

@contextmanager # We need to use this decorator to make a func a context manager
def my_context_manager():
    # here is the logic to run on setup
    try:
        yield # We can yield something to be able to bind it using `as`
    except Exception as e:
        # logic to handle (optionally) the exception
    finally:
        # logic to clean up
```

So, we have:

```{list-table} A line-by-line explanation of generator-based context manager
:header-rows: 1
:name: code-explanation-context-manager

* - **Line**
  - **Code**
  - **Explanation**
* - 1
  - ```python
    from contextlib import contextmanager
    ```
  - Imports the `contextmanager` decorator from the `contextlib` module of the standard Python library (no need to install anything)
* - 3-4
  - ```python
    @contextmanager
    def my_context_manager():
    ```
  - We decorate the function to make it a context manager
* - 5
  - ```python
    # here is the logic to run on setup
    ```
  - Here (before the `yield` statement) you put all the logic to set up the runtime context (as you would in the `__enter__` method of a class-based definition)
* - 6-7
  - ```python
    try:
        yield 
    ```
  - This is where the magic happens. It creates a generator function, so it saves the state and sends a value (here we send nothing, but anything you add after `yield` can be assigned using the `as` keyword, like the return value of the `__enter__` method). It is inside the `try-except` block to be able to catch and process (or suppress) any exception that occurred in the context manager
* - 8-9
  - ```python
    except Exception as e:
        # logic to handle (optionally) exception
    ```
  - Here we catch any exception which occurred inside the context manager. You can catch a more specific error or keep it as general as `Exception`. Here you have flexibility to handle or suppress a particular type of exception
* - 10-11
  - ```python
    finally:
        # logic to clean up
    ```
  - As in most programming languages, the `finally` block is executed in either case: whether an error was raised or not. The logic inside the `finally` block corresponds to the cleanup logic you would put in the `__exit__` method of a class-based definition
```

````{admonition} Asynchronous generator-based context managers
:class: attention
If you intend to create an asynchronous context manager (see section below [Asynchronous Context Managers](#asynchronous-context-managers)), remember to define the function (decorated with [`@asynccontextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager)) as `async`.
````


````{admonition} Context manager as decorator? Why not?
:class: tip
The [`contextlib`](https://docs.python.org/3/library/contextlib.html) library provides a variety of other useful tools. For example, you can create a context manager **as a decorator**. To do that, you just follow the [class-based definition](#class-based-definition) and add a parent class [`ContextDecorator`](https://docs.python.org/3/library/contextlib.html#contextlib.ContextDecorator), so you can use it as:


```{code-block} python
:lineno-start: 1
:emphasize-lines: 4

import os
from contextlib import ContextDecorator

class ChDir(ContextDecorator): # Note, we've added a parent class
    ...

@ChDir("/tmp")
def some_func():
    # some function's logic
    print(f"I am in {os.getcwd()}")

some_func()
```

````

## Usage
Regardless of the way you defined your context manager, you can use it as below:


```{code-cell} python
:tags: ["remove-input", "remove-output"]

import os

class ChDir:
    saved_path: str

    def __init__(self, new_path):
        self.new_path = new_path # We save the new directory we move into inside the context manager

    def __enter__(self):
        self.saved_path = os.getcwd() # We store this to restore it later
        os.chdir(self.new_path) # We actually change directory here
        print(f"📂 Changed directory to: {self.new_path}")
        return self  # Not required, but we can use it with the `as` keyword

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

## Asynchronous context managers

````{admonition} Do you know [**coroutines**](./coroutines.md)?
:class: important
To understand this section well, read 📰 the [Coroutines](./coroutines.md) chapter first.
````

When possible, such as when performing input/output operations like handling files, opening database connections, or managing HTTP connections, we can create an asynchronous version of a context manager. The dunder methods for creating asynchronous context managers can be coroutines (see the [Coroutines](./coroutines.md) chapter). These special methods' names change slightly: they must be defined using `async def`, and their names are `__aenter__` and `__aexit__` for setting up and cleaning up the asynchronous context manager, respectively. As an example, let's create a simple asynchronous context manager to lock a file in order to prevent it from being overwritten by concurrent tasks (to avoid data inconsistency).


```{code-block} python
:lineno-start: 1
:emphasize-lines: 11, 17

import asyncio

class AsyncFileLock:
    filename: str
    lock: asyncio.Lock

    def __init__(self, filename):
        self.filename = filename
        self.lock = asyncio.Lock()
    
    async def __aenter__(self):  # Note: we are using `async` and the name changed
        print(f"Acquiring lock for {self.filename}...")
        await self.lock.acquire()
        print(f"Lock acquired for {self.filename}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):  # Note: the name is `__aexit__`
        self.lock.release()
        print(f"Lock released for {self.filename}")
        return False
```

We can then use it as follows:


```{code-cell} python
:tags: ["remove-input", "remove-output"]

import asyncio

class Lock:
    filename: str
    lock: asyncio.Lock

    def __init__(self, filename):
        self.filename = filename
        self.lock = asyncio.Lock()
    
    async def __aenter__(self):
        print(f"Acquiring lock for {self.filename}...")
        await self.lock.acquire()
        print(f"Lock acquired for {self.filename}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        print(f"Lock released for {self.filename}")
        return False
   
```



```{code-cell} python
async def some_long_file_handling_func():
    print("Processing file...")
    await asyncio.sleep(10)
    print("File processing done")

async with Lock("/tmp/sample.txt"):
    await some_long_file_handling_func()
```




[^dunder]: Don't remember what dunder methods are? See [Special Attributes](./special_attributes.md).
