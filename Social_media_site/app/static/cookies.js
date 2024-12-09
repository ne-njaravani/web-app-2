window.addEventListener("load", function() {
  // Check if the user has already accepted or declined cookies
  if (!document.cookie.split('; ').find(row => row.startsWith('cookie_consent='))) {
      // Create the consent message element
      var consentMessage = document.createElement('div');
      consentMessage.id = 'cookie-consent';
      consentMessage.className = 'cookie-consent';
      consentMessage.innerHTML = `
          <span>This website uses cookies to ensure you get the best experience on our website.</span>
          <button id="cookie-consent-accept" class="cookie-consent-button">Got it!</button>
          <button id="cookie-consent-decline" class="cookie-consent-button">Decline</button>
          <a href="/privacy-policy" class="cookie-consent-link">Learn more</a>
      `;

      // Append the consent message to the footer
      document.body.appendChild(consentMessage);

      // Add event listener to the accept button to set the cookie and remove the message
      document.getElementById('cookie-consent-accept').addEventListener('click', function() {
          document.cookie = "cookie_consent=accepted; path=/; max-age=" + (60 * 60 * 24 * 365);
          document.getElementById('cookie-consent').remove();
      });

      // Add event listener to the decline button to set the cookie and remove the message
      document.getElementById('cookie-consent-decline').addEventListener('click', function() {
          document.cookie = "cookie_consent=declined; path=/; max-age=" + (60 * 60 * 24 * 365);
          document.getElementById('cookie-consent').remove();
      });
  }
});