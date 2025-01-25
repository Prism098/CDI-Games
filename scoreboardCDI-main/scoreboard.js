async function fetchTopScores() {
  try {
      const response = await fetch('http://localhost:4000/top-scores');
      const scores = await response.json();

      const scoreList = document.getElementById('scoreList');
      scoreList.innerHTML = ''; // Maak de lijst leeg voordat nieuwe data wordt toegevoegd

      scores.forEach((item, index) => {
          const li = document.createElement('li');
          li.textContent = `${index + 1}. ${item.name || 'Onbekend'} - ${item.totalScore || 0}`;
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
    constructor(type, color1, color2) {
      this.type = type; // "circle", "half-circle", "right-triangle", "triangle"
      this.color1 = color1; // Hex code for the starting gradient color
      this.color2 = color2; // Hex code for the ending gradient color
      this.size = Math.random() * 200 + 75; // Larger size (75 to 275)
      this.respawnOffScreen(); // Initialize position off-screen
    }
  
    // Respawn shape completely off-screen
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
  
    // Create a linear gradient for the shape
    createGradient(ctx) {
      // Define gradient start and end points
      const gradient = ctx.createLinearGradient(
        this.x - this.size, // Start gradient on the left side of the shape
        this.y - this.size,
        this.x + this.size, // End gradient on the right side of the shape
        this.y + this.size
      );
  
      // Add the specified colors
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
  
      ctx.fillStyle = this.createGradient(ctx); // Apply the gradient
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





