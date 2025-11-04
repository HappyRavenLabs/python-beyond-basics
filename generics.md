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

At the very beginning, let us follow a clear distinction made in {cite}`pep-0484` between **a class** and **a type**. 

````{admonition} A type
:class: note
**A type** is a variable or function annotation - a static attribute used for static type-checking. You cannot create instances of types!
````

````{admonition} A class
:class: note
**A class** is a kind of factory for creating instances; classes are a runtime concept! 
````

````{admonition} A class is a type
:class: important
**Every** class is also **a type**, but not vice-versa!
````


## Type Hints

Let us recall that Python supports type hints as a completely voluntary mechanism. As Python's makers claim that they will never be mandatory, they are nevertheless an extremely useful concept which (quite easily) enables programmers to avoid potentially catastrophic logical errors. 

To make this concrete, let us consider a banking system. Access to money should be granted only to an authorized user, let's say represented by an `AuthorizedUser` class, not just any `User` instance. Remember, Python does not require explicit types; hence, provided no extra validation logic is implemented, a program could accidentally grant access to an unauthorized user, leading to security vulnerabilities.

```python
class User:
    def __init__(self, name: str):
        self.name = name

class AuthorizedUser(User):
    def __init__(self, name: str, auth_token: str):
        super().__init__(name)
        self.auth_token = auth_token

def withdraw_money(user: AuthorizedUser, amount: float) -> bool:
    # Only authorized users should access this
    # Without type hints, any User could be passed here
    print(f"Withdrawing ${amount} for {user.name}")
    return True

regular_user = User("John")
withdraw_money(regular_user, 1000.0)  # Static-check type error!

# This is correct
authorized_user = AuthorizedUser("Jane", "token123")
withdraw_money(authorized_user, 1000.0)  # OK
```

Thanks to type hints, tools for static code analysis such as [MyPy](https://github.com/python/mypy) can capture such errors on demand.


````{admonition} Type hints
:class: hint

In Python, type hints are given after a `:` (colon) symbol just after the name of a variable or function parameter, or after `->` when representing the type returned by a function:

```python
age: int = 100  # we annotate `age` as a variable containing `int` values
```

or 

```python
def process(data: list, eps: float, title: str) -> str:
    # some logic here
    return f"Processed {title}"
```
````

## Type Aliases

When needed, we can define aliases for a type, e.g., to make code more meaningful:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 1

Minute = int

def sleep(time: Minute) -> None:
    # some logic here
    pass
```

In the above example, it is clear that the argument's integer value represents minutes, not seconds or milliseconds, so the code is clearer than:

```{code-block} python
:lineno-start: 1

def sleep(time_minutes: int) -> None:
    # some logic here
    pass
```

Let us now see another example:

```{code-block} python
:lineno-start: 1

Minute = int
Retry = int

def retry(backoff: Minute, max_retry: Retry) -> None:
    # some logic here
    pass
```

In the code above, nothing prevents us from running the code:

```{code-block} python
:lineno-start: 1

backoff_time: Minute = 10
retry_count: Retry = 5

# Accidentally swapping the arguments!
retry(retry_count, backoff_time)  # Static type checker won't complain!
```

As you can see, static type checking alone doesn't prevent this confusion because both are just `int` aliases. When you need static checking to ensure consistency, you can define simple superclasses to enforce the right types:

```{code-block} python
:lineno-start: 1

class Minute(int):
    pass

class Retry(int):
    pass
```

This forces you to create instances explicitly:

```{code-block} python
:lineno-start: 1

backoff_time: Minute = Minute(10)
retry_count: Retry = Retry(5)

# Now this will fail at runtime
retry(retry_count, backoff_time)  # TypeError!
```

Then, running:

```bash
mypy our_code.py
```

will result in the following errors:

```text
our_code.py:5: error: Argument 1 to "retry" has incompatible type "Retry"; expected "Minute"  [arg-type]
our_code.py:5: error: Argument 2 to "retry" has incompatible type "Minute"; expected "Retry"  [arg-type]
```

However, this approach requires extra computation at runtime, which is often unnecessary. Hence, you can define a new type using the [`NewType`](https://docs.python.org/3/library/typing.html#newtype) helper construct:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 3,4

from typing import NewType

Minute = NewType("Minute", int)
Retry = NewType("Retry", int)
```

Remember, `NewType` **must** take only a name (it should be the same as the variable it is assigned to) and its superclass!

````{admonition} NewType vs Real Classes
:class: warning
`NewType` is only for static type checking and cannot be subclassed. If you need inheritance, methods, or runtime behavior, use real class inheritance instead! `NewType` outputs cannot be used in subclassing or runtime checks with `isinstance`!
````

## What Are Generic Types?

First, let us see how the Cambridge Dictionary defines the adjective **generic** {cite}`CambridgeDict_generic`:

> *generic:* shared by, typical of, or relating to a whole group of similar things, rather than to any particular thing

How do we translate that into the language of programmers? Well, in software engineering we most frequently speak about **generic types** or **generic classes**. 

````{admonition} Generic types
:class: note
**Generic types** are types that are parameterized by other types, e.g., *a list of integers*, *a stack of strings*, or *a dictionary mapping strings to users*!
````

### Why Do We Need Generics?

Imagine you're building a data structure like a stack. Without generics, you might write `IntStack` class dealing with integers, but what if you need a stack of strings? Or floats? You'd have to write `StringStack`, `FloatStack`, etc. This is repetitive and error-prone. Generics solve this problem by allowing you to write **one** stack that works with **any** type, provided they share similar logic!

````{admonition} Generics vs Inheritance  
:class: note
**Generics** (`Stack[int]`, `Stack[str]`): Same behavior, different data types. Write one class, use it type-safely with many types.  
**Inheritance** (`Dog extends Animal`): Different behaviors. A `Dog` has specific methods that `Animal` doesn't.  
These are complementary tools - use generics to avoid duplication, use inheritance to specialize behavior!
````

## Creating a Generic

In Python, generic types are usually related to collections classes, e.g., *a set of floats* or *a stack of requests*, where we specify what type of objects a collection manages; or methods

Since Python 3.12, where a modern and simpler form of defining generics have been introduced by PEP695 {cite}`pep-0695`, we basically define generic class as:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 1

class Graph[T]:
    
    def __init__(self) -> None:
        self.nodes: list[T] = []
    
    def add(self, item: T) -> None:
        self.nodes.append(item)
    
    def get_all(self) -> list[T]:
        return self.nodes
```




and generic methods as:


```{code-block} python
:lineno-start: 1
:emphasize-lines: 1

def join[T](arg1: T, arg2: T) -> T:
    # some logic here
    return arg1
```

This mysterious variable  `T` in both listing is actually the placeholder for the type generic class or method is parametrized with, e.q. in the code below:

```python

res = join("a", "b")
```

the `T` will be set with `str` as we passed two string literals: `"a"` and `"b"`.



````{admonition} Mixed type in generic  
:class: note
Note that we can call `join(1, "b")` and [MyPy](https://github.com/python/mypy) will not complain. In this case, the placeholder parameter `T` is binded to the `object` type whose subclasses are both `int` and `str`. That is why static type not necesarily complains about it. You can check type binding by adding statement `reveal_type(res)`. Remember, it will not work on runtime and just on static type check with `mypy` command.
````


````{admonition} Type parameter name
:class: important
The name of type placeholder need not to be `T`. It actually can be arbitrary valid python identifier. If your generic class or function takes multiple parameter placeholder, they needs to be unique:

```{code-block} python
:lineno-start: 1

class MyClass[T1, T2]:
    pass
```

````


````{admonition} Parametrizing generics
:class: tip
With functions, we cannot explicitly state the type for generic — the type is inferred automatically - but for classes, we can. In fact, we can intialize our `Graph` class in multiple ways:

```{code-block} python
:lineno-start: 1
# All of these are valid
graph_1 = Graph()  # Type is inferred
graph_2: Graph[int] = Graph()  # Explicit annotation
graph_3 = Graph[int]()  # Runtime parameterization

# Usage
graph_2.add(42)  # OK
graph_2.add("hello")  # Type checker will complain!
```


````
## Constrained parameter type

## Types of Variance

Now that we understand generics, let's dive into a somewhat advanced aspect — **variance**. The term **variance** might sound kind of confusing, as it's usually associated with the statistical measure of data spread. However, in Python's type system, as clearly explained in PEP 483 {cite}`pep-0483`, there are three types of variance. In general, types can be:

1. **Covariant**
2. **Contravariant**
3. **Invariant**

Sounds mysterious? Let us see some real-world examples, quite far apart from the software development world:

```{list-table} Real-Life Analogies for Variance in Python
:header-rows: 1
:name: variance-real-life

* - **Type of Variance**
  - **Plain Explanation**
  - **Real-Life Analogy**

* - **Covariance**
  - You can **use something more specific** where something more general is expected.  
  - 🐶 **Example:** A **dog** is an **animal** beyond any doubt!  
    If a vet clinic says, "We treat all animals," you can bring your **dog** — that's perfectly fine.  
    The clinic expects an *animal* (general), and you provided a *dog* (specific).  
    → That's **covariance** in action.

* - **Contravariance**
  - You can **accept something more general** where something more specific is expected.  
  - 👩‍🏫 **Example:** Imagine a **teacher** who can teach **any student**, regardless of age or subject.  
    If a school says, "We need a **math teacher for high school students**," sending this general **teacher** still works — they can handle those students too. The teacher can *accept* a wider variety of students than what was specifically requested.  
    → That's **contravariance** — accepting something broader.

* - **Invariance**
  - Only an **exact type match** works — no substitutions allowed.  
  - 🐕 **Example:** A **dog bowl** is made **only for dogs**.  
    You can't use it for cats or generic animals — it's a strict fit.  
    Even though a dog *is* an animal, the bowl says "dog only."  
```

### Variance in Python Code

For Python generics, starting from Python 3.12, parameter type variance (e.g. `T` in our `class Graph[T]:` definitoon) is inferred automatically, unless specified explicitly. To specify it explicitly, we will use the [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar) object from [`typing`](https://docs.python.org/3/library/typing.html) built-in module.


```{code-block} python
:lineno-start: 1
:emphasize-lines: 1

from typing import TypeVar

T = TypeVar("T") # default = invariant
T = TypeVar("T", covariant=True) # covariant 
T = TypeVar("T", contravariant=True) # contravariant 
T = TypeVar("T", infer_variance=True) # infer automaticaaly based on logic of generic

T = TypeVar("T", contravariant=True, covariant=True) # error, cannot specify both at once
```

then we can use them excatly as in [Creating a generic](#creating-a-generic):

```{code-block} python
:lineno-start: 10

class Graph[T]:
    # the rest of the code
```

````{admonition} Default variance type
:class: important
The default type of variance in Python generics is **invariant**, meaning **exact match** is required. Use `covariant=True` for immutable containers and `contravariant=True` for consumer types.
````


## Upper-Bounded parameter type
We already know, that our generic will work without type-check complains with any kind (even mixture `int` and `str`) of type. There are, however, many cases, where the type needs to be limited, e.g. a generic method should be valid only for `str` and its subclasses. To achieve this, we can specify upper-bound for our parameter placeholder by means of type annotation. We just type-annotate our placeholder type:


```{code-block} python

class Graph[T: str]:
    # the rest of the code
```

and it will work in either case:

```{code-block} python
class Str2(str):
    pass

g1 = Graph[str]()
g2 = Graph[Str2]()
```


````{admonition} excplitc bound of type-var
:class: important
If using the older syntax with explicit [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar), you define upper bound in the following way:

```python
T = TypeVar("T", bound=str)
```

````

## Type constraints
Besides bounding generic type placeholder to a particular type (and its subtypes), we can also constraint it to two or more types. By constraining, we mean





````{admonition} excplitc constraints of type-var
:class: important
If using the older syntax with explicit [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar), you define constraitns as position variadic arguments:

```python
T = TypeVar("T", str, int)
```

Remember, you need to specify not less than **two** constraints!

````