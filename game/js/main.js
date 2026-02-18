const CANVAS_ID  = 'dm-canvas';
const FPS = 30;
const TPS = 30;
const FRAME_INTERVAL = 1000 / FPS;
const TICK_INTERVAL = 1000 / TPS;

window.onload = () => {
    const canvas = document.getElementById(CANVAS_ID);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    new DungeonMachine(canvas).run();
}

class DungeonMachine {
    constructor(canvas) {
        this.renderer = new Renderer(canvas);
        this.lastTickTime = 0;
        this.lastFrameTime = 0;
    }

    frame() {
    }

    tick() {
    }

    run() {
        const currentTime = performance.now();

        while (currentTime - this.lastTickTime >= TICK_INTERVAL) {
            this.tick();
            this.lastTickTime += TICK_INTERVAL;
        }
        if (currentTime - this.lastFrameTime >= FRAME_INTERVAL) {
            this.frame();
            this.lastFrameTime = currentTime;
        }
        requestAnimationFrame(() => this.run());
    }
}

