import { Sprite } from "./renderer/renderable";
import { TextInput } from "./ui/element";

class State {
    constructor(renderer, uiManager) {
        this.renderer = renderer;
        this.uiManager = uiManager;
    }

    enter() {}
    render() {}
    update() {}
    exit() {}
}

const LOGO_SRC = 'https://www.pngmart.com/files/23/Dungeons-And-Dragons-Logo-PNG-File.png';

export class MenuState extends State {
    constructor(renderer, uiManager) {
        super(renderer, uiManager);
    }

    enter() {
        this.uiManager.addElement(
            new TextInput(
                this.uiManager.getWidth() / 2,
                700, 
                600, 200, true
            )
        );
        const logoImg = new Image();
        logoImg.src = LOGO_SRC;
        
        this.logo = new Sprite(logoImg, 600, 200);
    }

    render() {
        this.logo.render(
            this.renderer, 
            this.renderer.getWindowWidth() / 2, 
            300, 
            true
        );
        this.renderer.renderText(
            'Theme of campaign:', 
            this.renderer.getWindowWidth() / 2, 
            540, 50, 
            'Arial', '#fff', 
            true
        );
    }

    update() {}

    exit() {}
}