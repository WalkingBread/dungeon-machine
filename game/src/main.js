import { Renderer } from "./renderer.js";
import { GameLoop } from "./loop.js";

const CANVAS_ID  = 'dm-canvas';

window.onload = () => {
    const canvas = document.getElementById(CANVAS_ID);
    new DungeonMachine(canvas).run();
}

const FPS = 30;
const TPS = 30;

class DungeonMachine {
    constructor(canvas) {
        this.renderer = new Renderer(canvas);
        this.loop = new GameLoop(FPS, TPS)

        window.addEventListener('resize', this.resize_window)
        this.resize_window()
    }

    resize_window() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        this.renderer.resize(width, height);
    }

    run() {
        this.loop.setFrame(() => {
            this.renderer.clearScreen()
        })

        this.loop.setTick(() => {

        })

        this.loop.run()
    }

}