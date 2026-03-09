import { State } from "./state.js";
import { createSession } from "../session/session.js";
import { Renderable } from "../renderer/renderable.js";
import { wait } from "../utils/async.js";
import { JoiningState } from "./joining.js";

class LoadingText extends Renderable {
    constructor() {
        super();
    }

    render(renderer, x, y) {
        renderer.renderText('Creating game session...', x, y, 60, 'Arial', '#fff', true);
    }
}

export class CreateGameState extends State {
    constructor(game, username) {
        super(game);
        this.username = username;
    }

    async enter() {
        this.loadingText = new LoadingText();

        const session = await createSession();

        await wait(1000);
       
        this.game.setState(new JoiningState(this.game, session, this.username));
    }

    render() {
        const renderer = this.game.renderer;

        this.loadingText.render(renderer, renderer.getCenterX(), renderer.getCenterY());
    }
}