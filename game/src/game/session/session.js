import { connectToWebSocket, request } from "../utils/api.js";

const HOST = 'localhost';
const PORT = 8000;
const HTTP_BASE_URL = `http://${HOST}:${PORT}`
const WS_BASE_URL = `ws://${HOST}:${PORT}/ws`

class Player {
    constructor(id) {
        this.id = id;
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
        this.socket = await connectToWebSocket(WS_ENDPOINT, event => {
            console.log(JSON.parse(event.data));
        });

        return new Player(playerData.player_id);
    }

    async leave(player) {
        const ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/leave`;

        await request(ENDPOINT, 'POST', { player_id: player.id });

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