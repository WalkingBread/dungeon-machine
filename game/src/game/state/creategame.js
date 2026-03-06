import { State } from "./state.js";
import { createSession } from "../session/session.js";
import { Renderable } from "../renderer/renderable.js";
import { wait } from "../utils/async.js";
import { LobbyState } from "./lobby.js";

class LoadingText extends Renderable {
    constructor() {
        super();
        this.text = '';
    }

    render(renderer, x, y) {
        renderer.renderText(this.text, x, y, 60, 'Arial', '#fff', true);
    }
}

export class CreateGameState extends State {
    constructor(game, username) {
        super(game);
        this.username = username;
    }

    async enter() {
        this.loadingText = new LoadingText();
        this.loadingText.text = 'Creating game session...';

        const session = await createSession();

        await wait(1000);
        this.loadingText.text = 'Joining...'

        const player = await session.join(this.username);

        await wait(1000);
        this.game.setState(new LobbyState(this.game, session, player));
    }

    render() {
        const renderer = this.game.renderer;

        const centerX = renderer.getWindowWidth() / 2;
        const centerY = renderer.getWindowHeight() / 2;

        this.loadingText.render(renderer, centerX, centerY);
    }
}