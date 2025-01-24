async function fetchTopScores() {
    try {
        const response = await fetch('http://localhost:4000/top-scores');
        const scores = await response.json();

        const scoreList = document.getElementById('scoreList');
        scoreList.innerHTML = ''; // Maak de lijst leeg voordat nieuwe data wordt toegevoegd

        scores.forEach((item, index) => {
            const li = document.createElement('li');
            li.textContent = `${index + 1}. ${item.name} - ${item.totalScore}`;
            scoreList.appendChild(li);
        });
    } catch (err) {
        console.error('Fout bij ophalen van scores:', err);
    }
}

// Start de confetti zodra de pagina geladen is en haal scores op------------------------------------------------------------------------------------------------------------------------------
window.onload = function() {
    fetchTopScores(); // Haal de scores op
    confetti.start(); // Start de confetti
};




// --------------creeeren van shapes--------------------------------------------------------------------------------------------------------------------------------------
const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size to match the screen
function setCanvasSize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

// Shape Class
class Shape {
  constructor(type) {
    this.type = type; // "circle", "half-circle", "right-triangle", "triangle"
    this.size = Math.random() * 200 + 75; // Larger size (50 to 150)
    this.respawnOffScreen(); // Initialize position off-screen
  }

  // Respawn shape completely off-screen
  respawnOffScreen() {
    const spawnSides = ["top", "bottom", "left", "right"];
    const side = spawnSides[Math.floor(Math.random() * spawnSides.length)];

    switch (side) {
      case "top": // Spawn above the canvas
        this.x = Math.random() * canvas.width;
        this.y = -this.size;
        break;
      case "bottom": // Spawn below the canvas
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + this.size;
        break;
      case "left": // Spawn to the left of the canvas
        this.x = -this.size;
        this.y = Math.random() * canvas.height;
        break;
      case "right": // Spawn to the right of the canvas
        this.x = canvas.width + this.size;
        this.y = Math.random() * canvas.height;
        break;
    }

    // Assign random speed and direction
    const angle = Math.random() * Math.PI * 2; // Random angle in radians
    const speed = Math.random() * 1 + 0.3; // Speed between 2 and 5
    this.speedX = Math.cos(angle) * speed;
    this.speedY = Math.sin(angle) * speed;
    this.color = 'rgba(255, 255, 255, 1)'; // White color
  }

  draw() {
    ctx.beginPath();
    switch (this.type) {
      case "circle":
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        break;
      case "half-circle":
        ctx.arc(this.x, this.y, this.size, 0, Math.PI); // Half-circle
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
    ctx.fillStyle = this.color;
    ctx.fill();
  }

  update() {
    // Move the shape
    this.x += this.speedX;
    this.y += this.speedY;

    // Check if the shape has completely moved off-screen
    if (
      this.x - this.size > canvas.width || // Right
      this.x + this.size < 0 || // Left
      this.y - this.size > canvas.height || // Bottom
      this.y + this.size < 0 // Top
    ) {
      this.respawnOffScreen(); // Respawn off-screen
    }

    this.draw();
  }
}

// Generate 2 shapes per type (circle, half-circle, right triangle, triangle)
const shapes = [];
const types = ["circle", "half-circle", "right-triangle", "triangle"];
types.forEach((type) => {
  for (let i = 0; i < 2; i++) { // Max 2 shapes of each type
    shapes.push(new Shape(type));
  }
});

// Animation Loop
function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
  shapes.forEach((shape) => shape.update()); // Update and draw each shape
  requestAnimationFrame(animate); // Loop
}

// Initialize canvas size and animation
setCanvasSize();
animate();

// Resize canvas on window resize
window.addEventListener('resize', () => {
  setCanvasSize();
});





