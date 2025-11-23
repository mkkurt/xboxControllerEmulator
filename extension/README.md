# CloudPad Chrome Extension

## Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension` folder

## Usage

1. Start the CloudPad desktop app
2. Navigate to a cloud gaming site (Xbox Cloud Gaming, GeForce NOW, etc.)
3. The extension will auto-connect and inject a virtual Xbox controller
4. Your physical controller will now work on the cloud gaming platform!

## Supported Platforms

- Xbox Cloud Gaming (xbox.com)
- GeForce NOW
- Amazon Luna
- Google Stadia

## Troubleshooting

**Extension shows "CloudPad app not running":**
- Make sure the CloudPad desktop app is open and running
- Check that the app shows "WebSocket server running on ws://127.0.0.1:8765"

**Controller not detected in game:**
- Refresh the browser page after connecting your controller
- Check the extension popup to verify connection status
- Open browser console (F12) and look for "CloudPad: Connected" message

## Icons

Note: The extension currently uses placeholder icons. For production, create:
- icon16.png (16x16)
- icon48.png (48x48)  
- icon128.png (128x128)
