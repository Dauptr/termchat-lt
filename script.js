// --- CONFIGURATION ---
const MQTT_HOST = "broker.hivemq.com";
const MQTT_PORT = 8000;
const MQTT_TOPIC = "termchat/lt/v1";
const ZAI_API_URL = "https://api.z.ai/v1/codegen";
const ZAI_API_KEY = "42b0a4fbe60e4568ba1b74d5e8d030d6.xSVMYljtqVXmRr33";

// --- STATE VARIABLES ---
let client;
let isConnected = false;
let nickname = "Anon" + Math.floor(Math.random() * 9999);
let inputMode = "INTRO";
let pendingAIChange = null;

// --- DOM ELEMENTS ---
const outputDiv = document.getElementById('output');
const inputField = document.getElementById('command-input');
const statusText = document.getElementById('status-text');
const introScreen = document.getElementById('intro-screen');
const chatRoom = document.getElementById('chat-room');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
  inputField.focus();
});
document.addEventListener('click', () => {
  if (window.getSelection().toString() === '') inputField.focus();
});
inputField.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const text = inputField.value.trim();
    inputField.value = '';
    if (inputMode === 'INTRO') {
      handleIntro();
    } else if (inputMode === 'CHAT') {
      handleChatCommand(text);
    }
  }
});

// --- LOGIC HANDLERS ---
function handleIntro() {
  introScreen.classList.add('hidden');
  chatRoom.classList.remove('hidden');
  inputMode = 'CHAT';
  logToTerminal("ESTABLISHING SECURE UPLINK...", "system");
  setTimeout(() => {
    logToTerminal("EXCHANGING KEYS...", "system");
    setTimeout(() => {
      connectMQTT();
    }, 500);
  }, 500);
}
function connectMQTT() {
  const clientId = "termchat-client-" + Math.random().toString(16).substr(2, 8);
  client = new Paho.MQTT.Client(MQTT_HOST, MQTT_PORT, clientId);
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;
  const options = {
    timeout: 5,
    useSSL: false,
    onSuccess: onConnect,
    onFailure: onFailure
  };
  logToTerminal(`CONNECTING TO ${MQTT_HOST}...`, "system");
  client.connect(options);
}
function handleChatCommand(text) {
  if (!isConnected) {
    logToTerminal("CONNECTION LOST. CANNOT TRANSMIT.", "system");
    return;
  }
  if (!text) return;
  if (text.startsWith('/')) {
    processCommand(text);
    return;
  }
  const message = new Paho.MQTT.Message(JSON.stringify({
    nick: nickname,
    text: sanitize(text),
    timestamp: new Date().toLocaleTimeString()
  }));
  message.destinationName = MQTT_TOPIC;
  try {
    client.send(message);
    renderMessage(nickname, text, 'user-msg');
  } catch (err) {
    logToTerminal("TRANSMISSION ERROR: " + err.message, "system");
  }
}
function processCommand(cmd) {
  const parts = cmd.split(' ');
  const command = parts[0].toLowerCase();
  switch (command) {
    case '/help':
      logToTerminal("AVAILABLE COMMANDS:", "system");
      logToTerminal(" /nick [name] - Update codename", "system");
      logToTerminal(" /clear - Clear screen", "system");
      logToTerminal(" /exit - Disconnect", "system");
      logToTerminal(" /ai [instruction] - AI code assistant (e.g. /ai change background color to blue)", "system");
      break;
    case '/nick':
      if (parts[1]) {
        const oldNick = nickname;
        nickname = sanitize(parts[1]);
        logToTerminal(`IDENTITY UPDATED: ${oldNick} -> ${nickname}`, "system");
      } else {
        logToTerminal("ERROR: NAME REQUIRED", "system");
      }
      break;
    case '/clear':
      chatRoom.innerHTML = '';
      logToTerminal("TERMINAL CLEARED.", "system");
      break;
    case '/exit':
      if(client && client.isConnected()) client.disconnect();
      location.reload();
      break;
    case '/ai':
      const aiInstruction = parts.slice(1).join(' ');
      if (aiInstruction) {
        handleAICommand(aiInstruction);
      } else {
        logToTerminal("ERROR: AI INSTRUCTION REQUIRED", "system");
      }
      break;
    default:
      logToTerminal(`UNKNOWN COMMAND: ${command}`, "system");
      break;
  }
}

// --- MQTT CALLBACKS ---
function onConnect() {
  isConnected = true;
  statusText.innerHTML = "🟢 ONLINE";
  statusText.className = "status status-online";
  client.subscribe(MQTT_TOPIC);
  logToTerminal("UPLINK ESTABLISHED.", "system");
  logToTerminal(`WELCOME, ${nickname}.`, "system");
}
function onFailure(responseObject) {
  isConnected = false;
  statusText.innerHTML = "🔴 ERR";
  statusText.className = "status status-offline";
  logToTerminal("CONN FAILED: " + responseObject.errorMessage, "system");
  logToTerminal("RETRYING...", "system");
  setTimeout(connectMQTT, 3000);
}
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    isConnected = false;
    statusText.innerHTML = "🔴 OFFLINE";
    statusText.className = "status status-offline";
    logToTerminal("UPLINK SEVERED.", "system");
  }
}
function onMessageArrived(message) {
  try {
    const payload = JSON.parse(message.payloadString);
    if (payload.nick && payload.text) {
      if (payload.nick !== nickname) {
        renderMessage(payload.nick, payload.text, 'other-msg');
      }
    }
  } catch (e) {
    logToTerminal(message.payloadString, 'other-msg');
  }
}

// --- UI HELPERS ---
function logToTerminal(text, type) {
  const line = document.createElement('div');
  line.className = type;
  const time = new Date().toLocaleTimeString([], { hour12: false });
  line.textContent = `[${time}] ${text}`;
  chatRoom.appendChild(line);
  scrollToBottom();
}
function renderMessage(nick, text, cssClass) {
  const line = document.createElement('div');
  const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit' });
  const safeNick = sanitize(nick);
  const safeText = sanitize(text);
  line.innerHTML = `<span style="opacity:0.6">[${time}]</span> <span style="font-weight:bold"><${safeNick}></span> ${safeText}`;
  line.className = cssClass;
  chatRoom.appendChild(line);
  scrollToBottom();
}
function scrollToBottom() {
  outputDiv.scrollTop = outputDiv.scrollHeight;
}
function sanitize(str) {
  return String(str).replace(/[&<>"']/g, function(m) {
    return ({
      '&': '&', '<': '<', '>': '>', '"': '"', "'": '&#39;'
    })[m];
  });
}

// --- AI COMMAND HANDLER ---
async function handleAICommand(instruction) {
  logToTerminal(`AI: Processing "${instruction}"...`, "system");
  // Only allow background color changes for safety
  if (!/^change background color to [a-zA-Z]+$/i.test(instruction.trim())) {
    logToTerminal("AI: Only 'change background color to [color]' is allowed for safety.", "system");
    return;
  }
  const color = instruction.trim().split(' ').pop().toLowerCase();
  // Confirm with user before applying
  showAIConfirmBox(color);
}
function showAIConfirmBox(color) {
  // Remove existing confirm box if any
  const oldBox = document.getElementById('ai-confirm-box');
  if (oldBox) oldBox.remove();
  const box = document.createElement('div');
  box.className = 'confirm-box';
  box.id = 'ai-confirm-box';
  box.innerHTML = `AI suggests changing background color to <b>${sanitize(color)}</b>.<br>Apply this change?
    <button class="confirm-btn" id="ai-yes">Yes</button>
    <button class="confirm-btn" id="ai-no">No</button>`;
  chatRoom.appendChild(box);
  scrollToBottom();
  document.getElementById('ai-yes').onclick = () => {
    document.body.style.backgroundColor = color;
    logToTerminal(`AI: Background color changed to ${color}.`, "system");
    box.remove();
  };
  document.getElementById('ai-no').onclick = () => {
    logToTerminal("AI: Change cancelled.", "system");
    box.remove();
  };
}
