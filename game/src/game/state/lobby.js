import { Renderable } from "../renderer/renderable.js";
import { Button, DefaultGameButton, TextInput } from "../ui/element.js";
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

class SessionIdCopyButton extends Button {
    constructor(x, y) {
        super('Copy', x, y, 100, 50, true);
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

class CharacterDisplay extends Renderable {
    constructor(character) {
        super();
        this.character = character;
    }

    render(renderer, x, y) {
        y += 50;
        renderer.renderText(
            `Name: ${this.character.name}`, 
            x, y, 40, 'Arial', '#fff'
        );

        Object.keys(this.character.stats).forEach(stat => {
            const value = this.character.stats[stat];

            y += 60;
            renderer.renderText(
                `${stat}: ${value}`, 
                x, y, 40, 'Arial', '#fff'
            );
        });
    }
}

class CharacterNameLabel extends Renderable {
    constructor(x, y) {
        super();
    }

    render(renderer, x, y) {
        renderer.renderText('Character name', x, y, 40, 'Arial', '#fff');
    }
}

class CharacterNameInput extends TextInput {
    constructor(x, y) {
        super(x, y, 400, 70);
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
        this.characterDisplay = null;
        this.characterNameLabel = new CharacterNameLabel();

        const centerX = this.game.uiManager.getCenterX();

        this.sessionIdCopyButton = new SessionIdCopyButton(centerX, 80);
        this.sessionIdCopyButton.onClick = async () => {
            await navigator.clipboard.writeText(this.session.id);
        };

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
        );

        this.startGameButton.onClick = () => {
            // TO DO
        };

        this.characterNameInput = new CharacterNameInput(
            this.game.uiManager.getWidth() - 450,
            400
        );

        this.createCharacterButton = new DefaultGameButton(
            'Create Character',
            this.game.uiManager.getWidth() - 200,
            this.game.uiManager.getHeight() - 100
        );
        this.createCharacterButton.onClick = async () => {
            if(!this.session.localPlayer.character) {
                const name = this.characterNameInput.getValue();
                await this.session.createCharacter(name);
                this.game.uiManager.removeElement(this.characterNameInput);
            }
            this.createCharacterButton.enabled(false);
        };

        this.game.uiManager.addElements([
            this.leaveButton,
            this.startGameButton,
            this.createCharacterButton,
            this.characterNameInput,
            this.sessionIdCopyButton
        ]);

    }

    render() {
        const renderer = this.game.renderer;
        const centerX = renderer.getCenterX();

        this.sessionIdText.render(renderer, centerX, 40);
        this.playersDisplay.render(renderer, 50, 200)
        
        if(this.characterDisplay) {
            this.characterDisplay.render(renderer, renderer.getWindowWidth() - 400, 200);
        } else {
            this.characterNameLabel.render(renderer, renderer.getWindowWidth() - 450, 360);
        }
    }

    update() {
        if(this.session.localPlayer.character) {
            this.characterDisplay = new CharacterDisplay(this.session.localPlayer.character);
        }
    }
}