import { useEffect, useMemo, useRef, Children } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

import './Scroll.css';

gsap.registerPlugin(ScrollTrigger);

const ScrollFloat = ({
  children,
  scrollContainerRef,
  containerClassName = '',
  textClassName = '',
  animationDuration = 1,
  ease = 'back.inOut(2)',
  scrollStart = 'center bottom+=50%',
  scrollEnd = 'bottom bottom-=40%',
  stagger = 0.03
}) => {
  const containerRef = useRef(null);

  // Check if we're animating a string (like "React Bits") or React Components (like your feature cards)
  const isString = typeof children === 'string';

  const content = useMemo(() => {
    // Original React Bits logic for splitting text strings
    if (isString) {
      return children.split('').map((char, index) => (
        <span className="char" key={index}>
          {char === ' ' ? '\u00A0' : char}
        </span>
      ));
    }
    
    // NEW: Logic for component children (like cards) 
    // We wrap them in divs marked with the '.char' class so GSAP still targets them, 
    // but without disrupting height behaviors in CSS Grids.
    return Children.map(children, (child, index) => (
      <div className="char" key={index} style={{ display: 'flex', height: '100%' }}>
        {child}
      </div>
    ));
  }, [children, isString]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const scroller = scrollContainerRef && scrollContainerRef.current ? scrollContainerRef.current : window;

    // Grab exactly what GSAP expects based on the text or component wrappers above
    const charElements = el.querySelectorAll('.char');

    gsap.fromTo(
      charElements,
      {
        willChange: 'opacity, transform',
        opacity: 0,
        yPercent: 120,
        // Using extreme stretching for text is fine, but looks broken on complex UI cards,
        // so we disable the wild scale distortions for components while keeping the bounce float.
        scaleY: isString ? 2.3 : 1, 
        scaleX: isString ? 0.7 : 1, 
        transformOrigin: '50% 0%'
      },
      {
        duration: animationDuration,
        ease: ease,
        opacity: 1,
        yPercent: 0,
        scaleY: 1,
        scaleX: 1,
        stagger: stagger,
        scrollTrigger: {
          trigger: el,
          scroller,
          start: scrollStart,
          end: scrollEnd,
          scrub: true
        }
      }
    );
  }, [scrollContainerRef, animationDuration, ease, scrollStart, scrollEnd, stagger, isString]);

  // If it's a string, we preserve the semantic h2 exactly as React Bits intended.
  if (isString) {
    return (
      <h2 ref={containerRef} className={`scroll-float ${containerClassName}`}>
        <span className={`scroll-float-text ${textClassName}`}>{content}</span>
      </h2>
    );
  }

  // If we're rendering components (e.g., cards), we return a div. 
  // Returning an h2 wrapped around complex grid children causes HTML validation errors and layout breakage.
  return (
    <div ref={containerRef} className={`scroll-float-components ${containerClassName}`}>
      {content}
    </div>
  );
};

export default ScrollFloat;