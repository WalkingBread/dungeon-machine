export class GameLoop {
    constructor(fps, tps) {
        this.fps = fps;
        this.tps = tps;
        this.frameInterval = 1000 / fps;
        this.tickInterval = 1000 / tps;
        this.lastFrameTime = 0;
        this.lastTickTime = 0;
        this.frame = () => {}
        this.tick = () => {}
    }

    setFrame(frame) {
        this.frame = frame;
        return this
    }

    setTick(tick) {
        this.tick = tick;
        return this
    }

    run() {
        const currentTime = performance.now();

        while (currentTime - this.lastTickTime >= this.frameInterval) {
            this.tick();
            this.lastTickTime = currentTime;
        }
        if (currentTime - this.lastFrameTime >= this.tickInterval) {
            this.frame();
            this.lastFrameTime = currentTime;
        }
        requestAnimationFrame(() => this.run());
    }
}