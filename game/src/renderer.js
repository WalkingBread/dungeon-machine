const BLACK = '#000'
const WHITE = '#fff'

export class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
    }

    resize(width, height) {
        const dpr = window.devicePixelRatio || 1;

        this.canvas.width = width * dpr;
        this.canvas.height = height * dpr;

        this.canvas.style.width = `${width}px`;
        this.canvas.style.height = `${height}px`;

        this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    clearScreen() {
        this.ctx.fillStyle = BLACK;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
}
