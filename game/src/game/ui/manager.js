export class UiManager {
    constructor(uiLayer) {
        this.uiLayer = uiLayer;
        this.elements = [];
    }

    addElement(element) {
        this.elements.push(element);
        this.uiLayer.appendChild(element.element);
    }

    addElements(elements) {
        this.elements.push(elements);
        elements.forEach(element => {
            this.uiLayer.appendChild(element.element);
        });
    }

    getWidth() {
        return parseInt(this.uiLayer.style.width);
    }

    getHeight() {
        return parseInt(this.uiLayer.style.height);
    }
}