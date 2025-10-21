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

**Iterating** means doing something again and again {cite}`CambridgeDict_iteration` and in the context of software development it usually means accessing the piece of data one by one. **Iterator** hence, is an object which enables **iterating** over some collection or stream of data {cite}`PythonDocs_Iterator`. 

````{admonition} Iterator
:class: tip

In short, an iterators equip us with the mechanism to **access sequentially items** (one-by-one) from some **iterable source of data** such as a stream or a collection (e.g. a dictionary or a list).
````

We mentioned about *iterable source of data**, but what actually is it?

````{admonition} Iterable source of data
:class: hint

Iterable source of data is a source of data we can iterate over, so we can take one by one element. Syntahtically it is an object having implementation of `__iter__` method (see [Iterable source of data](#itreable-object))
````

Iterators are commonly used in `for` loop. By convention, looping over some object (if supported):

```{code-block} python
:lineno-start: 1

for item in my_collection:
    print(item)
```

is equivalent to the code:

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

That logic can be visible in the example below:




```{raw} html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-R-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #ffffff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 0 0 rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-style: italic;
        }

        .stream-container {
            background: linear-gradient(to bottom, #e3f2fd 0%, #bbdefb 100%);
            border: 3px solid #2196f3;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            position: relative;
            min-height: 200px;
            overflow: hidden;
        }

        .stream-label {
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

        .droplets {
            display: flex;
            gap: 15px;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 40px;
        }

        .droplet {
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
            animation: float 2s ease-in-out infinite;
            transition: background 0.3s, opacity 0.3s, box-shadow 0.3s;
        }

        .droplet span {
            transform: rotate(45deg);
            color: white;
            font-weight: bold;
            font-size: 18px;
            transition: color 0.3s;
        }

        /* --- MODIFIED/NEW STYLES --- */

        /* Style for droplets that have been processed */
        .droplet.processed {
            background: linear-gradient(135deg, #b0bec5 0%, #78909c 100%);
            opacity: 0.7;
            animation: none; /* Stop floating */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Style for the currently active/retrieved droplet */
        .droplet.active {
            background: linear-gradient(135deg, #ffee58 0%, #fdd835 100%);
            box-shadow: 0 0 15px 5px rgba(253, 216, 53, 0.7); /* Yellow glow */
            animation: pulse 1.2s ease-in-out infinite; /* New pulse animation */
            z-index: 10;
        }

        .droplet.active span {
            color: #333; /* Darker text for yellow background */
        }
        
        /* Original float animation for unprocessed droplets */
        @keyframes float {
            0%, 100% { transform: rotate(-45deg) translateY(0px); }
            50% { transform: rotate(-45deg) translateY(-5px); }
        }

        /* New pulse animation for the active droplet */
        @keyframes pulse {
            0%, 100% {
                transform: rotate(-45deg) translateY(0px) scale(1);
            }
            50% {
                transform: rotate(-45deg) translateY(-5px) scale(1.1);
            }
        }
        
        /* Removed @keyframes drip */

        /* --- END MODIFIED STYLES --- */

        .empty-message {
            text-align: center;
            color: #999;
            font-size: 18px;
            font-style: italic;
            margin-top: 50px;
            display: none;
        }

        .empty-message.visible {
            display: block;
            animation: fadeIn 0.5s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 20px;
        }

        button {
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

        button:hover {
            background: #1976d2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4);
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .code-display {
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

        .code-line {
            margin: 8px 0;
            opacity: 0;
            animation: slideIn 0.4s ease-out forwards;
        }

        .code-line.error {
            color: #f48771;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .method {
            color: #dcdcaa;
        }

        .value {
            color: #ce9178;
        }

        .comment {
            color: #6a9955;
        }

        .keyword {
            color: #569cd6;
        }

        .info-box {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
        }

        .info-box.empty {
            background: #f8d7da;
            border-color: #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="subtitle">Iterating through data in <code>my_collection</code></p>

        <div class="controls">
            <button id="getBtn" onclick="getNextValue()">Call <code>next(my_collection)</code></button>
            <button id="resetBtn" onclick="resetStream()">Reset</button>
        </div>

        <div class="stream-container">
            <div class="stream-label">Data Stream/Collection</div>
            <div class="droplets" id="droplets"></div>
            <div class="empty-message" id="emptyMsg">💧 Iterator is exhausted - no more data to retrieve</div>
        </div>

        <div class="code-display" id="codeDisplay">
            <div class="code-line"><span class="comment"># Click "Call next(my_collection)" to retrieve values from the collection</span></div>
        </div>

        <div class="info-box" id="infoBox">
            <strong>ℹ️ How it works:</strong> Each droplet represents a data value in the collection. 
            Calling <code>next(my_collection)</code> <strong>points to</strong> and retrieves the next value in sequence. The original collection remains unchanged.
        </div>
    </div>

    <script>
        let streamData = [1, 2, 3, 4];
        let currentIndex = 0;

        function initializeStream() {
            const dropletsContainer = document.getElementById('droplets');
            dropletsContainer.innerHTML = '';
            
            streamData.forEach((value, index) => {
                const droplet = document.createElement('div');
                droplet.className = 'droplet';
                droplet.id = `droplet-${index}`;
                droplet.innerHTML = `<span>${value}</span>`;
                droplet.style.animationDelay = `${index * 0.1}s`;
                dropletsContainer.appendChild(droplet);
            });
        }

        function getNextValue() {
            const codeDisplay = document.getElementById('codeDisplay');
            const emptyMsg = document.getElementById('emptyMsg');
            const infoBox = document.getElementById('infoBox');
            
            // --- NEW LOGIC ---
            // 1. Find and update the *previous* droplet
            if (currentIndex > 0) {
                const prevDroplet = document.getElementById(`droplet-${currentIndex - 1}`);
                if (prevDroplet) {
                    prevDroplet.classList.remove('active');
                    prevDroplet.classList.add('processed');
                }
            }
            // --- END NEW LOGIC ---

            if (currentIndex < streamData.length) {
                const value = streamData[currentIndex];
                
                // --- MODIFIED LOGIC ---
                // 2. Find and highlight the *current* droplet
                const droplet = document.getElementById(`droplet-${currentIndex}`);
                droplet.classList.add('active'); // Add 'active' class
                // --- END MODIFIED LOGIC ---
                
                // Add code line
                setTimeout(() => {
                    const codeLine = document.createElement('div');
                    codeLine.className = 'code-line';
                    codeLine.innerHTML = `item = <span class="method">next</span>(my_collection) <span class="comment"># Retrieved: <span class="value">${value}</span></span>`;
                    codeDisplay.appendChild(codeLine);
                    codeDisplay.scrollTop = codeDisplay.scrollHeight;
                }, 100);
                
                currentIndex++;
                
                // Check if iterator is exhausted
                if (currentIndex >= streamData.length) {
                    setTimeout(() => {
                        emptyMsg.classList.add('visible');
                        infoBox.className = 'info-box empty';
                        // --- MODIFIED TEXT ---
                        infoBox.innerHTML = '<strong>⚠️ Iterator Exhausted:</strong> All values have been retrieved. The collection itself is still full, but the iterator has no more items. Calling <code>next(my_collection)</code> again will raise a <code>StopIteration</code> exception.';
                        // --- END MODIFIED TEXT ---
                    }, 500);
                }
            } else {
                // Iterator is empty - show StopIteration
                const codeLine = document.createElement('div');
                codeLine.className = 'code-line error';
                codeLine.innerHTML = `item = <span class="method">next</span>(my_collection) <span class="comment"># Raises:</span><br><span class="keyword">StopIteration</span>: iterator exhausted`;
                codeDisplay.appendChild(codeLine);
                codeDisplay.scrollTop = codeDisplay.scrollHeight;

                // --- NEW LOGIC ---
                // Clean up the last active item
                if (currentIndex > 0) {
                     const prevDroplet = document.getElementById(`droplet-${currentIndex - 1}`);
                     if (prevDroplet) {
                         prevDroplet.classList.remove('active');
                         prevDroplet.classList.add('processed');
                     }
                }
                // --- END NEW LOGIC ---
            }
        }

        function resetStream() {
            currentIndex = 0;
            const emptyMsg = document.getElementById('emptyMsg');
            const codeDisplay = document.getElementById('codeDisplay');
            const infoBox = document.getElementById('infoBox');
            const getBtn = document.getElementById('getBtn');
            
            emptyMsg.classList.remove('visible');
            
            // --- MODIFIED TEXT ---
            codeDisplay.innerHTML = '<div class="code-line"><span class="comment"># Iterator reset. The collection was never changed!</span></div>';
            infoBox.className = 'info-box';
            infoBox.innerHTML = '<strong>ℹ️ How it works:</strong> Each droplet represents a data value in the collection. Calling <code>next(my_collection)</code> <strong>points to</strong> and retrieves the next value in sequence. The original collection remains unchanged.';
            // --- END MODIFIED TEXT ---
            
            getBtn.disabled = false;
            
            initializeStream();
        }

        // Initialize on load
        initializeStream();
    </script>
</body>
</html>
```

And to access successive values we use an **iterator** object which needs to be compliant with iterator protocol.

## Iterating over an object
**Iterator** object has quite trivial requirement to be satisfied to be an iterator: it needs to implement a dunder `__next__` method. It has the following signature:


```{code-block} python
:lineno-start: 1


from typing import Any

class MyDummyIterator:

    def __next__(self) -> Any:
        pass

```

So it is argumentless[^argumentless] method whose purpose is to produce the successive element of a collection or stream of data and raises [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception when iterator is exhausted.


````{admonition} Exhausted iterator
:class: important

If an iterotr is **exhausted** means it has no next data to return. If so, each successive call of `__next__` method must raise the built-in [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception. If you violate that requirement, iterator will not work properly and does not exit the `for` loop when iteration is finished! 
````

That would work, as visible in the example below:


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

however, by convention, Python will not treat it as iterator:


```{code-block} python
:lineno-start: 1
:tags: ["raises-exception"]

from collection.abc import Iterator

class MyIterator:

    def __next__(self):
        return 1

assert isinstance(MyIterator, Iterator)
```

why? because Python expects ietrator to follow exactly the specified iterator protocol (see [Iterator Protocl](#iterator-protocol)) which requires **iterators to be iterable** objects themselves! so we can use iterator object in `for` loop seamlessly. For that case above it is not true:


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

## Iterator Protocol

To make iterator an iterable object itself, two methods need to be implemented:

1. `__next__(self)` to access the subseqent element
2. `__iter__(self)` to return an iterator (usually itself)


With those two method implemented properly the following piece of code will work smoothly:

```{code-block} python
:lineno-start: 1
:emphasize-lines: 4

class MyIterator:

    def __iter__(self):
        return self

    def __next__(self):
        # that's infinit iterator, it never raises StopIteration exception
        return 1 

for item in MyIterator():
    print(item)
```

and we can verify that:

```{code-block} python
:lineno-start: 1

from collections.abc import Iterator

assert isinstance(MyIterator(), Iterator)
```


````{admonition} Iterator subclassing
:class: important

It is not necessery (as you've seen above) to subclass [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) abstract class to make na iterator[^no_subclass] {cite}`python:abc_collections` but I will encourage you to explot [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) package when dealing with collections ietrators and all similar stuff. If we explicitly subclass [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator), we don't need to implement `__iter__` method explicitly as it is provided by the superclass as mixin method.

```{code-block} python
:lineno-start: 1
:emphasize-lines: 4

from collections.abc import Iterator

class MyIterator(Iterator):

    def __next__(self):
        # note, again we have an inifite iterator
        # as it never raises StopIteration exception
        return 1
```
````


[^argumentless]: I refer to argumentless method to methods which do not take any explicit arguments, namely they have only `self` or `cls` argument passed implicitly refering to the object or type invoking the given method. 

[^abstract]: Don't know what abstract method is? It is a method which must be implemented (in subclass) in order to create an instance of this class. 

[^no_subclass]: There is no magic behind checking against being an instace of [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) without subclassing. The [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator) abstract class just implements special `__subclasshook__` which ckecks is a class implements `__iter__` and `__next__` methods. 

## Itreable sources of data
Let us explore a bit more iterables source of data. A source of data can be iterated over (**is iterable**) if at least one out of two below cases is satisfied {cite}`pep-0234`:

1. an object implements a special (dunder) method `__getitem__` for accessing data (so in short, it is a sequenctail or mapping collection {cite}`python:abc_collections`),


```{code-cell} python
my_list = [1, 2, 3]
idx = 1
item = my_list[idx] # equivalent to my_list.__getitem__(idx)
assert item == 2
```

2. it implements a dunder `__iter__` method returning an **iterator** object (an instance of a type compliant with the [Iterator Protocol](#iterator-protocol)):


```{code-cell} python
from collections.abc import Iterator

my_list = [1, 2, 3]
list_iter = iter(my_list) # or my_list.__iter__()
assert isinstance(list_iter, Iterator)
```



````

