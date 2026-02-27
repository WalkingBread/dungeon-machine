export class KeyboardHandler {
    constructor() {
        this.keys = new Set()
    }

    onKeyPress(e) {
        this.keys.add(e.code)
    }

    onKeyRelease(e) {
        this.keys.delete(e.code)
    }
}

export class MouseHandler {
    constructor() {
        this.mouseX = 0;
        this.mouseY = 0;
        this.pressedButtons = new Set()
    }

    onButtonPress(e) {
        this.pressedButtons.add(e.button);
    }

    onButtonRelease(e) {
        this.pressedButtons.delete(e.button);
    }

    onMouseMove(e) {
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
    }

}