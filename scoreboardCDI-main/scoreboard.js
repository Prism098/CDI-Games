/**************************************************************
  scoreboard.js
**************************************************************/

// =================== ARRAYS & CONSTANTS ===================
let currentScores = []; // For the Top Scores (from server)
let localRecent = [];   // For the Recent scoreboard (client-only)

const MAX_PLAYERS = 10;
const SLOT_HEIGHT_TOP = 70;
const SLOT_HEIGHT_RECENT = 70;

// DOM elements for the two lists
const scoreList = document.getElementById('scoreList');     // top scoreboard <ol>
const recentList = document.getElementById('recentList');   // local "recent" <ol>

// =================== ON LOAD ===================
window.onload = function() {
  // (Optional) load localRecent from localStorage
  const savedLocal = localStorage.getItem('localRecent');
  if (savedLocal) {
    localRecent = JSON.parse(savedLocal);
    initialRenderLocalRecent(localRecent);
  }

  // Fetch top scores, then render
  fetchTopScores().then(() => {
    if (currentScores.length > 0) {
      initialRenderTop(currentScores);
    }
  });

  // Poll top scores every 3s
  setInterval(fetchTopScores, 3000);

  // If you want background shapes or confetti always on load, do it here
};

// =================== FETCH & UPDATE: TOP SCORES ===================
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

    // Compare old vs. new
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
  if (changes.added) {
    // Also store the new entry in localRecent (to simulate "recent" scoreboard)
    addToLocalRecent(changes.added);

    // Then handle the top scoreboard animations
    if (changes.removed) {
      animateSingleUpdate(changes.added, changes.removed, newScores);
    } else {
      animateSimpleAddition(changes.added, newScores);
    }
  }
}

// =================== INITIAL RENDER: TOP SCORES ===================
function initialRenderTop(scores) {
  scoreList.innerHTML = '';

  scores.forEach((p, i) => {
    const li = document.createElement('li');
    li.dataset.name = p.name;
    li.style.top = (i * SLOT_HEIGHT_TOP) + 'px';
    li.style.opacity = '0';

    // Inner layout
    const wrapper = document.createElement('div');
    wrapper.className = 'score-item';
    wrapper.innerHTML = `
      <span class="score-name">${p.name}</span>
      <span class="score-value">${p.totalScore}</span>
    `;
    li.appendChild(wrapper);

    scoreList.appendChild(li);

    // Fade-in
    gsap.to(li, { opacity: 1, delay: i * 0.3, duration: 0.5 });
  });
}

// =================== ANIMATION: TOP SCORES ===================

// If a new user is added (no one removed)
function animateSimpleAddition(added, newScores) {
  startConfettiForNewEntry();

  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);

  // Create the new <li>
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

  // Shift items below it
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

  // highlight effect
  gsap.set(newEl, { backgroundColor: "rgba(255,255,255,0.8)" });

  timeline.fromTo(newEl,
    { opacity: 0, y: -30 },
    { opacity: 1, y: 0, duration: 0.8, ease: "back.out(1.5)", immediateRender: false },
    ">0.2"
  )
  .to(newEl, {
    backgroundColor: "rgba(0,0,0,0.8)",
    duration: 2,
    ease: "power4.out",
    delay: 0.5
  });
}

// =================== LOCAL "RECENT" SCOREBOARD ===================

// 1) Add a new entry to the local array
function addToLocalRecent(newEntry) {
  // We store oldLocal to diff with new
  const oldLocal = [...localRecent];

  // Insert at front
  localRecent.unshift(newEntry);

  // Keep only 10
  if (localRecent.length > 10) {
    localRecent.pop();
  }

  // Save to localStorage if you wish
  localStorage.setItem('localRecent', JSON.stringify(localRecent));

  // Animate changes
  processLocalRecentUpdate(oldLocal, localRecent);
}

// 2) On page load, we do an initialRenderLocalRecent (no animation)
function initialRenderLocalRecent(scores) {
  recentList.innerHTML = '';
  scores.forEach((p, i) => {
    const li = document.createElement('li');
    li.dataset.name = p.name;
    li.style.top = (i * SLOT_HEIGHT_RECENT) + 'px';

    const wrapper = document.createElement('div');
    wrapper.className = 'score-item';
    wrapper.innerHTML = `
      <span class="score-name">${p.name}</span>
      <span class="score-value">${p.totalScore}</span>
    `;
    li.appendChild(wrapper);

    recentList.appendChild(li);
  });
}

// 3) We do a diff of old vs new to see if there's an added or removed
function processLocalRecentUpdate(oldArr, newArr) {
  const changes = getListChanges(oldArr, newArr);

  if (changes.added) {
    if (changes.removed) {
      animateLocalSingleUpdate(changes.added, changes.removed, newArr);
    } else {
      animateLocalSimpleAddition(changes.added, newArr);
    }
  } else {
    // if no changes, do nothing
  }
}

// 4) "Simple addition" for the local scoreboard
function animateLocalSimpleAddition(added, newArr) {
  // We do the same approach as animateSimpleAddition, but for recentList
  const timeline = gsap.timeline();

  // newIndex = 0 because we always insert the new item at the top
  const newIndex = 0;

  // Shift existing items down by 1
  for (let i = 0; i < newArr.length - 1; i++) {
    const el = recentList.children[i];
    if (el) {
      timeline.to(el, {
        top: (i + 1) * SLOT_HEIGHT_RECENT,
        duration: 0.6,
        ease: "power2.out"
      }, i === 0 ? 0 : "<0.1");
    }
  }

  // Create new <li> at index 0
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
  recentList.insertBefore(newEl, recentList.firstChild);

  // Fade in from above
  timeline.fromTo(newEl,
    { opacity: 0, y: -20 },
    { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" },
    ">0.1"
  );

  // If list grew beyond 10, remove the last item
  if (newArr.length > MAX_PLAYERS) {
    const lastIndex = MAX_PLAYERS; // index 10 if length=11
    timeline.to(recentList.children[lastIndex], {
      opacity: 0,
      y: 20,
      duration: 0.6,
      ease: "power2.in",
      onComplete() {
        this.targets()[0].remove();
      }
    }, ">0.1");
  }
}

// 5) "Single update" for local scoreboard
function animateLocalSingleUpdate(added, removed, newArr) {
  // This is the scenario where we also remove an old item at the bottom
  const timeline = gsap.timeline();

  // remove the old item at the bottom (index=9?), if that's your logic
  const removedIndex = MAX_PLAYERS - 1;
  if (recentList.children[removedIndex]) {
    timeline.to(recentList.children[removedIndex], {
      opacity: 0,
      y: 20,
      duration: 0.6,
      ease: "power2.in",
      onComplete() {
        this.targets()[0].remove();
      }
    });
  }

  // Shift others down
  for (let i = 0; i < MAX_PLAYERS - 1; i++) {
    const el = recentList.children[i];
    if (el) {
      timeline.to(el, {
        top: (i + 1) * SLOT_HEIGHT_RECENT,
        duration: 0.8,
        ease: "power2.out"
      }, i === 0 ? ">0.2" : "<0.1");
    }
  }

  // Insert new item at index 0
  const newEl = document.createElement('li');
  newEl.dataset.name = added.name;

  const wrapper = document.createElement('div');
  wrapper.className = 'score-item';
  wrapper.innerHTML = `
    <span class="score-name">${added.name}</span>
    <span class="score-value">${added.totalScore}</span>
  `;
  newEl.appendChild(wrapper);

  newEl.style.top = "0px";
  newEl.style.opacity = '0';
  recentList.insertBefore(newEl, recentList.firstChild);

  timeline.fromTo(newEl, {
    opacity: 0,
    y: -30
  }, {
    opacity: 1,
    y: 0,
    duration: 0.8,
    ease: "back.out(1.5)",
    immediateRender: false
  }, ">0.2");
}

// =================== UTILS & CONFETTI ===================
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

// init shapes
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
