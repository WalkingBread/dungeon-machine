import { GameLoop } from './loop.js'
import { MenuState } from './state.js'

const FPS = 30;
const TPS = 30;

export class Game {
    constructor(renderer, uiManager, keyboardHandler, mouseHandler, loop_config = {'fps': FPS, 'tps': TPS}) {
        this.renderer = renderer
        this.uiManager = uiManager;
        this.mouseHandler = mouseHandler;
        this.keyboardHandler = keyboardHandler;
        this.loop = this.#setupLoop(loop_config)
        this.state = null;
        
        this.#setState(new MenuState(uiManager));
    }

    #setupLoop(loop_config) {
        return new GameLoop(
            loop_config['fps'], 
            loop_config['tps']
        )
        .setFrame(() => this.#render())
        .setTick(() => this.#update())
    }

    #setState(state) {
        if(this.state) {
            this.state.exit();
        }
        state.enter();
        this.state = state;
    }

    #render() {
        this.renderer.clearScreen()
        this.state.render()
    }

    #update() {
        this.state.update()
    }

    run() {
        this.loop.run()
    }
}