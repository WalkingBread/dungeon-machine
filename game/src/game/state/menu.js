import { State } from './state.js'
import { Renderable, Sprite } from '../renderer/renderable.js'
import { GameImage } from '../renderer/image.js';
import { TextInput, Button} from '../ui/element.js'
import { CreateGameState } from './creategame.js';
import { JoinGameState } from './joingame.js';

const LOGO_SRC = 'https://www.pngmart.com/files/23/Dungeons-And-Dragons-Logo-PNG-File.png';

class Logo extends Sprite {
    constructor() {
        super(new GameImage(LOGO_SRC), 600, 200);
    }
}

class UsernameTextInput extends TextInput {
    constructor(x, y) {
        super(x, y, 400, 70, true);
    }
}

class CreateGameButton extends Button {
    constructor(x, y) {
        super('Create game', x, y, 300, 100, true);
    }
}

class JoinGameButton extends Button {
    constructor(x, y) {
        super('Join game', x, y, 300, 100, true);
    }
}

class UsernameText extends Renderable {
    constructor() {
        super();
    }

    render(renderer, x, y) {
        renderer.renderText('Username:', x, y, 40, 'Arial', '#fff', true);
    }
}

function isValidUsername(username) {
    const regex = /^[a-zA-Z0-9_]{3,16}$/;
    return regex.test(username);
}

export class MenuState extends State {
    constructor(game) {
        super(game);
    }

    enter() {
        this.logo = new Logo();

        this.usernameText = new UsernameText();

        const centerX = this.game.uiManager.getWidth() / 2;

        this.usernameInput = new UsernameTextInput(centerX, 470);
        this.createGameButton = new CreateGameButton(centerX, 650);
        this.joinGameButton = new JoinGameButton(centerX, 800);

        this.createGameButton.enabled(false);
        this.joinGameButton.enabled(false);

        this.usernameInput.onType = () => {
            const isValid = isValidUsername(this.usernameInput.getValue());

            this.createGameButton.enabled(isValid);
            this.joinGameButton.enabled(isValid);
        };

        this.createGameButton.onClick = () => {
            const username = this.usernameInput.getValue();
            this.game.setState(new CreateGameState(this.game, username));
        };

        this.joinGameButton.onClick = () => {
            const username = this.usernameInput.getValue();
            this.game.setState(new JoinGameState(this.game, username));
        };

        this.game.uiManager.addElements([
            this.usernameInput,
            this.createGameButton,
            this.joinGameButton
        ]);
    }

    render() {
        const centerX = this.game.uiManager.getWidth() / 2;

        this.logo.render(this.game.renderer, centerX, 200, true);
        this.usernameText.render(this.game.renderer, centerX, 400);
    }
}