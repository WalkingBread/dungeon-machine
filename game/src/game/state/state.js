export class State {
    constructor(game) {
        this.game = game;
        this.game.uiManager.clear();
    }

    enter() {}
    render() {}
    update() {}
    exit() {}
}