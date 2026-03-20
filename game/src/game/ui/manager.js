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

    removeElement(element) {
        this.elements.splice(this.elements.indexOf(element), 1);
        element.element.remove();
    }

    getWidth() {
        return parseInt(this.uiLayer.style.width);
    }

    getHeight() {
        return parseInt(this.uiLayer.style.height);
    }

    getCenterX() {
        return this.getWidth() / 2;
    }

    getCenterY() {
        return this.getHeight() / 2;
    }

    clear() {
        this.uiLayer.innerHTML = '';
        this.elements = [];
    }
}