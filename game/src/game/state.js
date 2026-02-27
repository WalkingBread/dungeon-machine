import { TextInput } from "./ui/element";

class State {
    constructor(uiManager) {
        this.uiManager = uiManager;
    }

    enter() {}
    render(renderer) {}
    update() {}
    exit() {}
}

export class MenuState extends State {
    constructor(uiManager) {
        super(uiManager);
    }

    enter() {
        this.uiManager.addElement(new TextInput(100, 100, 200, 50))
    }

    render(renderer) {

    }

    update() {

    }

    exit() {}
}