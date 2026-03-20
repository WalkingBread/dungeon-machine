class Player {
    constructor(sessionId, id, username, status = null, character = null) {
        this.sessionId = sessionId;
        this.id = id;
        this.username = username;
        this.status = status;
        this.character = character;
    }
}

export class LocalPlayer extends Player {
    constructor(sessionId, id, username, auth_token) {
        super(sessionId, id, username);
        this.auth_token = auth_token;
    }
}

export class RemotePlayer extends Player {
    constructor(sessionId, id, username, status, character) {
        super(sessionId, id, username, status, character);
    }
}