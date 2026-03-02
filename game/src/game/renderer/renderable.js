export class Renderable {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }

    render(renderer, x, y, centered = false) {
        if(centered) {
            x -= this.width / 2;
            y -= this.height / 2;
        }
        this.draw(renderer, x, y);
    }

    draw(renderer, x, y) {}
}

export class Sprite extends Renderable {
    constructor(image, width, height) {
        super(width, height);
        this.image = image;
    }

    draw(renderer, x, y) {
        renderer.renderImage(this.image, x, y, this.width, this.height);
    }
}