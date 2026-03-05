import { State } from "./state.js";

const CREATE_SESSION_ENDPOINT = 'http://localhost:8080/';

export class CreateGameState extends State {
    constructor(game, username) {
        super(game);
        this.username = username;
    }

    enter() {
        
    }

    render() {}

    update() {}

    exit() {}

    async createSession() {
        try {
            const response = await fetch(CREATE_SESSION_ENDPOINT);

        } catch(error) {
            
        }
        

    }
}