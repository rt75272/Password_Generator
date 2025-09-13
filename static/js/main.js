// ------------------------------------------------------------------------------------
// Copy Button Script
//
// Copy-to-clipboard helper
// Listens for clicks on the copy button and writes the displayed password
// to the user's clipboard using the asynchronous Clipboard API.
//
// Usgage:
// 1. Include this script in your HTML file (e.g., at the end of the body).
// 2. Ensure there is a button with id="copyBtn" and an element with id="passwordText".
// ------------------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  // Grab references to the button and the element containing the password.
  const copyBtn = document.getElementById('copyBtn');
  const passwordEl = document.getElementById('passwordText');
  // If either element is missing (template changed), do nothing.
  if (!copyBtn || !passwordEl) return;
  // Handle click event. Uses async/await for the clipboard call.
  copyBtn.addEventListener('click', async () => {
    // Trim whitespace and ensure there is something to copy.
    const text = passwordEl.textContent.trim();
    if (!text) return;
    try {
      // navigator.clipboard is modern and promise-based; it requires
      // a secure context (HTTPS or localhost). If it succeeds, show feedback.
      await navigator.clipboard.writeText(text);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => (copyBtn.textContent = 'Copy'), 1500);
    } catch (err) {
      // On failure (older browsers or permissions), show brief error text.
      // We intentionally keep the UX simple; a production app might
      // implement a fallback using a hidden textarea + execCommand.
      copyBtn.textContent = 'Failed';
      setTimeout(() => (copyBtn.textContent = 'Copy'), 1500);
    }
  });
});
