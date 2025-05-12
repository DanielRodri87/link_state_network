const canvas = document.getElementById('petriCanvas');
const ctx = canvas.getContext('2d');

class PetriNet {
    constructor() {
        this.places = [
            { x: 100, y: 100, label: "Host 1" },
            { x: 300, y: 100, label: "Router 1" },
            { x: 500, y: 100, label: "Host 2" },
            { x: 200, y: 300, label: "Router 2" },
            { x: 400, y: 300, label: "Router 3" },
        ];
        
        this.transitions = [
            { x: 200, y: 100 },
            { x: 400, y: 100 },
            { x: 300, y: 200 },
            { x: 300, y: 300 },
        ];

        this.tokens = [
            { placeIndex: 0, count: 1 },
            { placeIndex: 2, count: 1 },
        ];
    }

    draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw arcs
        this.drawArcs();
        
        // Draw places
        this.places.forEach((place, index) => {
            ctx.beginPath();
            ctx.arc(place.x, place.y, 30, 0, 2 * Math.PI);
            ctx.stroke();
            
            // Draw labels
            ctx.font = '12px Arial';
            ctx.fillText(place.label, place.x - 25, place.y + 50);
            
            // Draw tokens
            const token = this.tokens.find(t => t.placeIndex === index);
            if (token) {
                ctx.beginPath();
                ctx.arc(place.x, place.y, 10, 0, 2 * Math.PI);
                ctx.fill();
            }
        });
        
        // Draw transitions
        this.transitions.forEach(transition => {
            ctx.fillRect(transition.x - 15, transition.y - 5, 30, 10);
        });
    }

    drawArcs() {
        // Define connections
        const arcs = [
            [0, 0], [0, 2], [1, 1], [1, 3],
            [2, 1], [2, 2], [3, 2], [3, 3]
        ];

        arcs.forEach(([placeIndex, transitionIndex]) => {
            const place = this.places[placeIndex];
            const transition = this.transitions[transitionIndex];
            
            ctx.beginPath();
            ctx.moveTo(place.x, place.y);
            ctx.lineTo(transition.x, transition.y);
            ctx.stroke();
        });
    }
}

const petriNet = new PetriNet();
petriNet.draw();

// Download functionality
document.getElementById('downloadBtn').addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'rede_petri.png';
    link.href = canvas.toDataURL();
    link.click();
});
