const DIV_TAG = 'div';
const INPUT_TAG = 'input';

export class UiElement {
    constructor(x, y, width, height, centered = false, tag = DIV_TAG) {
        if(centered) {
            x -= width / 2;
            y -= height / 2;
        }

        this.element = this.#setupElement(x, y, width, height, tag);
    }

    #setupElement(x, y, width, height, tag) {
        let element = document.createElement(tag);
        element.style.position = 'absolute';
        element.style.left = `${x}px`;
        element.style.top = `${y}px`;
        element.style.width = `${width}px`;
        element.style.height = `${height}px`;
        element.style.pointerEvents = 'auto';
        return element;
    }

    addStyle(styleClass) {
        this.element.className = styleClass;
    }
}

export class TextInput extends UiElement {
    constructor(x, y, width, height, centered = false) {
        super(x, y, width, height, centered, INPUT_TAG);
        this.element.type = 'text';
    }
}