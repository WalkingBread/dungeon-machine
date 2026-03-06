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

        const response = await fetch(ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to join session");
        }

        const data = await response.json();

        console.log(`Joined as ${username}. Player ID: ${data.player_id}`);

        return new Player(data.player_id);
    }
}

export async function createSession() {
    const ENDPOINT = `${BASE_URL}/create-game`

    try {
        const response = await fetch(ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Error ${response.status}: ${errorData.detail}`);
        }

        const data = await response.json();
        console.log("Game created! Session ID:", data.session_id);
        
        return new GameSession(data.session_id);

    } catch (error) {
        console.error("Failed to create game:", error.message);
        throw error;
    }
}