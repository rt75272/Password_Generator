// ------------------------------------------------------------------------------------
// Copy Button Script for Multiple Password Options
//
// Copy-to-clipboard helper for multiple password options
// Listens for clicks on copy buttons and writes the corresponding password
// to the user's clipboard using the asynchronous Clipboard API.
//
// Usage:
// 1. Include this script in your HTML file (e.g., at the end of the body).
// 2. Ensure there are buttons with class="btn-copy" and corresponding password elements.
// ------------------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  // Get all copy buttons
  const copyButtons = document.querySelectorAll('.btn-copy');
  // Add click handler to each copy button
  copyButtons.forEach((copyBtn, index) => {
    copyBtn.addEventListener('click', async () => {
      // Find the password text element in the same password option
      const passwordOption = copyBtn.closest('.password-option');
      const passwordEl = passwordOption ? passwordOption.querySelector('.password-text') : null;
      // Fallback: if we can't find the password element, try data attribute
      let text = '';
      if (passwordEl) {
        text = passwordEl.textContent.trim();
      } else if (copyBtn.dataset.target !== undefined) {
        // Alternative: get password from data attribute
        text = passwordEl ? passwordEl.dataset.password : '';
      }
      // If still no text found, try to get from the password text element
      if (!text && passwordEl) {
        text = passwordEl.textContent.trim();
      }
      if (!text) {
        copyBtn.textContent = 'No password';
        setTimeout(() => (copyBtn.textContent = 'Copy'), 1500);
        return;
      }
      try {
        // navigator.clipboard is modern and promise-based; it requires
        // a secure context (HTTPS or localhost). If it succeeds, show feedback.
        await navigator.clipboard.writeText(text);
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.color = '#4ade80';
        
        setTimeout(() => {
          copyBtn.textContent = originalText;
          copyBtn.style.color = '';
        }, 1500);
      } catch (err) {
        // On failure (older browsers or permissions), show brief error text.
        // We intentionally keep the UX simple; a production app might
        // implement a fallback using a hidden textarea + execCommand.
        copyBtn.textContent = 'Failed';
        setTimeout(() => (copyBtn.textContent = 'Copy'), 1500);
      }
    });
  });
});
