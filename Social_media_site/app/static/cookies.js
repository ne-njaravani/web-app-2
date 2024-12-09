window.addEventListener("load", function() {
  // Check if the user has already accepted cookies
  if (!document.cookie.split('; ').find(row => row.startsWith('cookie_consent='))) {
      // Create the consent message element
      var consentMessage = document.createElement('div');
      consentMessage.id = 'cookie-consent';
      consentMessage.style.background = '#eaf7f7';
      consentMessage.style.color = '#5c7291';
      consentMessage.style.padding = '10px';
      consentMessage.style.position = 'fixed';
      consentMessage.style.bottom = '0';
      consentMessage.style.width = '100%';
      consentMessage.style.textAlign = 'center';
      consentMessage.innerHTML = `
          <span>This website uses cookies to ensure you get the best experience on our website.</span>
          <button id="cookie-consent-button" style="background: #56cbdb; color: #ffffff; border: none; padding: 5px 10px; margin-left: 10px;">Got it!</button>
          <a href="/privacy-policy" style="color: #56cbdb; margin-left: 10px;">Learn more</a>
      `;

      // Append the consent message to the footer
      document.body.appendChild(consentMessage);

      // Add event listener to the button to set the cookie and remove the message
      document.getElementById('cookie-consent-button').addEventListener('click', function() {
          document.cookie = "cookie_consent=accepted; path=/; max-age=" + (60 * 60 * 24 * 365);
          document.getElementById('cookie-consent').remove();
      });
  }
});