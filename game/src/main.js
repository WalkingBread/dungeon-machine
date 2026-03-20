import { Game } from "./game/game.js";
import { KeyboardHandler, MouseHandler } from "./game/event/eventhandler.js";

const CANVAS_ID  = 'dm-canvas';
const UI_LAYER_ID = 'ui-layer';
const GAME_CONTAINER_ID = 'dm-container';

window.onload = () => {
    const gameContainer = document.getElementById(GAME_CONTAINER_ID);
    new DungeonMachine(gameContainer).run();
}

const DESIGN_WIDTH = 1920;
const DESIGN_HEIGHT = 1080;

class DungeonMachine {
    constructor(gameContainer) {
        this.gameContainer = gameContainer;

        const canvas = this.#setupCanvas();
        const ui = this.#setupUI();
        
        this.resizeWindow();

        this.game = new Game(
            canvas,
            ui,
            this.#setupKeyboardHandler(),
            this.#setupMouseHandler()
        );

        //window.addEventListener('contextmenu', (e) => e.preventDefault());
        window.addEventListener('resize', () => this.resizeWindow());
    }

    #setupCanvas() {
        const canvas = document.getElementById(CANVAS_ID);
        canvas.width = DESIGN_WIDTH;
        canvas.height = DESIGN_HEIGHT;
        canvas.style.width = `${DESIGN_WIDTH}px`;
        canvas.style.height = `${DESIGN_HEIGHT}px`;
        return canvas;
    }

    #setupUI() {
        const ui = document.getElementById(UI_LAYER_ID);
        ui.style.width = `${DESIGN_WIDTH}px`;
        ui.style.height = `${DESIGN_HEIGHT}px`;
        return ui;
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

        const scaleX = w / DESIGN_WIDTH;
        const scaleY = h / DESIGN_HEIGHT;

        const scale = Math.min(scaleX, scaleY);

        this.gameContainer.style.transform = `scale(${scale})`;
    }

    run() {
        this.game.run()
    }

}