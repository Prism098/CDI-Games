// scoreboard.js
let currentScores = [];
const MAX_PLAYERS = 10;
const SLOT_HEIGHT = 60;
const scoreList = document.getElementById('scoreList');

// Update the window.onload function
window.onload = function() {
  // Initial load
  fetchScores().then(() => {
    // After first fetch, render initial list
    if (currentScores.length > 0) {
      initialRender(currentScores);
    }
  });
  
  setInterval(fetchScores, 3000);
};

async function fetchScores() {
  try {
    const res = await fetch('http://localhost:4000/top-scores?_=' + Date.now()); // Cache busting
    const newScores = await res.json();
    const trimmedScores = newScores.slice(0, MAX_PLAYERS);
    
    // First load handling
    if (currentScores.length === 0) {
      initialRender(trimmedScores);
      currentScores = trimmedScores;
      return;
    }

    // Subsequent updates
    if(JSON.stringify(currentScores) !== JSON.stringify(trimmedScores)) {
      processScoreUpdate(currentScores, trimmedScores);
      currentScores = trimmedScores;
    }
  } catch (err) {
    console.error('Error fetching scores:', err);
  }
}

function processScoreUpdate(oldScores, newScores) {
  const changes = getListChanges(oldScores, newScores);
  
  // Handle both add-only and add+remove scenarios
  if (changes.added) {
    if (changes.removed) {
      animateSingleUpdate(changes.added, changes.removed, newScores);
    } else {
      animateSimpleAddition(changes.added, newScores);
    }
  }
}

function animateSimpleAddition(added, newScores) {
  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);
  
  // Create and animate new entry
  const newEl = document.createElement('li');
  newEl.dataset.name = added.name;
  newEl.textContent = `${newIndex + 1}. ${added.name} - ${added.totalScore}`;
  newEl.style.top = `${newIndex * SLOT_HEIGHT}px`;
  newEl.style.opacity = '0';
  scoreList.insertBefore(newEl, scoreList.children[newIndex]);

  timeline.fromTo(newEl, 
    { opacity: 0, y: -20 },
    { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }
  );

  // Update positions below new entry
  for (let i = newIndex + 1; i < newScores.length; i++) {
    const element = scoreList.children[i];
    if (element) {
      timeline.to(element, {
        top: i * SLOT_HEIGHT,
        duration: 0.6,
        ease: "power2.out"
      }, "<0.2");
    }
  }
}

function getListChanges(oldList, newList) {
  const oldSet = new Set(oldList.map(p => p.name));
  const newSet = new Set(newList.map(p => p.name));
  
  return {
    added: newList.find(p => !oldSet.has(p.name)),
    removed: oldList.find(p => !newSet.has(p.name))
  };
}

function animateSingleUpdate(added, removed, newScores) {
  const timeline = gsap.timeline();
  const newIndex = newScores.findIndex(p => p.name === added.name);
  const removedIndex = MAX_PLAYERS - 1; // Always last position

  // 1. Fade out removed element
  const removedEl = scoreList.children[removedIndex];
  timeline.to(removedEl, {
    opacity: 0,
    y: 20,
    duration: 0.6,
    ease: "power2.in",
    onComplete: () => removedEl.remove()
  });

  // 2. Animate positions moving down
  for (let i = newIndex; i < MAX_PLAYERS - 1; i++) {
    const element = scoreList.children[i];
    if (element) {
      timeline.to(element, {
        top: (i + 1) * SLOT_HEIGHT,
        duration: 3,
        ease: "power2.out"
      }, i === newIndex ? "+=0.1" : "<0.1");
    }
  }

  // 3. Create and animate new entry
  const newEl = document.createElement('li');
  newEl.dataset.name = added.name;
  newEl.textContent = `${newIndex + 1}. ${added.name} - ${added.totalScore}`;
  newEl.style.top = `${newIndex * SLOT_HEIGHT}px`;
  newEl.style.opacity = '0';
  scoreList.insertBefore(newEl, scoreList.children[newIndex]);

  timeline.to(newEl, {
    opacity: 1,
    y: 0,
    duration: 3,
    ease: "power2.out"
  }, "-=0.4");

  // Update displayed ranks
  newScores.forEach((player, index) => {
    const el = scoreList.querySelector(`[data-name="${player.name}"]`);
    if (el && el !== newEl) {
      el.textContent = `${index + 1}. ${player.name} - ${player.totalScore}`;
    }
  });
}

// Initial render
function initialRender(scores) {
  // Clear existing elements
  while (scoreList.firstChild) {
    scoreList.removeChild(scoreList.firstChild);
  }

  // Create and animate initial entries
  scores.forEach((p, i) => {
    const li = document.createElement('li');
    li.dataset.name = p.name;
    li.textContent = `${i + 1}. ${p.name} - ${p.totalScore}`;
    li.style.top = `${i * SLOT_HEIGHT}px`;
    li.style.opacity = '0';
    scoreList.appendChild(li);

    //snelheid van nieuwe plaatsingen en snelheid verschijnen van persoon
    gsap.to(li, {
      opacity: 1,
      delay: i * 0.5,
      duration: 0.5
    });
  });
}



// -------------------- Background Shapes --------------------
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
  for (let i=0;i<2;i++){
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
