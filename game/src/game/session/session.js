import { request } from "../utils/api.js";

const HOST = 'localhost';
const PORT = 8000;
const BASE_URL = `http://${HOST}:${PORT}`

class Player {
    constructor(id) {
        this.id = id;
    }
}

class GameSession {
    constructor(id) {
        this.id = id;
    }

    async join(username) {
        const ENDPOINT = `${BASE_URL}/session/${this.id}/join`;

        const playerData = await request(ENDPOINT, 'POST', { username : username })

        return new Player(playerData.player_id);
    }

    async leave(player) {
        const ENDPOINT = `${BASE_URL}/session/${this.id}/leave`;

        await request(ENDPOINT, 'POST', { player_id: player.id });
    }
}

export async function createSession() {
    const ENDPOINT = `${BASE_URL}/create-game`;

    const sessionData = await request(ENDPOINT, 'POST');

    return new GameSession(sessionData.session_id);
}

export async function getSession(sessionId) {
    const ENDPOINT = `${BASE_URL}/session/${sessionId}`;

    const sessionData = await request(ENDPOINT, 'GET');

    return new GameSession(sessionData.session_id);
}