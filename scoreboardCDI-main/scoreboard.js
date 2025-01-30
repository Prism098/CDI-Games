/**************************************************************
  scoreboard.js
**************************************************************/

/** ============ GLOBALS & CONSTANTS ============ **/
let currentScores = [];    // For the Top Scores (from server)
let localRecent = [];      // For the Recent scoreboard (client-only)

const MAX_PLAYERS = 10;
const SLOT_HEIGHT_TOP = 70;
const SLOT_HEIGHT_RECENT = 70;

// DOM elements for the two <ol> boards
const scoreList = document.getElementById('scoreList');     // top scoreboard
const recentList = document.getElementById('recentList');   // local "recent"

// =============== ON LOAD ===============
window.onload = function() {
  // (Optional) load localRecent from localStorage
  const savedLocal = localStorage.getItem('localRecent');
  if (savedLocal) {
    localRecent = JSON.parse(savedLocal);
    initialRenderLocalRecent(localRecent); // fade in each item
  }

  // Fetch top scores & do an initial render
  fetchTopScores().then(() => {
    if (currentScores.length > 0) {
      initialRenderTop(currentScores);
    }
  });

  // Re-poll top scores every 3 seconds
  setInterval(fetchTopScores, 3000);
};

// ============ FETCH & UPDATE: TOP SCORES ============
async function fetchTopScores() {
  try {
    const res = await fetch('http://localhost:4000/top-scores?_=' + Date.now());
    const newScores = await res.json();
    const trimmedScores = newScores.slice(0, MAX_PLAYERS);

    // First load
    if (currentScores.length === 0) {
      currentScores = trimmedScores;
      initialRenderTop(currentScores);
      return;
    }

    // If scoreboard changed, process updates
    if (JSON.stringify(currentScores) !== JSON.stringify(trimmedScores)) {
      processTopScoreUpdate(currentScores, trimmedScores);
      currentScores = trimmedScores;
    }
  } catch (err) {
    console.error("Error fetching top scores:", err);
  }
}

function processTopScoreUpdate(oldScores, newScores) {
  const changes = getListChanges(oldScores, newScores);

  // If there's a newly added top-10 user:
  if (changes.added) {
    // Also store that new entry in localRecent
    addToLocalRecent(changes.added);

    // Then animate for top scoreboard
    if (changes.removed) {
      animateSingleUpdate(changes.added, changes.removed, newScores);
    } else {
      animateSimpleAddition(changes.added, newScores);
    }
  }
}

// ============ INITIAL RENDER: TOP SCORES ============
function initialRenderTop(scores) {
  scoreList.innerHTML = '';

  scores.forEach((p, i) => {
    const li = document.createElement('li');
    li.dataset.name = p.name;

    // position & initial opacity
    li.style.top = (i * SLOT_HEIGHT_TOP) + 'px';
    li.style.opacity = '0';

    // create inner structure
    const wrapper = document.createElement('div');
    wrapper.className = 'score-item';
    wrapper.innerHTML = `
      <span class="score-name">${p.name}</span>
      <span class="score-value">${p.totalScore}</span>
    `;
    li.appendChild(wrapper);
    scoreList.appendChild(li);

    // fade in each item
    gsap.to(li, {
      opacity: 1,
      delay: i * 0.3,
      duration: 0.5
    });
  });
}

// ======= ANIMATIONS: TOP SCORES =======

// If a new user is added (no one removed)
function animateSimpleAddition(added, newScores) {
  startConfettiForNewEntry();

  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);

  // create new <li>
  const newEl = document.createElement('li');
  newEl.dataset.name = added.name;

  const wrapper = document.createElement('div');
  wrapper.className = 'score-item';
  wrapper.innerHTML = `
    <span class="score-name">${added.name}</span>
    <span class="score-value">${added.totalScore}</span>
  `;
  newEl.appendChild(wrapper);

  newEl.style.top = (newIndex * SLOT_HEIGHT_TOP) + 'px';
  newEl.style.opacity = '0';
  scoreList.insertBefore(newEl, scoreList.children[newIndex]);

  // fade in from above
  timeline.fromTo(newEl,
    { opacity: 0, y: -20 },
    { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }
  );

  // shift items below
  for (let i = newIndex + 1; i < newScores.length; i++) {
    const el = scoreList.children[i];
    if (el) {
      timeline.to(el, {
        top: i * SLOT_HEIGHT_TOP,
        duration: 0.6,
        ease: "power2.out"
      }, "<0.2");
    }
  }
}

// If a new user is added AND one user is removed
function animateSingleUpdate(added, removed, newScores) {
  startConfettiForNewEntry();

  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);
  const removedIndex = MAX_PLAYERS - 1;

  // 1) fade out old #10
  timeline.to(scoreList.children[removedIndex], {
    opacity: 0,
    y: 20,
    duration: 0.6,
    ease: "power2.in",
    onComplete() {
      this.targets()[0].remove();
    }
  });

  // 2) shift items from newIndex downward
  for (let i = newIndex; i < MAX_PLAYERS - 1; i++) {
    timeline.to(scoreList.children[i], {
      top: (i + 1) * SLOT_HEIGHT_TOP,
      duration: 0.8,
      ease: "power2.out"
    }, i === newIndex ? ">0.2" : "<0.1");
  }

  // 3) Insert new item
  const newEl = document.createElement('li');
  newEl.dataset.name = added.name;

  const wrapper = document.createElement('div');
  wrapper.className = 'score-item';
  wrapper.innerHTML = `
    <span class="score-name">${added.name}</span>
    <span class="score-value">${added.totalScore}</span>
  `;
  newEl.appendChild(wrapper);

  newEl.style.top = (newIndex * SLOT_HEIGHT_TOP) + 'px';
  newEl.style.opacity = '0';
  scoreList.insertBefore(newEl, scoreList.children[newIndex]);

  // highlight & fade in
  gsap.set(newEl, { backgroundColor: "rgba(255,255,255,0.8)" });

  timeline.fromTo(newEl,
    { opacity: 0, y: -30 },
    { opacity: 1, y: 0, duration: 0.8, ease: "back.out(1.5)", immediateRender: false },
    ">0.2"
  ).to(newEl, {
    backgroundColor: "rgba(0,0,0,0.8)",
    duration: 2,
    ease: "power4.out",
    delay: 0.5
  });
}


// ======= RECENT SCORES (client-only) =======

function addToLocalRecent(newEntry) {
  // Insert at front of array
  localRecent.unshift(newEntry);

  // If we exceed 10, remove last from array
  if (localRecent.length > MAX_PLAYERS) {
    localRecent.pop();
  }

  // Save to localStorage
  localStorage.setItem('localRecent', JSON.stringify(localRecent));

  // Animate the insertion in the DOM
  animateLocalAddOrUpdate();
}

// 1) On page load, render each item with a fade in
function initialRenderLocalRecent(scores) {
  recentList.innerHTML = '';

  scores.forEach((p, i) => {
    const li = document.createElement('li');
    li.dataset.name = p.name;

    li.style.top = (i * SLOT_HEIGHT_RECENT) + 'px';
    li.style.opacity = '0';

    const wrapper = document.createElement('div');
    wrapper.className = 'score-item';
    wrapper.innerHTML = `
      <span class="score-name">${p.name}</span>
      <span class="score-value">${p.totalScore}</span>
    `;
    li.appendChild(wrapper);

    recentList.appendChild(li);

    // fade in each item
    gsap.to(li, {
      opacity: 1,
      delay: i * 0.3,
      duration: 0.5
    });
  });
}

// 2) Each time we add a new item, do the step-by-step "fade out → shift → fade in new"
function animateLocalAddOrUpdate() {
  const timeline = gsap.timeline();

  // 1) If we already have 10 <li> in the DOM, fade out the last one
  if (recentList.children.length === MAX_PLAYERS + 1) {
    // We grew to 11; remove the old #10
    const removed = recentList.children[MAX_PLAYERS];
    timeline.to(removed, {
      opacity: 0,
      y: 20,
      duration: 0.6,
      ease: "power2.in",
      onComplete() {
        this.targets()[0].remove();
      }
    });
  } else if (recentList.children.length === MAX_PLAYERS) {
    // If we are exactly 10 but we inserted a new item in the array, 
    // we want to fade out the old last item. 
    // Actually, we handle that AFTER we insert the new item at top. 
    // So let's handle the "move down" logic first in that scenario. 
  }

  // 2) Shift every <li> from index 0..(length-1) down 1 slot
  for (let i = 0; i < recentList.children.length; i++) {
    const el = recentList.children[i];
    timeline.to(el, {
      top: (i + 1) * SLOT_HEIGHT_RECENT,
      duration: 0.8,
      ease: "power2.out"
    }, i === 0 ? ">0.2" : "<0.1");
  }

  // 3) Insert new item at index=0 & fade in
  // The new item is localRecent[0]
  const newEntry = localRecent[0];
  const newEl = document.createElement('li');
  newEl.dataset.name = newEntry.name;

  const wrapper = document.createElement('div');
  wrapper.className = 'score-item';
  wrapper.innerHTML = `
    <span class="score-name">${newEntry.name}</span>
    <span class="score-value">${newEntry.totalScore}</span>
  `;
  newEl.appendChild(wrapper);

  // put it in the DOM at the top
  newEl.style.top = "0px";
  newEl.style.opacity = '0';
  // highlight effect if you like:
  gsap.set(newEl, { backgroundColor: "rgba(255,255,255,0.8)" });

  recentList.insertBefore(newEl, recentList.firstChild);

  // 4) fade in the new top item
  timeline.fromTo(newEl, {
    opacity: 0,
    y: -30
  }, {
    opacity: 1,
    y: 0,
    duration: 0.8,
    ease: "back.out(1.5)",
    immediateRender: false
  }, ">0.2")
  .to(newEl, {
    backgroundColor: "rgba(0,0,0,0.8)",
    duration: 2,
    ease: "power4.out",
    delay: 0.5
  });
}


// =============== UTILS & CONFETTI ===============
function getListChanges(oldList, newList) {
  const oldSet = new Set(oldList.map(p => p.name));
  const newSet = new Set(newList.map(p => p.name));
  
  return {
    added: newList.find(p => !oldSet.has(p.name)),
    removed: oldList.find(p => !newSet.has(p.name))
  };
}

function startConfettiForNewEntry() {
  confetti.start();
  setTimeout(() => confetti.stop(), 5000);
}

/**************************************************************
    BACKGROUND SHAPES - UNCHANGED
**************************************************************/
const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');

function setCanvasSize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
class Shape {
  constructor(type, color1, color2) {
    this.type = type;
    this.color1 = color1;
    this.color2 = color2;
    this.size = Math.random() * 200 + 75;
    this.respawnOffScreen();
  }
  respawnOffScreen() {
    const spawnSides = ["top", "bottom", "left", "right"];
    const side = spawnSides[Math.floor(Math.random() * spawnSides.length)];
    switch (side) {
      case "top":
        this.x = Math.random() * canvas.width;
        this.y = -this.size;
        break;
      case "bottom":
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + this.size;
        break;
      case "left":
        this.x = -this.size;
        this.y = Math.random() * canvas.height;
        break;
      case "right":
        this.x = canvas.width + this.size;
        this.y = Math.random() * canvas.height;
        break;
    }
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 1 + 0.3;
    this.speedX = Math.cos(angle) * speed;
    this.speedY = Math.sin(angle) * speed;
  }
  createGradient(ctx) {
    const gradient = ctx.createLinearGradient(
      this.x - this.size,
      this.y - this.size,
      this.x + this.size,
      this.y + this.size
    );
    gradient.addColorStop(0, this.color1);
    gradient.addColorStop(1, this.color2);
    return gradient;
  }
  draw() {
    ctx.beginPath();
    switch (this.type) {
      case "circle":
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        break;
      case "half-circle":
        ctx.arc(this.x, this.y, this.size, 0, Math.PI);
        break;
      case "right-triangle":
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x + this.size, this.y);
        ctx.lineTo(this.x, this.y - this.size);
        ctx.closePath();
        break;
      case "triangle":
        ctx.moveTo(this.x, this.y - this.size);
        ctx.lineTo(this.x - this.size, this.y + this.size);
        ctx.lineTo(this.x + this.size, this.y + this.size);
        ctx.closePath();
        break;
    }
    ctx.fillStyle = this.createGradient(ctx);
    ctx.fill();
  }
  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (
      this.x - this.size > canvas.width ||
      this.x + this.size < 0 ||
      this.y - this.size > canvas.height ||
      this.y + this.size < 0
    ) {
      this.respawnOffScreen();
    }
    this.draw();
  }
}
setCanvasSize();
const shapes = [];
["circle","half-circle","right-triangle","triangle"].forEach(type => {
  for (let i=0; i<2; i++){
    shapes.push(new Shape(type,"#FFFFFF","#E4E4E4"));
  }
});
function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  shapes.forEach(shape => shape.update());
  requestAnimationFrame(animate);
}
animate();
window.addEventListener('resize', setCanvasSize);
