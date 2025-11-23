// Background service worker for CloudPad extension
console.log('CloudPad extension loaded');

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'STATUS') {
    sendResponse({ status: 'active' });
  }
  return true;
});
