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

# Iterators

## Introduction

**Iterating** means doing something repeatedly {cite}`CambridgeDict_iteration`, and in software development, it typically refers to accessing data elements one by one. An **iterator** is an object that enables iteration over a collection or stream of data {cite}`PythonDocs_Iterator`. 

````{admonition} Iterator
:class: tip

Iterators provide a mechanism to **access items sequentially** (one-by-one) from an **iterable source of data**, such as a stream or collection (e.g., a dictionary or list).
````

This raises an important question: what qualifies as an *iterable source of data*?

````{admonition} Iterable source of data
:class: hint

An iterable source of data is any source from which elements can be retrieved sequentially. Syntactically, it is an object that implements the `__iter__` method (see [Iterable sources of data](#iterable-sources-of-data)).
````

Iterators are most commonly encountered in `for` loops. By convention, when looping over an object:

```{code-block} python
:lineno-start: 1

for item in my_collection:
    print(item)
```

Python internally transforms this into the following equivalent code:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 1,4,6

iterator = iter(my_collection)
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

This transformation demonstrates how Python uses iterators under the hood. To access successive values from a collection, we use an **iterator** object that must comply with the iterator protocol (see [Iterator protocol](#iterator-protocol)).

This logic can be seen in the example below:

```{raw} html
<div class="iterator-viz-wrapper">
    <style>
        .iterator-viz-wrapper * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        .iterator-viz-wrapper {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .iterator-viz-wrapper .container {
            background: white;
            border-radius: 20px;
            padding: 00px;
            box-shadow: 0 0 0 rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
        }

        .iterator-viz-wrapper h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }

        .iterator-viz-wrapper .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-style: italic;
        }

        .iterator-viz-wrapper .stream-container {
            background: linear-gradient(to bottom, #e3f2fd 0%, #bbdefb 100%);
            border: 3px solid #2196f3;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            position: relative;
            min-height: 200px;
            overflow: hidden;
        }

        .iterator-viz-wrapper .stream-label {
            position: absolute;
            top: 10px;
            left: 15px;
            background: #2196f3;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }

        .iterator-viz-wrapper .droplets {
            display: flex;
            gap: 15px;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 40px;
        }

        .iterator-viz-wrapper .droplet {
            width: 60px;
            height: 70px;
            background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            position: relative;
            animation: iterator-viz-float 2s ease-in-out infinite;
            transition: background 0.3s, opacity 0.3s, box-shadow 0.3s;
        }

        .iterator-viz-wrapper .droplet span {
            transform: rotate(45deg);
            color: white;
            font-weight: bold;
            font-size: 18px;
            transition: color 0.3s;
        }

        .iterator-viz-wrapper .droplet.processed {
            background: linear-gradient(135deg, #b0bec5 0%, #78909c 100%);
            opacity: 0.7;
            animation: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .iterator-viz-wrapper .droplet.active {
            background: linear-gradient(135deg, #ffee58 0%, #fdd835 100%);
            box-shadow: 0 0 15px 5px rgba(253, 216, 53, 0.7);
            animation: iterator-viz-pulse 1.2s ease-in-out infinite;
            z-index: 10;
        }

        .iterator-viz-wrapper .droplet.active span {
            color: #333;
        }
        
        @keyframes iterator-viz-float {
            0%, 100% { transform: rotate(-45deg) translateY(0px); }
            50% { transform: rotate(-45deg) translateY(-5px); }
        }

        @keyframes iterator-viz-pulse {
            0%, 100% {
                transform: rotate(-45deg) translateY(0px) scale(1);
            }
            50% {
                transform: rotate(-45deg) translateY(-5px) scale(1.1);
            }
        }

        .iterator-viz-wrapper .empty-message {
            text-align: center;
            color: #999;
            font-size: 18px;
            font-style: italic;
            margin-top: 50px;
            display: none;
        }

        .iterator-viz-wrapper .empty-message.visible {
            display: block;
            animation: iterator-viz-fadeIn 0.5s ease-in;
        }

        @keyframes iterator-viz-fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .iterator-viz-wrapper .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 20px;
        }

        .iterator-viz-wrapper button {
            background: #2196f3;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }

        .iterator-viz-wrapper button:hover {
            background: #1976d2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4);
        }

        .iterator-viz-wrapper button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .iterator-viz-wrapper .code-display {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 16px;
            margin-top: 20px;
            line-height: 1.6;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        .iterator-viz-wrapper .code-line {
            margin: 8px 0;
            opacity: 0;
            animation: iterator-viz-slideIn 0.4s ease-out forwards;
        }

        .iterator-viz-wrapper .code-line.error {
            color: #f48771;
        }

        @keyframes iterator-viz-slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .iterator-viz-wrapper .method {
            color: #dcdcaa;
        }

        .iterator-viz-wrapper .value {
            color: #ce9178;
        }

        .iterator-viz-wrapper .comment {
            color: #6a9955;
        }

        .iterator-viz-wrapper .keyword {
            color: #569cd6;
        }

        .iterator-viz-wrapper .info-box {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
        }

        .iterator-viz-wrapper .info-box.empty {
            background: #f8d7da;
            border-color: #f5c6cb;
        }
    </style>

    <div class="container">
        <p class="subtitle">Iterating through data accessible via <code>iterator</code></p>

        <div class="controls">
            <button id="iteratorGetBtn" onclick="iteratorGetNextValue()">Call <code>next(iterator)</code></button>
            <button id="iteratorResetBtn" onclick="iteratorResetStream()">Reset</button>
        </div>

        <div class="stream-container">
            <div class="stream-label">Data Stream/Collection</div>
            <div class="droplets" id="iteratorDroplets"></div>
            <div class="empty-message" id="iteratorEmptyMsg">💧 Iterator is exhausted - no more data to retrieve</div>
        </div>

        <div class="code-display" id="iteratorCodeDisplay">
            <div class="code-line"><span class="comment"># Click "Call next(iterator)" to retrieve values from the collection</span></div>
        </div>

        <div class="info-box" id="iteratorInfoBox">
            <strong>ℹ️ How it works:</strong> Each droplet represents a data value in the collection. 
            Calling <code>next(iterator)</code> <strong>points to</strong> and retrieves the next value in sequence. The original collection remains unchanged.
        </div>
    </div>

    <script>
        (function() {
            let streamData = [1, 2, 3, 4];
            let currentIndex = 0;

            function initializeStream() {
                const dropletsContainer = document.getElementById('iteratorDroplets');
                dropletsContainer.innerHTML = '';
                
                streamData.forEach((value, index) => {
                    const droplet = document.createElement('div');
                    droplet.className = 'droplet';
                    droplet.id = `iterator-droplet-${index}`;
                    droplet.innerHTML = `<span>${value}</span>`;
                    droplet.style.animationDelay = `${index * 0.1}s`;
                    dropletsContainer.appendChild(droplet);
                });
            }

            window.iteratorGetNextValue = function() {
                const codeDisplay = document.getElementById('iteratorCodeDisplay');
                const emptyMsg = document.getElementById('iteratorEmptyMsg');
                const infoBox = document.getElementById('iteratorInfoBox');
                
                if (currentIndex > 0) {
                    const prevDroplet = document.getElementById(`iterator-droplet-${currentIndex - 1}`);
                    if (prevDroplet) {
                        prevDroplet.classList.remove('active');
                        prevDroplet.classList.add('processed');
                    }
                }

                if (currentIndex < streamData.length) {
                    const value = streamData[currentIndex];
                    
                    const droplet = document.getElementById(`iterator-droplet-${currentIndex}`);
                    droplet.classList.add('active');
                    
                    setTimeout(() => {
                        const codeLine = document.createElement('div');
                        codeLine.className = 'code-line';
                        codeLine.innerHTML = `item = <span class="method">next</span>(iterator) <span class="comment"># Retrieved: <span class="value">${value}</span></span>`;
                        codeDisplay.appendChild(codeLine);
                        codeDisplay.scrollTop = codeDisplay.scrollHeight;
                    }, 100);
                    
                    currentIndex++;
                    
                    if (currentIndex >= streamData.length) {
                        setTimeout(() => {
                            emptyMsg.classList.add('visible');
                            infoBox.className = 'info-box empty';
                            infoBox.innerHTML = '<strong>⚠️ Iterator Exhausted:</strong> All values have been retrieved. The collection itself is still full, but the iterator has no more items. Calling <code>next(iterator)</code> again will raise a <code>StopIteration</code> exception.';
                        }, 500);
                    }
                } else {
                    const codeLine = document.createElement('div');
                    codeLine.className = 'code-line error';
                    codeLine.innerHTML = `item = <span class="method">next</span>(iterator) <span class="comment"># Raises:</span><br><span class="keyword">StopIteration</span>: `;
                    codeDisplay.appendChild(codeLine);
                    codeDisplay.scrollTop = codeDisplay.scrollHeight;

                    if (currentIndex > 0) {
                         const prevDroplet = document.getElementById(`iterator-droplet-${currentIndex - 1}`);
                         if (prevDroplet) {
                             prevDroplet.classList.remove('active');
                             prevDroplet.classList.add('processed');
                         }
                    }
                }
            };

            window.iteratorResetStream = function() {
                currentIndex = 0;
                const emptyMsg = document.getElementById('iteratorEmptyMsg');
                const codeDisplay = document.getElementById('iteratorCodeDisplay');
                const infoBox = document.getElementById('iteratorInfoBox');
                const getBtn = document.getElementById('iteratorGetBtn');
                
                emptyMsg.classList.remove('visible');
                
                codeDisplay.innerHTML = '<div class="code-line"><span class="comment"># Iterator reset. The collection was never changed!</span></div>';
                infoBox.className = 'info-box';
                infoBox.innerHTML = '<strong>ℹ️ How it works:</strong> Each droplet represents a data value in the collection. Calling <code>next(iterator)</code> and retrieves the next value in sequence. The original collection remains unchanged.';
                
                getBtn.disabled = false;
                
                initializeStream();
            };

            initializeStream();
        })();
    </script>
</div>
```

## Iterating over an object

An **iterator** object has a straightforward requirement: it must implement the dunder `__next__` method with the following signature:

```{code-block} python
:lineno-start: 1

from typing import Any

class MyDummyIterator:

    def __next__(self) -> Any:
        pass

```

This is an argumentless[^argumentless] method whose purpose is to produce successive elements from a collection or stream of data. When the iterator is exhausted, it must raise a [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception.

````{admonition} Exhausted iterator
:class: important

An **exhausted** iterator has no more data to return. Once exhausted, each successive call to the `__next__` method must raise the built-in [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception. Violating this requirement will cause the iterator to malfunction and prevent the `for` loop from terminating properly.
````

Consider the following example, which appears to work correctly:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 8

class MyIterator:
    def __next__(self):
        return 1

class SomeIterableCollection:

    def __iter__(self):
        return MyIterator()

for item in SomeIterableCollection(): 
    print(item) 
```

However, Python will not recognize this as a proper iterator:

```{code-block} python
:lineno-start: 1
:tags: ["raises-exception"]

from collections.abc import Iterator

class MyIterator:

    def __next__(self):
        return 1

assert isinstance(MyIterator(), Iterator)
```

Why does this assertion fail? Python requires iterators to follow the complete iterator protocol (see [Iterator protocol](#iterator-protocol)), which demands that **iterators must themselves be iterable objects**. This ensures iterators can be used seamlessly in `for` loops. The example above violates this requirement, as demonstrated when attempting to iterate directly over the iterator:

```{code-block} python
:lineno-start: 1

class MyIterator:

    def __next__(self):
        return 1

for item in MyIterator():
    print(item)
```

```{code-cell} python
:tags: ["remove-input","raises-exception"]
from collections.abc import Iterator

class MyIterator:

    def __next__(self):
        return 1

for item in MyIterator():
    print(item)
```

## Iterator protocol

To make an iterator a proper iterable object, two methods must be implemented:

1. `__next__(self)` — returns the next element of an iterator
2. `__iter__(self)` — returns an iterator (conventionally, the object itself)

With both methods implemented correctly, the following code executes without error:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 3,4

class MyIterator:

    def __iter__(self):
        return self

    def __next__(self):
        # This is an infinite iterator that never raises StopIteration
        return 1 

for item in MyIterator():
    print(item)
```

We can verify this implementation satisfies the iterator protocol:

```{code-block} python
:lineno-start: 1

from collections.abc import Iterator

assert isinstance(MyIterator(), Iterator)
```

````{admonition} Iterator subclassing
:class: important

As demonstrated above, subclassing the [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) abstract class is not required to create an iterator[^no_subclass] {cite}`python:abc_collections`. However, using the [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) module is recommended when working with collections and iterators. When explicitly subclassing [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator), the `__iter__` method need not be implemented explicitly, as the superclass provides it as a mixin method.

```{code-block} python
:lineno-start: 1
:emphasize-lines: 3

from collections.abc import Iterator

class MyIterator(Iterator):

    def __next__(self):
        # Note: this is an infinite iterator
        # as it never raises StopIteration exception
        return 1
```
````

[^argumentless]: An argumentless method is one that takes no explicit arguments beyond the implicit `self` or `cls` argument, which refers to the instance or type invoking the method.

[^abstract]: An abstract method is one that must be implemented in a subclass before an instance of that class can be created.

[^no_subclass]: The ability to check `isinstance` against [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) without explicit subclassing is not magical. The [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) abstract class implements a special `__subclasshook__` method that checks whether a class implements both `__iter__` and `__next__` methods.

## Iterable sources of data

Having established how iterators work, let us examine iterable sources of data in greater detail. An object is iterable if it satisfies at least one of the following conditions {cite}`pep-0234`:

1. The object implements the `__getitem__` dunder method for data access (i.e., it is a sequential or mapping collection {cite}`python:abc_collections`):

```{code-cell} python
my_list = [1, 2, 3]
idx = 1
item = my_list[idx]  # equivalent to my_list.__getitem__(idx)
assert item == 2
```

2. The object implements the `__iter__` dunder method, which returns an **iterator** object (an instance of a type compliant with the [Iterator Protocol](#iterator-protocol)):

```{code-cell} python
from collections.abc import Iterator

my_list = [1, 2, 3]
list_iter = iter(my_list)  # or my_list.__iter__()
assert isinstance(list_iter, Iterator)
```
