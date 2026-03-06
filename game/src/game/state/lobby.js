import { Renderable } from "../renderer/renderable";
import { State } from "./state";

class SessionIdText extends Renderable {
    constructor(sessionId) {
        super();
        this.sessionId = sessionId;
    }

    render(renderer, x, y) {
        renderer.renderText(`Session ID: ${this.sessionId}`, x, y, 30, 'Arial', '#fff', true);
    }
}

export class LobbyState extends State {
    constructor(game, session, player) {
        super(game);
        this.session = session;
        this.player = player;
    }

    enter() {
        this.sessionIdText = new SessionIdText(this.session.id);
    }

    render() {
        const renderer = this.game.renderer;
        const centerX = renderer.getCenterX();

        this.sessionIdText.render(renderer, centerX, 40);
    }
}