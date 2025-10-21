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
To get the most out of this chapter, learn about [iterators](./iterators.md).
````

## What Are Generators?

Generators were introduced in Python 2.2 with PEP255 {cite}`pep-0255`. 
The name is already quite self-explanatory: **something that generates**.
In fact, they are a particular kind of **iterators** (see [Iterators](./iterators.md) chapter):
a kind of **resumable functions** able to "remember" their current state so the next value can be computed and provided **on demand**. Syntactically, generators
are created as ordinary (`def`) or asynchronous (`async def`) functions having at least one `yield` statement.
So in its simplest form, it can look like the example below.


```{code-block} python
:lineno-start: 1
:emphasize-lines: 6

def generate_multiplier(x):
    i = 1
    print("We have created a generator. Variable 'i' is set to", i)
    while i < 3:
        print("Let us yield some value")
        yield x * i
        i = i + 1
        print("We now increment 'i'. It now has value", i)
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]

def generate_multiplier(x):
    i = 1
    print("We have created a generator. Variable 'i' is set to", i)
    while i < 3:
        print("Let us yield some value")
        yield x * i
        i = i + 1
        print("We now increment 'i'. It now has value", i)
```

```{code-cell} python
# We first create "an instance" of generator (generator iterator)
generator = generate_multiplier(5)
# We generate one value
print("We've yielded:", next(generator))
# ... and another one
print("We've yielded:", next(generator))
```

````{admonition} Yielding?
:class: important
The `yield` statement (or expression) can be used only **within** a function's definition {cite}`python:yield-statement`!
````

````{admonition} Generator vs Generator Iterator
:class: note

**Generator**, by definition (in Python), is a function with a `yield` statement.
**Generator iterator** is an **iterator** produced when invoking a generator function.
Sometimes the name **generator** is used in either case!

```python
# my_gen is a generator function (generator)
def my_gen():
    ...

# gen is a generator iterator
gen = my_gen()
```
````

````{admonition} Exhausted Generator Iterator
:class: important
Generator function can execute `yield` statement multiple time (explicitly or in loop). When all of them have been already executed, generator (iterator) is said to be **exhausted**, and requesting the next value will raise a [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception:

```python
next(generator) # StopIteration
```
produces:

```python
We now increment 'i'. It now has value 3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```
````

````{admonition} Infinite Generator
:class: hint
There is nothing against creating an infinite generator. To achieve that you can use an infinite loop (`while True`).
````

## Can a Generator `return`?

Well, yes, but it does not work as you might expect. We already know that executing 
the generator function produces a generator iterator. But we can have a `return` statement inside such a function:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 4

def sample_gen(x):
    yield 1
    yield 2
    return 100
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]

def sample_gen(x):
    yield 1
    yield 2
    return 100
```

As the `yield` statement will be executed twice (in the example above), we can run the `next` method twice 
for the generator iterator. Another call will raise a 
[`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception, and if our generator function has a `return` statement, the returned value will become part of the [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception:

```{code-cell} python
:tags: ["raises-exception"]
generator = sample_gen(5)
print("We've yielded:", next(generator))
print("We've yielded:", next(generator))
print("We've yielded:", next(generator))
```

So we can explicitly catch the [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception and extract the return value:

```{code-cell} python
try:
    generator = sample_gen(5)
    next(generator)
    next(generator)
    print("We've yielded:", next(generator))
except StopIteration as e:
    print(f"The generator returned: {e.value}")
```

### Using Return Values with Subgenerators

Another case is when using subgenerators {cite}`pep-0380`. Following the PEP380 document, the expression of the form:

```python
result = yield from expression
```

will:
1. Yield the successive values of the `expression` generator,
2. Assign the return value from the `expression` generator function to `result`. 

Let us see that in a simple example:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 24,28,30,37

def fetch_data():
    # Simulate acquiring JSON data via HTTP
    load = [
        {
            "id": 1,
            "name": "User Random 1",
            "age": 20
        },
        {
            "id": 2,
            "name": "User Random 2",
            "age": 14
        },
        {
            "id": 3,
            "name": "User Random 3",
            "age": 56
        }
    ]
    
    adult_count = 0
    
    for d in load:
        yield d  # Stream each user record
        
        # Count adult users
        if d["age"] >= 18:
            adult_count += 1 # We count adults
    
    return adult_count  # Return summary

def process_users():
    """Process users and use the count"""
    print("Fetching users...")
    
    # Get both the yielded data AND the return value
    adult_users = yield from fetch_data()
    
    print(f"\n✓ Found {adult_users} adult users")
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]
def fetch_data():
    # Simulate acquiring JSON data via HTTP
    load = [
        {
            "id": 1,
            "name": "User Random 1",
            "age": 20
        },
        {
            "id": 2,
            "name": "User Random 2",
            "age": 14
        },
        {
            "id": 3,
            "name": "User Random 3",
            "age": 56
        }
    ]
    
    adult_count = 0
    
    for d in load:
        yield d  # Stream each user record
        
        # Count adult users
        if d["age"] >= 18:
            adult_count += 1
    
    return adult_count  # Return summary

def process_users():
    """Process users and use the count"""
    print("Fetching users...")
    
    # Get both the yielded data AND the return value
    adult_users = yield from fetch_data()
    
    print(f"\n✓ Found {adult_users} adult users")
```

```{list-table} An explanation of lines of code with subgenerator
:header-rows: 1
:name: code-explanation-subgenerator

* - **Line**
  - **Code**
  - **Explanation**
* - 24
  - ```python
    yield d
    ```
  - Here, we stream the value prepared by the generator
* - 30
  - ```python
    return adult_count
    ```
  - After counting all adults, we return the count
* - 37
  - ```python
    adult_users = yield from fetch_data()
    ```
  - We stream data produced by the `fetch_data()` generator iterator and assign to `adult_users` the value returned by the generator function
```

You can see that generators, as a kind of "resumable functions," tend to be useful. They can be seen as **data producers**, especially practical for heavy operations requiring significant computational or time resources, so each value is produced **on demand**. But the `yield` expression can also serve as a medium for two-way communication! See section below for details [Synchronous Coroutines](#synchronous-coroutines).

## Synchronous Coroutines

Here, we've arrived at the place where we first meet **coroutines**.

````{admonition} Curious about modern coroutines?
:class: important

Here, we are about to talk about simple synchronous coroutines by means of generator functions. The topic of coroutines in the modern sense is elaborated in the chapter [Coroutines](./coroutines.md).
````

````{admonition} What is a Coroutine?
:class: hint

A **coroutine**, by definition, is a subroutine (a function) that can be paused and resumed.
````

### Creating a Simple Coroutine

To create a coroutine, let us first create a simple generator. Let it yield successive odd numbers.

```{code-cell} python
:tags: ["remove-input", "remove-output"]
def odd_generator():
    i = 1
    while True:
        yield i
        i += 2
```

```{code-block} python
:lineno-start: 1

def odd_generator():
    i = 1
    while True:
        print(x)
        i += 2
```


```{code-cell} python
# We create a generator iterator
gen = odd_generator()

print(next(gen))
print(next(gen))
print(next(gen))
```

Now, let us use the `yield` expression so that the result of `yield i` is assigned to a variable:

```{code-cell} python
:tags: ["remove-input", "remove-output"]
def odd_generator():
    i = 1
    while True:
        x = yield i
        print(f"x={x}")
        i += 2
```

```{code-block} python
:lineno-start: 1
:emphasize-lines: 4

def odd_generator():
    i = 1
    while True:
        x = yield i
        print(f"x={x}")
        i += 2
```


```{code-cell} python
# We create a generator iterator
gen = odd_generator()

print(next(gen))
print(next(gen))
print(next(gen))
```

We can see some `None`s are displayed (due to the `print(x)` statement). So `yield i` streams the value of the `i` variable and evaluates to `None`. But our generator iterator **can consume some data** too! We can send data to the generator iterator via the `send()` method:

```{code-cell} python
yielded_val = gen.send(100)
print(yielded_val)
```

We can see that 100 was displayed (`print(x)` as `x` takes the sent value) and `yielded_val` takes another odd value, as this is the value produced by our coroutine. We can always resign from yielding any value and just rely on values sent to the coroutine:


```{code-cell} python
:tags: ["remove-input", "remove-output"]
def my_coroutine():
    while True:
        x = yield
        print(f"x={x}")
```

```{code-block} python
:lineno-start: 1
:emphasize-lines: 3

def my_coroutine():
    while True:
        x = yield
        print(f"x={x}")
```

```{code-cell} python
# We create a generator iterator
cor = my_coroutine()

print(next(cor))  # Notice the coroutine does not produce any value
cor.send(100)
```

````{admonition} Coroutine Needs to Be "Started"
:class: warning

To be able to send any value to a coroutine, you need to run `next()` once to initialize the coroutine (represented as generator iterator) properly and reach the `yield` statement where the coroutine expects input. If you do `cor.send()` before calling `next()`, it will result in a `TypeError` with the message "*can't send non-None value to a just-started generator*".
````

### Throwing Exceptions into Coroutines

Similarly to sending data, we may force an exception to be raised. To achieve that, we will use the `throw` method of a coroutine:

```{code-cell} python
:tags: ["remove-input", "remove-output"]
def my_coroutine():
    while True:
        try:
            x = yield
        except Exception as e:
            print(f"Caught an exception: {e}")
        else:
            print(f"Received: {x}")
```


```{code-block} python
:lineno-start: 1
:emphasize-lines: 4
def my_coroutine():
    while True:
        try:
            x = yield # Here the error will be thrown
        except Exception as e:
            print(f"Caught an exception: {e}")
        else:
            print(f"Received: {x}")
```            


```{code-cell} python
cor = my_coroutine()

next(cor)  # remember! 
cor.throw(ValueError("my exception"))
```

````{admonition} Throw Only Exceptions!
:class: warning

The `throw` method of a coroutine accepts only subclasses of `BaseException`!
````

### Closing Coroutines

A coroutine (hence a generator iterator with which we interact via `send`, `throw`, and `close` methods) can be closed, meaning it is flagged as not consuming values anymore. You close a coroutine using the `close` method, which internally raises the [`GeneratorExit`](https://docs.python.org/3/library/exceptions.html#GeneratorExit) exception.

```{code-cell} python
:tags: ["remove-input", "remove-output"]
def my_coroutine():
    try:
        while True:
            try:
                x = yield
            except Exception as e:
                print(f"Caught an exception: {e}")
            else:
                print(f"Received: {x}")
    except GeneratorExit:
        print("Generator is closing")
```

```{code-block} python
:lineno-start: 1
:emphasize-lines: 2,10
def my_coroutine():
    try:
        while True:
            try:
                x = yield
            except Exception as e:
                print(f"Caught an exception: {e}")
            else:
                print(f"Received: {x}")
    except GeneratorExit:
        print("Generator is closing")
```



```{code-cell} python
cor = my_coroutine()

next(cor) 
cor.close()
```

````{admonition} Do Not Operate on Closed Coroutines!
:class: warning

When you `close()` a coroutine, you cannot `send()` to it anymore.
````

You can see that sending data into a closed coroutine raises an error:

```{code-cell} python
:tags: ["raises-exception"]
cor = my_coroutine()
next(cor) 
cor.close()
cor.send("Some message")
```

````{admonition} Async Generators
:class: important
Generators can also be asynchronous. The semantics were proposed in PEP 525 {cite}`pep-0525` and they rely on asynchronous functions (`async def`).
````
