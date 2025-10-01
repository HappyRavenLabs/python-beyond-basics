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

# Special Attributes

In Python, all data types have a set of special attributes, commonly referred to as **dunder attributes**[^dunder].  
These attributes provide developers with useful metadata about Python objects. They follow the naming pattern `__attribute__` — with two leading and two trailing underscores where `attribute` is the name of the given dunder attribute.

Python’s built-in objects come with many such attributes. Some external libraries also define their own custom dunder attributes, but this practice is generally discouraged unless it is truly necessary and thoroughly documented {cite}`python:lexical_identifiers`.  

In this section, we will explore the most important core dunder attributes across different types of Python objects.

[^dunder]: The term **dunder** comes from **d**ouble **under**score.

## Of Modules

### `__name__`

The `__name__` attribute holds the name of a module.

```{admonition} What is a Python module?
:class: hint

Not sure what a Python module is? According to the official Python tutorial, a module is simply  
“[...] **a file** containing Python definitions and statements” {cite}`python:tutorial_modules`.
```

By default, the module name corresponds to the filename without the `.py` suffix {cite}`python:tutorial_modules`.

For example, consider the file `my_math.py`

```python
# file my_math.py

def multiply(a: int, b: int) -> int:
  return a * b
```

Now, if we import this module:

```python
import my_math
print(my_math.__name__)
```

The output will be:

```bash
my_math
```


**However**, there is a special case: the `__mame__` attribute takes the value: `__main__` when a module is executed directly {cite}`python:datamodel_specialnames`

Let's modify `my_math.py` to display the value of `__name__`:

```python
# file my_math.py
print(__name__)

def multiply(a: int, b: int) -> int:
  return a * b
```

If we now run:

```bash
python3 my_math.py
```

The output will be:

```
__name__
```

The same happens when you execute code passed as a string:

```bash
python -c "print(__name__)"
```

Output:
```
__name__
```

````{admonition} Did you know?
:class: hint

Because `__name__` is set to `__main__` only when a file is executed directly, you will often see Python code guarded like this:

```python
if __name__ == "__main__":
    ...
```

This pattern allows developers to include logic that should only run on direct execution, while preventing it from running when the file is imported as a module.
Let’s investigate with an example:

```{code-cell} python3
# file: my_math.py

def multiply(a: int, b: int) -> int:
  return a * b

if __name__ == "__main__":
    print("I'm executed directly!")
```

Now compare the two cases:
- running `python my_math.py` will print `I'm executed directly!`
- importing it inside a Python shell (or any module) with `import my_math` will print nothing
````



## Of Functions


## Of Methods


## Of Classes

## Of Objects

```{admonition} Everything is an Object in Python
:class: warning

If you are already experienced in Python, you probably know that literally **all data** in the Python ecosystem are **objects** {cite}`python:datamodel`. This means that modules, functions, methods, and classes **are themselves objects**, not just instances of classes (that, by the way, are objects too).

In this section, the "Of Objects" subsection covers the **core special attributes** that are fundamental to **all** Python objects. The previous subsections (Modules, Functions, Methods, Classes) describe **additional specialized attributes** specific to those object types. Therefore, objects of those types will have both the general object attributes listed here and their type-specific attributes described above.
```

## References
```{bibliography}
```