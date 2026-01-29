/* --- CONFIGURATION --- */
const MQTT_HOST = "broker.hivemq.com";
const MQTT_PORT = 8000;
const MQTT_TOPIC = "termchat/lt/v1"; // Shared channel for everyone using this code

/* --- STATE VARIABLES --- */
let client;
let isConnected = false;
let nickname = "Anon" + Math.floor(Math.random() * 9999);
let inputMode = "INTRO"; // 'INTRO', 'NICKNAME', 'CHAT'

/* --- DOM ELEMENTS --- */
const outputDiv = document.getElementById('output');
const inputField = document.getElementById('command-input');
const statusText = document.getElementById('status-text');
const introScreen = document.getElementById('intro-screen');
const chatRoom = document.getElementById('chat-room');

/* --- INITIALIZATION --- */
document.addEventListener('DOMContentLoaded', () => {
    inputField.focus();
});

// Keep focus on input unless user specifically selects text
document.addEventListener('click', () => {
    inputField.focus();
});

inputField.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const text = inputField.value.trim();
        inputField.value = ''; // Clear input immediately for responsiveness

        if (inputMode === 'INTRO') {
            handleIntro();
        } else if (inputMode === 'CHAT') {
            handleChatCommand(text);
        }
    }
});

/* --- LOGIC HANDLERS --- */

function handleIntro() {
    introScreen.classList.add('hidden');
    chatRoom.classList.remove('hidden');
    inputMode = 'CHAT';
    
    logToTerminal("ESTABLISHING SECURE UPLINK...", "system");
    logToTerminal("INITIATING HANDSHAKE...", "system");
    
    // Small delay to simulate connection process
    setTimeout(() => {
        connectMQTT();
    }, 800);
}

function connectMQTT() {
    // Generate a random client ID
    const clientId = "termchat-client-" + Math.random().toString(16).substr(2, 8);

    client = new Paho.MQTT.Client(MQTT_HOST, MQTT_PORT, clientId);

    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    const options = {
        timeout: 3,
        useSSL: false, // Set to true if using port 8883 (WSS)
        onSuccess: onConnect,
        onFailure: onFailure
    };

    client.connect(options);
}

function handleChatCommand(text) {
    if (!isConnected) {
        logToTerminal("CONNECTION LOST. CANNOT TRANSMIT.", "system");
        return;
    }

    if (!text) return; // Ignore empty strings

    // Check for commands
    if (text.startsWith('/')) {
        processCommand(text);
        return;
    }

    // Send standard message
    const message = new Paho.MQTT.Message(JSON.stringify({
        nick: nickname,
        text: text,
        timestamp: new Date().toLocaleTimeString()
    }));
    message.destinationName = MQTT_TOPIC;
    client.send(message);

    // Render locally immediately
    renderMessage(nickname, text, 'user-msg');
}

function processCommand(cmd) {
    const parts = cmd.split(' ');
    const command = parts[0].toLowerCase();

    switch (command) {
        case '/help':
            logToTerminal("AVAILABLE COMMANDS:", "system");
            logToTerminal("  /nick [name]  - Change your codename", "system");
            logToTerminal("  /clear        - Clear terminal buffer", "system");
            logToTerminal("  /exit         - Terminate session", "system");
            break;
        case '/nick':
            if (parts[1]) {
                const oldNick = nickname;
                nickname = parts[1];
                logToTerminal(`IDENTITY UPDATED: ${oldNick} -> ${nickname}`, "system");
            } else {
                logToTerminal("ERROR: NEW NAME REQUIRED", "system");
            }
            break;
        case '/clear':
            // Remove
