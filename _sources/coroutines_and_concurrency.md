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

# Coroutines & Concurrency

````{admonition} This chapter is not ready yet?
:class: important
Writing a book takes time and for that chapter I did not have enough of it. Please, return later.
````

<!-- ````{admonition} What is a Coroutine?
:class: hint

A **coroutine**, by definition, is a subroutine (a function) that can be paused and resumed.
```` -->


```{raw} html
<div id="async-timeline">
  <style>
    #async-timeline *{box-sizing:border-box;margin:0;padding:0}
    #async-timeline{font-family:'Roboto',sans-serif;background:#fff;display:flex;align-items:center;justify-content:center;padding:20px}
    #async-timeline .container{width:100%;max-width:1000px;background:#fff;padding:36px;border-radius:14px;border:1px solid #e6e6e6;box-shadow:0 6px 20px rgba(0,0,0,0.06)}
    #async-timeline h1{font-size:26px;color:#222;margin-bottom:6px;font-weight:500}
    #async-timeline .subtitle{color:#666;font-size:14px;margin-bottom:20px}
    #async-timeline .timeline-container{position:relative;padding-top:70px}
    #async-timeline .timeline-axis{position:absolute;top:10px;left:100px;right:0;height:20px;display:flex;justify-content:space-between;align-items:flex-end;color:#666;font-size:12px;z-index:1}
    #async-timeline .timeline-axis::after{content:"";position:absolute;bottom:-6px;left:0;right:0;height:2px;background:#eee}
    #async-timeline .task-row{display:flex;align-items:center;gap:16px;margin-bottom:18px;position:relative}
    #async-timeline .task-label{width:100px;font-weight:500;color:#333;font-size:14px;flex-shrink:0;text-align:right}
    #async-timeline .task-track{flex:1;height:48px;background:#f6f6f6;border-radius:24px;position:relative;overflow:visible}
    #async-timeline .task-segment{position:absolute;height:100%;left:0%;width:0%;opacity:0;border-radius:24px;box-shadow:0 6px 14px rgba(0,0,0,0.08);transition:width linear,opacity .12s linear,left 0s}
    #async-timeline .segment-processing{background:linear-gradient(135deg,#42a5f5 0%,#478ed1 100%)}
    #async-timeline .segment-http{background:linear-gradient(135deg,#ef5350 0%,#e53935 100%)}
    #async-timeline .segment-io{background:linear-gradient(135deg,#ffa726 0%,#fb8c00 100%)}
    #async-timeline .legend{margin-top:26px;padding-top:18px;border-top:1px solid #eee;display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
    #async-timeline .legend-item{display:flex;gap:8px;align-items:center;color:#666;font-size:13px}
    #async-timeline .legend-color{width:20px;height:20px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.06)}
    @media(max-width:480px){#async-timeline .task-label{width:76px;font-size:13px;text-align:right}}
  </style>

  <div class="container">
    <h1>Asynchronous Task Execution</h1>
    <div class="subtitle">Sequential CPU work, concurrent I/O & HTTP waits</div>

    <div class="timeline-container">
      <div class="timeline-axis">
        <div>0ms</div><div>200ms</div><div>400ms</div>
        <div>600ms</div><div>800ms</div><div>1000ms</div>
      </div>

      <div class="task-row">
        <div class="task-label">Task 1</div>
        <div class="task-track">
          <div class="task-segment segment-processing" id="t1-proc1"></div>
          <div class="task-segment segment-io" id="t1-io"></div>
          <div class="task-segment segment-processing" id="t1-proc2"></div>
        </div>
      </div>

      <div class="task-row">
        <div class="task-label">Task 2</div>
        <div class="task-track">
          <div class="task-segment segment-processing" id="t2-proc1"></div>
          <div class="task-segment segment-io" id="t2-io"></div>
          <div class="task-segment segment-processing" id="t2-proc2"></div>
          <div class="task-segment segment-http" id="t2-http"></div>
        </div>
      </div>

      <div class="task-row">
        <div class="task-label">Task 3</div>
        <div class="task-track">
          <div class="task-segment segment-processing" id="t3-proc"></div>
          <div class="task-segment segment-http" id="t3-http"></div>
        </div>
      </div>
    </div>

    <div class="legend">
      <div class="legend-item"><div class="legend-color segment-processing"></div><span>Processing</span></div>
      <div class="legend-item"><div class="legend-color segment-io"></div><span>I/O Wait</span></div>
      <div class="legend-item"><div class="legend-color segment-http"></div><span>HTTP Wait</span></div>
    </div>
  </div>

  <script>
    (function(){
      const root = document.querySelector('#async-timeline');
      const TL = 1000, SCALE = 10;
      let running = false, timer = null;

      function seg(el,start,dur){
        if(!el)return;
        const L = (start/TL)*100, W = (dur/TL)*100;
        const delay = start*SCALE, durReal = dur*SCALE;
        el.style.transition='none';
        el.style.left=L+'%'; el.style.width='0%'; el.style.opacity='1';
        setTimeout(()=>{
          el.style.transition=`width ${durReal}ms linear`;
          requestAnimationFrame(()=>{ el.style.width=W+'%'; });
        },delay);
      }

      function reset(){
        root.querySelectorAll('.task-segment').forEach(e=>{
          e.style.transition='none';
          e.style.width='0%';
          e.style.left='0%';
          e.style.opacity='0';
        });
      }

      function start(){
        if(running) return;
        running=true; reset();

        const t1p1=root.querySelector('#t1-proc1'),
              t1io=root.querySelector('#t1-io'),
              t1p2=root.querySelector('#t1-proc2'),
              t2p1=root.querySelector('#t2-proc1'),
              t2io=root.querySelector('#t2-io'),
              t2p2=root.querySelector('#t2-proc2'),
              t2http=root.querySelector('#t2-http'),
              t3p=root.querySelector('#t3-proc'),
              t3http=root.querySelector('#t3-http');

        // sequential CPU (no overlap)
        seg(t1p1, 0, 150);
        seg(t2p1, 150, 100);
        seg(t3p, 250, 120);
        seg(t2p2, 370, 130);
        seg(t1p2, 500, 100);

        // async waits
        seg(t1io, 150, 350);
        seg(t2io, 250, 120);
        seg(t2http, 500, 300);
        seg(t3http, 370, 300);

        timer=setTimeout(()=>{running=false;start();},(TL*SCALE)+400);
      }

      window.addEventListener('load',()=>setTimeout(start,300));
      window.addEventListener('beforeunload',()=>{if(timer)clearTimeout(timer);});
    })();
  </script>
</div>


```