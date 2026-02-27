import { Renderer } from "./game/renderer/renderer.js";
import { Game } from "./game/game.js";
import { KeyboardHandler, MouseHandler } from "./game/event/eventhandler.js";
import { UiManager } from "./game/ui/manager.js";

const CANVAS_ID  = 'dm-canvas';
const UI_LAYER_ID = 'ui-layer'

window.onload = () => {
    const canvas = document.getElementById(CANVAS_ID);
    const ui = document.getElementById(UI_LAYER_ID);
    new DungeonMachine(canvas, ui).run();
}

class DungeonMachine {
    constructor(canvas, ui) {
        this.renderer = new Renderer(canvas);
        this.uiManager = new UiManager(ui); 
        this.game = new Game(
            this.renderer,
            this.uiManager,
            this.#setupKeyboardHandler(),
            this.#setupMouseHandler()
        );

        window.addEventListener('contextmenu', (e) => e.preventDefault());
        window.addEventListener('resize', () => this.resizeWindow());
        this.resizeWindow();
    }

    #setupKeyboardHandler() {
        let handler = new KeyboardHandler();
        window.addEventListener('keydown', e => handler.onKeyPress(e));
        window.addEventListener('keyup', e => handler.onKeyRelease(e));
        return handler;
    }

    #setupMouseHandler() {
        let handler = new MouseHandler();
        window.addEventListener('mousemove', e => handler.onMouseMove(e));
        window.addEventListener('mousedown', e => handler.onButtonPress(e));
        window.addEventListener('mouseup', e => handler.onButtonRelease(e));
        return handler;
    }

    resizeWindow() {
        const w = window.innerWidth;
        const h = window.innerHeight;

        this.renderer.resize(w, h);
        this.uiManager.resize(w, h, this.renderer.canvas);
    }

    run() {
        this.game.run()
    }

}