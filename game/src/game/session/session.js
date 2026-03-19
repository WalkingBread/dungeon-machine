import { PlayerCharacter } from "../character/player.js";
import { connectToWebSocket, request } from "../utils/api.js";
import { LocalPlayer, RemotePlayer} from "./player.js"

const HOST = 'localhost';
const PORT = 8000;
const HTTP_BASE_URL = `http://${HOST}:${PORT}`
const WS_BASE_URL = `ws://${HOST}:${PORT}/ws`

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

    #handleSessionState(message) {
        const players = message.data.players;
        players.forEach(player => {
            if(player.player_id === this.localPlayer.id) {
                this.localPlayer.status = player.status;
                this.localPlayer.character = player.character;
            } else {
                this.#addRemotePlayer(player);
            }
        });
    }

    #handlePlayerLeft(message) {
        this.remotePlayers = this.remotePlayers.filter(
            player => player.id !== message.player_id
        );
    }

    #handlePlayerJoined(message) {
        this.#addRemotePlayer(message.player_data);
    }

    #handlePlayerUpdate(message) {
        const playerData = message.player_data;
        const playerId = playerData.player_id;

        if(this.localPlayer.id === playerId) {
            this.localPlayer.status = playerData.status;
            this.localPlayer.character = this.#characterFromData(playerData.character);
            return;
        }
        
        const player = this.remotePlayers.find(p => p.id === playerId);

        if (player) {
            player.status = playerData.status;
            player.character = this.#characterFromData(playerData.character);
        }
    }

    #handleWebSocketMessage(socket, message) {
        console.log(message)
        switch(message.type) {
            case 'SESSION_STATE':
                this.#handleSessionState(message);
                break;
            case 'PLAYER_LEFT':
                this.#handlePlayerLeft(message);
                break;
            case 'PLAYER_JOINED':
                this.#handlePlayerJoined(message);
                break;
            case 'PLAYER_UPDATE':
                this.#handlePlayerUpdate(message);
                break;
            case 'INFO':
                break;
            default:
                console.log(`Unknown message type: ${message.type}.`);
        }
    }

    #characterFromData(characterData) {
        return new PlayerCharacter(
            characterData.name,
            characterData.health,
            characterData.max_health,
            characterData.money,
            characterData.stats
        )
    }

    async join(username) {
        const HTTP_ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/join`;
        const playerData = await request(HTTP_ENDPOINT, 'POST', { username : username });

        this.localPlayer = new LocalPlayer(
            this.id, 
            playerData.player_id, 
            username,
            playerData.auth_token
        );

        const WS_ENDPOINT = `${WS_BASE_URL}/session/${this.id}/${playerData.player_id}`;

        const webSocketOnOpen = socket => {
            this.#authenticatePlayer(socket, playerData.auth_token);
        };

        const webSocketOnMessage = (socket, event) => {
            const message = JSON.parse(event.data);
            this.#handleWebSocketMessage(socket, message);
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

    async createCharacter(name) {
        const HTTP_ENDPOINT = `${HTTP_BASE_URL}/session/${this.id}/create-character`;
        await request(HTTP_ENDPOINT, 'POST', { 
            player_id: this.localPlayer.id, 
            auth_token: this.localPlayer.auth_token, 
            name: name
        });
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