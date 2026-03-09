import { Renderable } from "../renderer/renderable.js";
import { DefaultGameButton } from "../ui/element.js";
import { MenuState } from "./menu.js";
import { State } from "./state.js";

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

        const centerX = this.game.uiManager.getCenterX();

        this.leaveButton = new DefaultGameButton(
            'Leave',
            200,
            this.game.uiManager.getHeight() - 100
        );

        this.leaveButton.onClick = () => {
            this.session.leave(this.player);
            this.game.setState(new MenuState(this.game));
        };

        this.startGameButton = new DefaultGameButton(
            'Start game', 
            centerX, 
            this.game.uiManager.getHeight() - 100
        )

        this.game.uiManager.addElements([
            this.leaveButton,
            this.startGameButton
        ]);
    }

    render() {
        const renderer = this.game.renderer;
        const centerX = renderer.getCenterX();

        this.sessionIdText.render(renderer, centerX, 40);
    }
}