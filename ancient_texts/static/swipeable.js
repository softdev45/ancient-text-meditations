import TinyGesture from './TinyGesture.js';
import { addTransition, removeTransition } from './DemoTransitions.js';
// import { addTransition, removeTransition } from "{{ url_for('static', filename='DemoTransitions.js') }}";

export default function Swipeable(node) {
  const options = {
    // Set a higher threshold for horizontal movement (e.g., 50px)
    // and a lower one for vertical movement (e.g., 10px).
    threshold: (type, self) => {
      if (type === 'x') {
        // return Math.max(50, Math.floor(0.15 * (window.innerWidth || document.body.clientWidth)));
        return 10;
      } else {
        // return Math.max(10, Math.floor(0.15 * (window.innerHeight || document.body.clientHeight)));
        return 10;
      }
    },
    velocityThreshold: 5,
    diagonalSwipes: false,
    // Other options...
  };
  const gesture = new TinyGesture(node, options);
  let goRaf;
  let backTimeout;
  const preventDefault = (event) => {
    event.preventDefault();
  };

  addTransition(node, 'transform 0.5s ease');

  // Don't allow the page to scroll when the target is first pressed.
  // node.addEventListener('touchstart', preventDefault, { passive: false });

  let xpos = 0;
  let ypos = 0;
  let myTransform = ` translateX(${xpos}px) translateY(${ypos}px)`;
  node.style.transform = '';

  function resetTransform() {
    node.style.transform = `${node.style.transform}`.replace(/\s*translateX\([^)]*\)/, '');
    node.style.transform = `${node.style.transform}`.replace(/\s*translateY\([^)]*\)/, '');
    myTransform = ` translateX(${xpos}px) translateY(${ypos}px)`;
  }

  function doTransform() {
    node.style.transform = `${node.style.transform}` + myTransform;
    clearTimeout(backTimeout);
    backTimeout = setTimeout(() => {
      xpos = 0;
      ypos = 0;
      resetTransform();
    }, 100);
  }

  // When the target is swiped, fling it really far in that direction before coming back to origin.
  gesture.on('swiperight', () => {
    console.log(gesture)
    if (gesture.scale > 1.1 || gesture.scale < 0.9) {
      return;
    }
    xpos = 1000;
    resetTransform();
    cancelAnimationFrame(goRaf);
    goRaf = requestAnimationFrame(doTransform);
    stepVerse(1)
  });
  gesture.on('swipeleft', () => {
    console.log(gesture)
    if (gesture.scale > 1.1 || gesture.scale < 0.9) {
      return;
    }
    xpos = -1000;
    resetTransform();
    cancelAnimationFrame(goRaf);
    goRaf = requestAnimationFrame(doTransform);
    stepVerse(-1)
  });
  gesture.on('swipeup', () => {
    if (gesture.scale > 1.1 || gesture.scale < 0.9) {
      return;
    }
    ypos = -300;
    resetTransform();
    cancelAnimationFrame(goRaf);
    goRaf = requestAnimationFrame(doTransform);
    changeView(1)
  });
  gesture.on('swipedown', () => {
    if (gesture.scale > 1.1 || gesture.scale < 0.9) {
      return;
    }
    ypos = 300;
    resetTransform();
    cancelAnimationFrame(goRaf);
    goRaf = requestAnimationFrame(doTransform);
    changeView(-1)
  });

  return {
    destroy() {
      node.removeEventListener('touchstart', preventDefault, {
        passive: false,
      });
      cancelAnimationFrame(goRaf);
      clearTimeout(backTimeout);
      node.style.transform = '';
      removeTransition(node, 'transform');
      gesture.destroy();
    },
  };
}