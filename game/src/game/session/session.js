import { connectToWebSocket, request } from "../utils/api.js";

const HOST = 'localhost';
const PORT = 8000;
const HTTP_BASE_URL = `http://${HOST}:${PORT}`
const WS_BASE_URL = `ws://${HOST}:${PORT}/ws`

class Player {
    constructor(sessionId, id, auth_token) {
        this.sessionId = sessionId;
        this.id = id;
        this.auth_token = auth_token;
    }

    async createCharacter(name) {
        const HTTP_ENDPOINT = `${HTTP_BASE_URL}/session/${this.sessionId}/create-character`;
        const characterData = await request(HTTP_ENDPOINT, 'POST', { 
            player_id: this.id, 
            auth_token: this.auth_token, 
            name: name
        });
    }
}

class GameSession {
    constructor(id) {
        this.id = id;
        this.socket = null;
    }

    async join(username) {
        const HTTP_ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/join`;
        const playerData = await request(HTTP_ENDPOINT, 'POST', { username : username });

        const WS_ENDPOINT = `${WS_BASE_URL}/session/${this.id}/${playerData.player_id}`;

        const webSocketOnOpen = socket => {
            socket.send(JSON.stringify({ 
                type: "AUTHENTICATE", 
                auth_token: playerData.auth_token
            }));
        };

        const webSocketOnMessage = (socket, event) => {
            const data = JSON.parse(event.data);
            console.log(data);
        };

        this.socket = await connectToWebSocket(WS_ENDPOINT, webSocketOnOpen, webSocketOnMessage); 

        return new Player(
            this.id, 
            playerData.player_id, 
            playerData.auth_token
        );
    }

    async leave(player) {
        const ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/leave`;

        await request(ENDPOINT, 'POST', { 
            player_id: player.id, 
            auth_token: player.auth_token
        });

        this.#closeConnection();
    }

    #closeConnection() {
        this.socket.close();
        this.socket = null;
    }
}

export async function createSession() {
    const ENDPOINT = `${HTTP_BASE_URL}/create-game`;

    const sessionData = await request(ENDPOINT, 'POST');

    return new GameSession(sessionData.session_id);
}

export async function getSession(sessionId) {
    const ENDPOINT = `${HTTP_BASE_URL}/session/${sessionId}`;

    const sessionData = await request(ENDPOINT, 'GET');

    return new GameSession(sessionData.session_id);
}