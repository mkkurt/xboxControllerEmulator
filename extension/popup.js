// Extension popup logic
document.addEventListener('DOMContentLoaded', () => {
  const statusDiv = document.getElementById('status');
  
  // Check if app is running
  const ws = new WebSocket('ws://127.0.0.1:8765');
  
  ws.onopen = () => {
    statusDiv.className = 'status connected';
    statusDiv.innerHTML = '<strong>Status:</strong> Connected to CloudPad app ✓';
    ws.close();
  };
  
  ws.onerror = () => {
    statusDiv.className = 'status disconnected';
    statusDiv.innerHTML = '<strong>Status:</strong> CloudPad app not running';
  };
  
  document.getElementById('help').addEventListener('click', (e) => {
    e.preventDefault();
    chrome.tabs.create({ url: 'https://github.com/yourusername/cloudpad' });
  });
});
