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

class PlayersInLobbyDisplay extends Renderable {
    constructor(session) {
        super();
        this.session = session;
    }

    render(renderer, x, y) {
        y += 50;
        renderer.renderText(
            `${this.session.localPlayer.username}: ${this.session.localPlayer.status}`, 
            x, y, 40, 'Arial', '#fff'
        );

        this.session.remotePlayers.forEach(player => {
            y += 60;
            renderer.renderText(
                `${player.username}: ${player.status}`, 
                x, y, 40, 'Arial', '#fff'
            );
        });
    }
}

export class LobbyState extends State {
    constructor(game, session) {
        super(game);
        this.session = session;
    }

    enter() {
    
        this.sessionIdText = new SessionIdText(this.session.id);
        this.playersDisplay = new PlayersInLobbyDisplay(this.session);

        const centerX = this.game.uiManager.getCenterX();

        this.leaveButton = new DefaultGameButton(
            'Leave',
            200,
            this.game.uiManager.getHeight() - 100
        );

        this.leaveButton.onClick = () => {
            this.session.leave();
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
        this.playersDisplay.render(renderer, 50, 200)
    }
}