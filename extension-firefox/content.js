// CloudPad Content Script - Auto-inject virtual gamepad
(function() {
  'use strict';
  
  console.log('CloudPad: Initializing...');
  
  // Virtual gamepad state
  let virtualGamepad = {
    id: 'CloudPad Virtual Xbox Controller',
    index: 0,
    connected: true,
    timestamp: performance.now(),
    mapping: 'standard',
    axes: [0, 0, 0, 0],
    buttons: Array(17).fill(null).map(() => ({ pressed: false, touched: false, value: 0 }))
  };
  
  // WebSocket connection to CloudPad app
  let ws = null;
  let wsConnected = false;
  
  function connectWebSocket() {
    try {
      ws = new WebSocket('ws://127.0.0.1:8765');
      
      ws.onopen = () => {
        console.log('CloudPad: Connected to local app');
        wsConnected = true;
        showNotification('CloudPad connected!', 'success');
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          updateGamepadState(data);
        } catch (e) {
          console.error('CloudPad: Invalid data', e);
        }
      };
      
      ws.onerror = () => {
        wsConnected = false;
      };
      
      ws.onclose = () => {
        wsConnected = false;
        console.log('CloudPad: Disconnected, retrying in 2s...');
        setTimeout(connectWebSocket, 2000);
      };
    } catch (e) {
      console.error('CloudPad: Connection failed', e);
      setTimeout(connectWebSocket, 2000);
    }
  }
  
  function updateGamepadState(data) {
    if (data.axes) {
      virtualGamepad.axes = data.axes;
    }
    if (data.buttons) {
      virtualGamepad.buttons = data.buttons;
    }
    virtualGamepad.timestamp = performance.now();
  }
  
  function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${type === 'success' ? '#4CAF50' : '#f44336'};
      color: white;
      padding: 16px 24px;
      border-radius: 8px;
      z-index: 999999;
      font-family: Arial, sans-serif;
      font-size: 14px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
  }
  
  // Intercept navigator.getGamepads()
  const originalGetGamepads = navigator.getGamepads.bind(navigator);
  
  navigator.getGamepads = function() {
    const realGamepads = originalGetGamepads();
    const gamepads = Array.from(realGamepads);
    
    // Insert virtual gamepad at first available slot
    if (wsConnected) {
      for (let i = 0; i < 4; i++) {
        if (!gamepads[i]) {
          virtualGamepad.index = i;
          gamepads[i] = virtualGamepad;
          break;
        }
      }
    }
    
    return gamepads;
  };
  
  // Start connection
  connectWebSocket();
  
  console.log('CloudPad: Virtual gamepad injected!');
  showNotification('CloudPad extension active', 'success');
  
})();
