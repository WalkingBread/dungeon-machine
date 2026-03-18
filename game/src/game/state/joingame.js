import { Renderable } from "../renderer/renderable.js";
import { getSession } from "../session/session.js";
import { TextInput, DefaultGameButton } from "../ui/element.js";
import { MenuState } from "./menu";
import { State } from "./state";
import { JoiningState } from "./joining.js";

class EnterIdText extends Renderable {
    constructor() {
        super();
    }

    render(renderer, x, y) {
        renderer.renderText('Enter game ID:', x, y, 60, 'Arial', '#fff', true);
    }
}

class SessionIdTextInput extends TextInput {
    constructor(x, y) {
        super(x, y, 400, 70, true);
    }
}

export class JoinGameState extends State {
    constructor(game, username) {
        super(game);
        this.username = username;
    }

    enter() {
        this.enterIdText = new EnterIdText();

        const centerX = this.game.uiManager.getCenterX();
        const centerY = this.game.uiManager.getCenterY();

        this.sessionIdInput = new SessionIdTextInput(centerX, centerY);

        this.backButton = new DefaultGameButton('Back', centerX, centerY + 250);
        this.backButton.onClick = () => {
            this.game.setState(new MenuState(this.game));
        };

        this.joinButton = new DefaultGameButton('Join', centerX, centerY + 120);
        this.joinButton.onClick = async () => {
            const sessionId = this.sessionIdInput.getValue();
            const session = await getSession(sessionId);
            
            this.game.setState(new JoiningState(this.game, session, this.username));
        };

        this.game.uiManager.addElements([
            this.sessionIdInput,
            this.backButton,
            this.joinButton
        ]);
    }

    render() {
        const renderer = this.game.renderer;

        const centerX = renderer.getCenterX();
        const centerY = renderer.getCenterY();

        this.enterIdText.render(renderer, centerX, centerY - 80);
    }
}