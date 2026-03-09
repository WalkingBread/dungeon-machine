import { LobbyState } from "./lobby.js";
import { State } from "./state.js";
import { Renderable } from "../renderer/renderable.js";
import { wait } from "../utils/async.js";

class LoadingText extends Renderable {
    constructor() {
        super();
    }

    render(renderer, x, y) {
        renderer.renderText('Joining...', x, y, 60, 'Arial', '#fff', true);
    }
}

export class JoiningState extends State {
    constructor(game, session, username) {
        super(game);
        this.session = session;
        this.username = username;
    }

    async enter() {
        this.loadingText = new LoadingText();

        const player = await this.session.join(this.username);
        await this.session.joinWs(player);

        await wait(1000);
               
        this.game.setState(new LobbyState(this.game, this.session, player));
    }

    render() {
        const renderer = this.game.renderer;
        this.loadingText.render(renderer, renderer.getCenterX(), renderer.getCenterY());
    }
}