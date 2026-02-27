const DIV_TAG = 'div';
const INPUT_TAG = 'input';

export class UiElement {
    constructor(x, y, width, height, tag = DIV_TAG) {
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
    constructor(x, y, width, height) {
        super(x, y, width, height, INPUT_TAG);
        this.element.type = 'text';
    }
}