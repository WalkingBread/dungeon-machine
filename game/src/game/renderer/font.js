const DEFAULT_FONT_SIZE = 30;
const DEFAULT_FONT_COLOR = '#fff';
const DEFAULT_FONT = 'Arial';

export class Font {
    constructor({font = DEFAULT_FONT, size = DEFAULT_FONT_SIZE, color = DEFAULT_FONT_COLOR}) {
        this.font = font;
        this.size = size;
        this.color = color;
    }
}