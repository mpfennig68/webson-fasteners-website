/* Display native navigation status; never prevent or replace form submission. */
(function () {
  'use strict';
  const form = document.querySelector('form.rfq-form');
  const status = document.getElementById('rfq-submit-status');
  if (!form || !status) return;
  const button = form.querySelector('button[type="submit"]');
  const label = button ? button.textContent : '';
  let pending;
  function reset() {
    window.clearTimeout(pending);
    status.textContent = '';
    status.hidden = true;
    form.removeAttribute('aria-busy');
    if (button) button.textContent = label;
  }
  form.addEventListener('submit', function () {
    window.clearTimeout(pending);
    form.setAttribute('aria-busy', 'true');
    status.hidden = false;
    status.textContent = 'Sending your request. Please keep this page open.';
    if (button) button.textContent = 'Sending…';
    pending = window.setTimeout(function () {
      status.textContent = 'Still sending your request. Please keep this page open until confirmation appears.';
    }, 10000);
  }, { passive: true });
  window.addEventListener('pageshow', reset);
  window.addEventListener('pagehide', function () { window.clearTimeout(pending); });
}());
