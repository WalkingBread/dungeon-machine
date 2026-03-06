const BLACK = '#000'
const WHITE = '#fff'

const DEFAULT_FONT = 'Arial';

export class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
    }

    clearScreen() {
        this.ctx.fillStyle = BLACK;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    renderText(text, x, y, size, font = DEFAULT_FONT, color = BLACK, centered = false) {
        this.ctx.font = `${size}px ${font}`;
        this.ctx.fillStyle = color;
        this.ctx.textAlign = 'left';
        if(centered) {
            this.ctx.textAlign = 'center';
        } 
        this.ctx.fillText(text, x, y);
    }

    renderImage(image, x, y, width = null, height = null) {
        if (width && height) {
            this.ctx.drawImage(image, x, y, width, height);
        } else {
            this.ctx.drawImage(image, x, y);
        }
    }

    getCenterX() {
        return this.getWindowWidth() / 2;
    }

    getCenterY() {
        return this.getWindowHeight() / 2;
    }

    getWindowWidth() {
        return this.canvas.width;
    }

    getWindowHeight() {
        return this.canvas.height;
    }
}
