import { GameLoop } from './loop.js'
import { Renderer } from './renderer/renderer.js';
import { MenuState } from './state/menu.js'
import { UiManager } from './ui/manager.js';

const FPS = 30;
const TPS = 30;

export class Game {
    constructor(canvas, ui, keyboardHandler, mouseHandler, loop_config = {'fps': FPS, 'tps': TPS}) {
        this.renderer = new Renderer(canvas);
        this.uiManager = new UiManager(ui);
        this.mouseHandler = mouseHandler;
        this.keyboardHandler = keyboardHandler;
        this.loop = this.#setupLoop(loop_config);
        this.state = null;

        this.setState(new MenuState(this));
    }

    #setupLoop(loop_config) {
        return new GameLoop(
            loop_config['fps'], 
            loop_config['tps']
        )
        .setFrame(() => this.#render())
        .setTick(() => this.#update());
    }

    setState(state) {
        if(this.state) {
            this.state.exit();
        }
        state.enter();
        this.state = state;
    }

    #render() {
        this.renderer.clearScreen();
        this.state.render();
    }

    #update() {
        this.state.update();
    }

    run() {
        this.loop.run();
    }
}