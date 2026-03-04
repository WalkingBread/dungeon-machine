const DIV_TAG = 'div';
const INPUT_TAG = 'input';
const BUTTON_TAG = 'button';

const DEFAULT_FONT_SIZE = 30;

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
        element.style.fontSize = `${DEFAULT_FONT_SIZE}px`;
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
        this.element.addEventListener('input', () => { this.onType() });
    }

    getValue() {
        return this.element.value;
    }

    onType() {}
}

export class Button extends UiElement {
    constructor(text, x, y, width, height, centered = false) {
        super(x, y, width, height, centered, BUTTON_TAG);
        this.element.innerHTML = text;
        this.element.addEventListener('click', () => { this.onClick() });
    }

    enabled(enabled = true) {
        this.element.disabled = !enabled;
    }

    onClick() {}

}