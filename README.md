# TermChat LT 🟢

A terminal-style real-time chat application built with MQTT, featuring retro aesthetics and online radio streaming capabilities.

## Features

✨ **Real-time Chat** - Connect with strangers worldwide via MQTT protocol
🎨 **Retro Terminal UI** - Green phosphor CRT-style interface with typewriter effects
📻 **Radio Streaming** - Listen to online radio while chatting
📱 **Progressive Web App** - Install as native app on mobile and desktop
🌐 **No Installation Required** - Works in any modern web browser
🇱🇹 **Lithuanian Language Support** - Native UI and system messages in Lithuanian

## Installation

### Web Browser
Simply open `index.html` in your browser or visit the hosted URL.

### Progressive Web App (PWA)
1. Open the app in your browser
2. Click the "Install" button (or menu → "Install app")
3. The app installs as a native application on your device
4. Works offline with cached content

## How to Use

### Chat
1. Type your message in the terminal prompt
2. Press Enter to send
3. Incoming messages from other users appear in real-time
4. System messages notify you of new connections

### Radio
1. Click the **LISTEN** button in the bottom-right
2. Button changes to **STOP** while playing
3. Click again to stop the stream

### Keyboard Shortcuts
- `Enter` - Send message
- `Ctrl+L` (or system menu) - Browser-based shortcuts

## Technical Details

### MQTT Broker
- **Host**: broker.emqx.io
- **Port**: 8084
- **Topic**: term-chat/global/v3
- **Protocol**: WebSocket Secure (WSS)

### Radio Stream
- **URL**: https://uk7.internet-radio.com:8000
- **Type**: AAC/MP3 streaming
- **Status**: Public online radio

### Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Real-time**: MQTT.js (Paho client)
- **PWA**: Service Worker, Web Manifest
- **Styling**: CSS variables, Flexbox, Animations
- **Audio**: Native HTML5 Audio API

## PWA Features

✅ **Installable** - Add to home screen
✅ **Offline Support** - Static assets cached locally
✅ **Standalone Mode** - Runs without browser chrome
✅ **Push Notifications** - (Ready for future integration)
✅ **Background Sync** - (Ready for future integration)

## Browser Support

| Browser | Support | PWA |
|---------|---------|-----|
| Chrome 50+ | ✅ Full | ✅ |
| Firefox 55+ | ✅ Full | ✅ |
| Safari 11+ | ✅ Full | ⚠️ Limited |
| Edge 17+ | ✅ Full | ✅ |
| Mobile Chrome | ✅ Full | ✅ |
| Mobile Safari | ✅ Full | ⚠️ Limited |

## File Structure

```
termchat-lt/
├── index.html          # Main app (HTML + CSS + JS)
├── manifest.json       # PWA configuration
├── sw.js              # Service Worker (offline support)
├── style.css          # (Optional separate styling)
├── script.js          # (Optional separate scripts)
└── README.md          # This file
```

## Setup & Deployment

### Local Development
```bash
# Start local server
python3 -m http.server 8000

# Open browser to
http://localhost:8000
```

### GitHub Pages
```bash
# Push to GitHub repository
git add .
git commit -m "Add PWA support"
git push origin main

# Enable GitHub Pages in settings
# Choose 'main' branch as source
```

### Self-Hosted Server
```bash
# Copy files to web server
scp -r termchat-lt/ user@server:/var/www/

# Ensure HTTPS is enabled for PWA features
```

## Configuration

### Change Radio Stream
Edit `index.html` line with `RADIO_STREAM`:
```javascript
const RADIO_STREAM = "https://your-radio-url.com:8000";
```

### Change MQTT Topic
Edit `index.html` line with `TOPIC`:
```javascript
const TOPIC = "your-custom/topic/path";
```

### Customize Theme
Edit CSS variables in `index.html`:
```css
:root {
    --term-green: #00ff00;      /* Main text color */
    --term-bg: #000000;         /* Background */
    --term-glow: 0 0 5px rgba(0, 255, 0, 0.7);  /* Glow effect */
}
```

## Troubleshooting

### Chat not connecting
- Check internet connection
- Verify MQTT broker is online (broker.emqx.io)
- Check browser console for errors

### Radio won't play
- Verify radio stream URL is accessible
- Check CORS settings (may need proxy)
- Try in different browser

### PWA not installing
- Requires HTTPS (or localhost)
- Check manifest.json is valid
- Service Worker must register successfully
- Clear browser cache and reload

## Future Enhancements

- [ ] User authentication
- [ ] Private messages
- [ ] Message history
- [ ] User profiles
- [ ] Emoji support
- [ ] File sharing
- [ ] Voice chat
- [ ] Custom themes
- [ ] Push notifications
- [ ] Message encryption

## License

Open source - Feel free to use and modify

## Contributing

Pull requests welcome! Feel free to fork and improve.

## Support

For issues or questions, check the browser console for error logs.

---

**Made with ❤️ using MQTT & Web Standards**
