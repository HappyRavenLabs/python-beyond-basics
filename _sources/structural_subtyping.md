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

# Structural Subtyping

````{admonition} Meet generics first?
:class: important
It can be useful to learn first about [generics](./generics.md), especially the section describing [Variance types](./generics.md#variance-types).
````


## Nominal Subtyping
````{admonition} Subtyping?
:class: hint
**Subtyping** is the process of **creating a more specific type** from a broader one.
````

In software engineering, we have two principal ways of subtyping:
1. nominal (i.e., by name),
2. structural (i.e., by shape).

In Python, nominal subtyping is far more popular and widely used. It relies on direct inheritance/generalization relationships. We won't spend much time on this kind of subtyping since it's well-known and, if you're an experienced Python user, you've surely encountered and used it.

```{code-block} python
:lineno-start: 1
:emphasize-lines: 4

class User:
    pass

class AuthorizedUser(User):
    pass
```

```{list-table} A line-by-line explanation of nominal subtyping
:header-rows: 1
:name: code-explanation-nominal-subtyping

* - **Line**
  - **Code**
  - **Explanation**
* - 1
  - ```python
    class User
    ```
  - Here, we create a base class (superclass/broader type)
* - 4
  - ```python
    class AuthorizedUser(User):
    ```
  - Here, we explicitly state (in parentheses) that `AuthorizedUser` is a subtype of `User`
```

````{admonition} Multiple inheritance/MRO
:class: tip
Python supports multiple inheritance. In that case, methods are searched according to a predefined order. See the example below:

```python
class A:
    pass

class B:
    pass

class C(A, B):
    ...

print(C.__mro__)
```
This results in a tuple like:

```
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)
```
showing the order of method lookup. Methods are searched among superclasses **from left to right**. See [`__mro__`](./special_attributes.md#mro)

````

````{admonition} Important!
:class: warning
Subtyping represents an **asymmetrical relationship**. This means `AuthorizedUser` is a `User` (it's a specific type of user), but the reverse is not true, a `User` is not necessarily an `AuthorizedUser`. Formally, if S is a subtype of T (written S <: T), you can use S wherever T is expected, but not vice versa.
````

## Protocol Definition
Python, beginning with version 3.8, officially introduced structural subtyping via PEP 544 {cite}`pep-0544` by introducing protocols. Let's start with a definition:

````{admonition} Structural Subtyping
:class: note
**Structural subtyping** is based **only** on following the same interface (implementing methods with **compatible** signatures) and (optionally) attributes. Unlike nominal subtyping, no explicit inheritance relationship is required.
````
You might ask, why do we need it at all? Sometimes you don't need or even can't inherit directly from a broader type. This happens when:
1. you work with legacy classes or third-party library classes you can't modify,
2. you want to decouple the interface from implementation (by creating protocols independent of class hierarchies),
3. you need static type checking for duck-typed code,
4. you create callbacks or plugins without needing to import or inherit from a superclass.

Let's move to an example:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 3,6

class DataConnector:

    def connect(self, ip: str, port: int) -> None: 
        pass

    def retrieve(self) -> str:
        return ""

class WebPageConnector:

    def connect(self, ip: str, port: int) -> None: 
        return None

    def retrieve(self) -> str:
        return "<html></html>"

class DatabaseConnector:

    def connect(self, ip: str, port: int) -> None: 
        return None

    def retrieve(self) -> str:
        return "1, 2, 3"    

def process_data(conn: DataConnector):
    conn.connect("127.0.0.1", 8888)
    data = conn.retrieve()

process_data(DatabaseConnector())
```

In our example, we've created a class `DataConnector` and defined a pair of methods to be implemented. The classes `WebPageConnector` and `DatabaseConnector` follow that interface, but there's an issue here:


````{admonition} Static type check
:class: error
Though the code works and no error will be raised at runtime, static type checking (which is the pivotal aspect of structural subtyping) will fail in this case. Running the `mypy` tool to check our code, you'll see:

```
error: Argument 1 to "process_data" has incompatible type "DatabaseConnector"; expected "DataConnector"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```
This happens because static typing tools doesn't recognize `DataConnector` as it's structural supertype.
````

To solve this, PEP 544 introduced a special [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) class type hint that marks classes as interfaces for structural subtyping. Look at the refined implementation of the code above.


```{code-block} python
:lineno-start: 1
:emphasize-lines: 1,3,5,8

from typing import Protocol

class DataConnector(Protocol):

    def connect(self, ip: str, port: int) -> None: 
        ...

    def retrieve(self) -> str:
        ...

class WebPageConnector:

    def connect(self, ip: str, port: int) -> None: 
        return None

    def retrieve(self) -> str:
        return "<html></html>"

class DatabaseConnector:

    def connect(self, ip: str, port: int) -> None: 
        return None

    def retrieve(self) -> str:
        return "1, 2, 3"    

def process_data(conn: DataConnector):
    conn.connect("127.0.0.1", 8888)
    data = conn.retrieve()

process_data(DatabaseConnector())
```

Note that our protocol must inherit from [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) and, by convention, interface methods' bodies contain just the ellipsis (`...`) symbol. Let's explore the emphasized lines more deeply:


```{list-table} A line-by-line explanation of protocol definition
:header-rows: 1
:name: code-explanation-protocol

* - **Line**
  - **Code**
  - **Explanation**
* - 1
  - ```python
    from typing import Protocol
    ```
  - We need to import the `Protocol` type hint class first
* - 3
  - ```python
    class DataConnector(Protocol):
    ```
  - We use nominal subtyping (I know this can be confusing) to indicate our class will be used for structural subtyping
* - 5-6
  - ```python
    def connect(...) -> None:
        ...
    ```
  - By convention, protocol methods should contain no body except the ellipsis literal (`...`)
```


````{admonition} Use type hints
:class: important
Since structural subtyping relies on method signatures, don't forget to use type hints!
````

````{admonition} Signature matching requirements
:class: warning
To follow the structural subtyping mechanism, the entire signature must be **compatible**, including:
1.  **method name:** must match exactly.
2.  **parameters:** the number, order, and kinds (e.g., positional-only, keyword-only) of parameters must be compatible (the parameter *names* themselves do not need to match).
3.  **parameter types:** must be compatible (contravariant).
4.  **return type:** must be compatible (covariant).

Note: Parameter types are **contravariant** (can accept broader types/supertypes)[^why_contra] and return types are **covariant** (can accept narrower types/subtypes) in subtyping relationships.
````

[^why_contra]: This rule is essential for **substitutability** (part of the Liskov Substitution Principle). When a class follows a protocol, it makes a promise, or "contract". If the protocol requires a method `handle(item: Animal)`, it promises to handle *any* `Animal`. If an implementation tried to narrow this to `handle(item: Dog)`, it would break that promise. Code using the protocol could pass a `Cat` (which *is* an `Animal`), but the `Dog`-only implementation would fail. To be safely substitutable, the implementation's parameter type must be *at least as general* as the protocol's. It can be `Animal` (invariant) or a *supertype* like `object` (**contravariant**), but never a *subtype* like `Dog`.

````{admonition} Check if class implements a protocol
:class: hint
By default, you cannot use `isinstance` or `issubclass` checks to verify that a class implements a given protocol. Checks like:

```python
isinstance(DatabaseConnector(), DataConnector)
``` 
will fail unless you explicitly use the `@runtime_checkable` decorator from the `typing` module. However, that's not recommended as it might slow down your code and only performs shallow checks. It's better to use the `hasattr` method to check if a class has the requested method, or rely on static type checkers.
````

````{admonition} See also decorators
:class: seealso
To learn about decorators, see the [Decorators](./decorators.md) chapter!
````

## Protocol Attributes
Not only methods but also attributes can be indicators of structural subtyping. Let's slightly change our protocol so it has two attributes and the `connect` method becomes argument-free:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 4,5

from typing import Protocol

class DataConnector(Protocol):
    ip: str
    port: int

    def connect(self) -> None: 
        ...

    def retrieve(self) -> str:
        ...

```
Now, to satisfy the protocol, we need to either define the attributes at the class level or initialize them is `__init__` or making them properties (`@property`):

```{code-block} python
:lineno-start: 13
:emphasize-lines: 2,3,14,15

class WebPageConnector:
    ip: str = "127.0.0.1"
    port: int = 8888

    def connect(self) -> None: 
        return None

    def retrieve(self) -> str:
        return "<html></html>"

class DatabaseConnector:

    def __init__(self) -> None:
        self.ip = "127.0.0.1"
        self.port = 8889

    def connect(self) -> None: 
        return None

    def retrieve(self) -> str:
        return "1, 2, 3"    

def process_data(conn: DataConnector):
    conn.connect()
    data = conn.retrieve()

process_data(WebPageConnector())
process_data(DatabaseConnector())
```

````{admonition} Attribute variance
:class: warning
Attributes in protocols are **invariant** by default (see [Variance types](./generics.md#variance-types) in the [Generics](./generics.md) chapter to read more about variance types), meaning an exact type match is required. This is because mutable attributes can be both read from and written to, which requires invariance for type safety.

However, read-only attributes can be **covariant**. Use `@property` to make a read-only attribute:

```python
from typing import Protocol

class DataConnector(Protocol):

    @property
    def some_attribute(self) -> int:
        ...
```

Then any class following the `DataConnector` protocol should have a `some_attribute` property of type `int` or any subtype of `int`. The property ensures the attribute is read-only, allowing covariance without sacrificing type safety.
````