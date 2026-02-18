BLACK = '#000'
WHITE = '#fff'

class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
    }

    clearScreen() {
        this.ctx.fillStyle = BLACK;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
}