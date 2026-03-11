import { connectToWebSocket, request } from "../utils/api.js";

const HOST = 'localhost';
const PORT = 8000;
const HTTP_BASE_URL = `http://${HOST}:${PORT}`
const WS_BASE_URL = `ws://${HOST}:${PORT}/ws`

class Player {
    constructor(sessionId, id, username, status, character = null) {
        this.sessionId = sessionId;
        this.id = id;
        this.username = username;
        this.status = status;
        this.character = character;
    }
}

class LocalPlayer extends Player {
    constructor(sessionId, id, username, status, auth_token) {
        super(sessionId, id, username, status);
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

class RemotePlayer extends Player {
    constructor(sessionId, id, username, status, character) {
        super(sessionId, id, username, status, character);
    }
}

class GameSession {
    constructor(id) {
        this.id = id;
        this.remotePlayers = [];
        this.localPlayer = null;
        this.socket = null;
    }

    #addRemotePlayer(playerData) {
        this.remotePlayers.push(new RemotePlayer(
            this.id,
            playerData.player_id,
            playerData.username,
            playerData.status,
            playerData.character
        ));
    }

    #authenticatePlayer(socket, auth_token) {
        socket.send(JSON.stringify({ 
            type: "AUTHENTICATE", 
            data: {
                auth_token: auth_token
            }
        }));
    }

    async join(username) {
        const HTTP_ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/join`;
        const playerData = await request(HTTP_ENDPOINT, 'POST', { username : username });

        const WS_ENDPOINT = `${WS_BASE_URL}/session/${this.id}/${playerData.player_id}`;

        const webSocketOnOpen = socket => {
            this.#authenticatePlayer(socket, playerData.auth_token);
        };

        const webSocketOnMessage = (socket, event) => {
            const message = JSON.parse(event.data);
            if(message.type === 'SESSION_STATE') {
                const players = message.data.players;
                players.forEach(player => {
                    if(player.player_id === playerData.player_id) {
                        this.localPlayer = new LocalPlayer(
                            this.id,
                            player.player_id, 
                            player.username,
                            player.status,
                            playerData.auth_token,
                            username
                        )
                    } else {
                        this.#addRemotePlayer(player);
                    }
                });
                console.log(this.remotePlayers);
                console.log(this.localPlayer);
            }
        };

        this.socket = await connectToWebSocket(WS_ENDPOINT, webSocketOnOpen, webSocketOnMessage); 
    }

    async leave() {
        const ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/leave`;

        await request(ENDPOINT, 'POST', { 
            player_id: this.localPlayer.id, 
            auth_token: this.localPlayer.auth_token
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