export async function request(url, method, body = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (body && !['GET', 'HEAD'].includes(method.toUpperCase())) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
    }

    return await response.json();
}

export async function connectToWebSocket(url, onopen, onmessage) {
    let socket = null;

    return new Promise((resolve, reject) => {
        socket = new WebSocket(url);

        socket.onopen = () => {
            onopen(socket);
            resolve(socket);
        };

        socket.onerror = (err) => {
            reject(err);
        };

        socket.onmessage = event => { onmessage(socket, event)};
    });
}