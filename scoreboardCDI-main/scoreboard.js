/**************************************************************
  scoreboard.js
**************************************************************/

/** ============ GLOBALS & CONSTANTS ============ **/
// TOP scores from server
let currentScores = [];
// RECENT scores from server
let currentRecent = [];

const MAX_PLAYERS = 10;
const SLOT_HEIGHT_TOP = 70;
const SLOT_HEIGHT_RECENT = 70;

// DOM elements for the two <ol> boards
const scoreList = document.getElementById('scoreList');     // Top scoreboard
const recentList = document.getElementById('recentList');   // Recent scoreboard

// =============== ON LOAD ===============
window.onload = function() {
  // 1) Fetch top & recent scores immediately
  fetchTopScores();
  fetchRecentScores();

  // 2) Re-poll both boards every 3 seconds
  setInterval(fetchTopScores, 3000);
  setInterval(fetchRecentScores, 3000);
};

/**************************************************************
  TOP SCORES
**************************************************************/
async function fetchTopScores() {
  try {
    const res = await fetch('http://localhost:4000/top-scores?_=' + Date.now());
    const newScores = await res.json();
    const trimmed = newScores.slice(0, MAX_PLAYERS);

    // If first load
    if (currentScores.length === 0) {
      currentScores = trimmed;
      initialRenderTop(currentScores);
      return;
    }

    // If scoreboard changed, process updates
    if (JSON.stringify(currentScores) !== JSON.stringify(trimmed)) {
      processTopScoreUpdate(currentScores, trimmed);
      currentScores = trimmed;
    }
  } catch (err) {
    console.error("Error fetching top scores:", err);
  }
}

function processTopScoreUpdate(oldScores, newScores) {
  const changes = getListChanges(oldScores, newScores);

  // If there's a newly added top-10 user:
  if (changes.added) {
    // Then animate for top scoreboard
    if (changes.removed) {
      animateSingleUpdate(changes.added, changes.removed, newScores);
    } else {
      animateSimpleAddition(changes.added, newScores);
    }
  }
}

/** Initial one-time render of the top scoreboard */
function initialRenderTop(scores) {
  scoreList.innerHTML = '';

  scores.forEach((p, i) => {
    const li = document.createElement('li');
    li.dataset.name = p.name;
    li.style.top = (i * SLOT_HEIGHT_TOP) + 'px';
    li.style.opacity = '0';

    const wrapper = document.createElement('div');
    wrapper.className = 'score-item';
    wrapper.innerHTML = `
      <span class="score-name">${p.name}</span>
      <span class="score-value">${p.totalScore}</span>
    `;
    li.appendChild(wrapper);

    scoreList.appendChild(li);

    // Fade in each item
    gsap.to(li, {
      opacity: 1,
      delay: i * 0.3,
      duration: 0.5
    });
  });
}

/** Animate a simple new addition (no one removed) */
function animateSimpleAddition(added, newScores) {
  startConfettiForNewEntry();

  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);

  // Create new <li>
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

  // Fade in from above
  timeline.fromTo(newEl,
    { opacity: 0, y: -20 },
    { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }
  );

  // Shift items below
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

/** Animate single update (added & removed) */
function animateSingleUpdate(added, removed, newScores) {
  startConfettiForNewEntry();

  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);
  const removedIndex = MAX_PLAYERS - 1;

  // 1) Fade out old #10
  timeline.to(scoreList.children[removedIndex], {
    opacity: 0,
    y: 20,
    duration: 0.6,
    ease: "power2.in",
    onComplete() {
      this.targets()[0].remove();
    }
  });

  // 2) Shift items from newIndex downward
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

  // Highlight & fade in
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


/**************************************************************
  RECENT SCORES (FROM SERVER)
**************************************************************/
async function fetchRecentScores() {
  try {
    const res = await fetch('http://localhost:4000/recent-scores?_=' + Date.now());
    const newScores = await res.json();
    const trimmed = newScores.slice(0, MAX_PLAYERS);

    // First load
    if (currentRecent.length === 0) {
      currentRecent = trimmed;
      initialRenderRecent(currentRecent);
      return;
    }

    // If scoreboard changed, process updates
    if (JSON.stringify(currentRecent) !== JSON.stringify(trimmed)) {
      processRecentScoreUpdate(currentRecent, trimmed);
      currentRecent = trimmed;
    }
  } catch (err) {
    console.error("Error fetching recent scores:", err);
  }
}

/** Compare old vs new for the "recent" scoreboard & animate if new user is added. */
function processRecentScoreUpdate(oldScores, newScores) {
  const changes = getListChanges(oldScores, newScores);

  if (changes.added) {
    if (changes.removed) {
      animateSingleUpdateRecent(changes.added, changes.removed, newScores);
    } else {
      animateSimpleAdditionRecent(changes.added, newScores);
    }
  }
}

/** Initial one-time render of the recent scoreboard */
function initialRenderRecent(scores) {
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

/** Animate a simple new addition in the "recent" scoreboard */
function animateSimpleAdditionRecent(added, newScores) {
  // If you want confetti here, do it:
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

  newEl.style.top = (newIndex * SLOT_HEIGHT_RECENT) + 'px';
  newEl.style.opacity = '0';
  recentList.insertBefore(newEl, recentList.children[newIndex]);

  // fade in from above
  timeline.fromTo(newEl,
    { opacity: 0, y: -20 },
    { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }
  );

  // shift items below
  for (let i = newIndex + 1; i < newScores.length; i++) {
    const el = recentList.children[i];
    if (el) {
      timeline.to(el, {
        top: i * SLOT_HEIGHT_RECENT,
        duration: 0.6,
        ease: "power2.out"
      }, "<0.2");
    }
  }
}

/** Animate a single update in "recent" scoreboard (new & removed doc) */
function animateSingleUpdateRecent(added, removed, newScores) {
  // If you want confetti
  startConfettiForNewEntry();

  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);
  const removedIndex = MAX_PLAYERS - 1;

  // 1) fade out old #10
  timeline.to(recentList.children[removedIndex], {
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
    timeline.to(recentList.children[i], {
      top: (i + 1) * SLOT_HEIGHT_RECENT,
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

  newEl.style.top = (newIndex * SLOT_HEIGHT_RECENT) + 'px';
  newEl.style.opacity = '0';
  recentList.insertBefore(newEl, recentList.children[newIndex]);

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

/**************************************************************
  UTILS & CONFETTI
**************************************************************/
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
