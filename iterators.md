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

**Iterating** means doing something again and again {cite}`CambridgeDict_iteration` and in the context of software development it usually means accessing the piece of data one by one. **Iterator** hence, is an object which enables iterating over some collection or stream of data {cite}`PythonDocs_Iterator`. 

````{admonition} Iterator
:class: tip

In short, an iterators equip us with the mechanism to **access sequentially items** (one-by-one) from some source of data such as a stream or a collection (e.g. a dictionary or a list).
````

The iterator protocol was officially introduced with PEP234 {cite}`pep-0234` document.

When we use loops, an iterator for a collection is created implciitly

Look at the figure below to see some interactive visualisation of iterating process. We have some source of data we want to iterate over to query sequentially item by item. Our source can be an ordinary Python `list` or unbounded stream of data received over HTTP. 

````{admonition} Iteraetion does not change collection
:class: warning

Process of iteration does not alter the underlying source of data. It is completly different object.
````



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


## Iterator Protocol
Formally, in Python, iterator protocol is constituted by two dunder [^dunder] methods:

1. `__iter__`
2. `__next__`


[^dunder]: Don't remember what dunder methods are? See [Special Attributes](./special_attributes.md).



````{admonition} StopIteration"
:class: warning

When an iterator is exhausted and does not provide data anymore, it must raise [`StopIterator`](https://docs.python.org/3/library/exceptions.html#StopIteration) exception and keep raising it for subsequent calls.
````




## References
```{bibliography}
```