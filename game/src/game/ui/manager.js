export class UiManager {
    constructor(uiLayer) {
        this.uiLayer = uiLayer;
    }

    resize(windowWidth, windowHeight, canvas) {
        const rect = canvas.getBoundingClientRect();
        
        const scaleX = rect.width / windowWidth;
        const scaleY = rect.height / windowHeight;

        this.uiLayer.style.transform = `scale(${scaleX}, ${scaleY})`;
        this.uiLayer.style.transformOrigin = 'top left';
    }

    addElement(element) {
        this.uiLayer.appendChild(element.element);
    }
}