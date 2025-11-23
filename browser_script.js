// Xbox Controller Injector for Cloud Gaming
// Copy and paste this into the Developer Console (F12) of your browser while on xCloud/GeForce Now.

(function() {
    console.log("Connecting to HOTAS Emulator...");
    const ws = new WebSocket('ws://127.0.0.1:8765');
    
    let virtualGamepad = {
        id: "Xbox 360 Controller (Standard Gamepad Vendor: 045e Product: 028e)",
        index: 0,
        connected: true,
        timestamp: 0,
        mapping: "standard",
        axes: [0, 0, 0, 0],
        buttons: Array(17).fill().map(() => ({ pressed: false, value: 0 }))
    };

    ws.onopen = () => {
        console.log("Connected to HOTAS Emulator!");
        
        // 1. Override navigator.getGamepads
        const originalGetGamepads = navigator.getGamepads;
        navigator.getGamepads = function() {
            return [virtualGamepad, null, null, null];
        };

        // 2. Dispatch 'gamepadconnected' event
        // We use a generic Event and patch the gamepad property to avoid
        // "does not implement interface Gamepad" errors with plain objects.
        const event = new Event('gamepadconnected', { bubbles: true, cancelable: false });
        event.gamepad = virtualGamepad;
        window.dispatchEvent(event);
        console.log("Dispatched gamepadconnected event (Generic)");
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        virtualGamepad.timestamp = performance.now();
        virtualGamepad.axes = data.axes; // Browser handles array of numbers fine usually
        virtualGamepad.buttons = data.buttons;
        
        // Debug log every 100 updates (~1-2 seconds)
        if (!window.logCounter) window.logCounter = 0;
        window.logCounter++;
        if (window.logCounter % 100 === 0) {
            console.log("Recv Data:", data.axes[0].toFixed(2), data.buttons[0].pressed);
        }
    };

    ws.onclose = () => console.log("Disconnected from Emulator");
    ws.onerror = (e) => console.error("Emulator Error:", e);

})();
