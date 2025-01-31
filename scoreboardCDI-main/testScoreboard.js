// Array om de gebruikte namen bij te houden
let usedNames = [];

// Functie om een willekeurige naam te genereren zonder duplicaten
function generateRandomName() {
  const names = ['Bas', 'Reinier', 'Abdul', 'Milan', 'Efdal', 'Max', 'Roel', 'Anne', 'Danny', 'Jasper'];
  
  // Krijg een willekeurige naam die nog niet is gebruikt
  let randomName;
  do {
    randomName = names[Math.floor(Math.random() * names.length)];
  } while (usedNames.includes(randomName)); // Herhaal totdat een unieke naam wordt gevonden

  // Voeg de naam toe aan de lijst van gebruikte namen
  usedNames.push(randomName);
  
  return randomName;
}

// Functie om een willekeurige score te genereren tussen 500 en 1000
function generateRandomScore() {
  return Math.floor(Math.random() * (1000 - 500 + 1)) + 500; 
}

// Functie om de scorelijst te genereren en te sorteren
function generateScoreboard() {
  const scoreList = document.getElementById('scoreList');
  const numScores = 10; // Aantal scores die we willen tonen

  // Maak een array om de scores en namen op te slaan
  let scores = [];

  for (let i = 0; i < numScores; i++) {
    const name = generateRandomName(); // Genereer unieke naam
    const score = generateRandomScore(); // Genereer score tussen 500 en 1000

    // Voeg naam en score toe aan de scores array
    scores.push({ name: name, score: score });
  }

  // Sorteer de array van scores van hoog naar laag
  scores.sort((a, b) => b.score - a.score);

  // Voeg de gesorteerde lijst toe aan de HTML
  scores.forEach((item, index) => {
    const li = document.createElement('li');
    li.textContent = `${index + 1}. ${item.name} - ${item.score}`; // Voeg nummer, naam en score toe
    scoreList.appendChild(li); // Voeg het item toe aan de lijst
  });
}

// Start de confetti zodra de pagina geladen is
window.onload = function() {
  generateScoreboard(); // Genereer het scorebord
  confetti.start(); // Start de confetti direct bij het laden van de pagina
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
    shapes.push(new Shape(type, "#FFFFFF", "#E4E4E4")); // Gradient from red to blue
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