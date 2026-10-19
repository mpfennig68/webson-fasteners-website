/* Confirm Formcarry acceptance before navigating; never retry automatically. */
(function () {
  'use strict';
  const form = document.querySelector('form.rfq-form');
  const status = document.getElementById('rfq-submit-status');
  if (!form || !status || !window.fetch || !window.AbortController) return;
  const button = form.querySelector('button[type="submit"]');
  const label = button ? button.textContent : '';
  let sending = false;
  function reset() {
    sending = false;
    form.removeAttribute('aria-busy');
    if (button) { button.disabled = false; button.textContent = label; }
  }
  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (sending) return;
    sending = true;
    form.setAttribute('aria-busy', 'true');
    status.hidden = false;
    status.textContent = 'Sending your request. Please keep this page open.';
    if (button) { button.disabled = true; button.textContent = 'Sending…'; }
    const controller = new AbortController();
    const slow = window.setTimeout(function () {
      status.textContent = 'Still waiting for confirmation. Please keep this page open and do not submit again.';
    }, 10000);
    const timeout = window.setTimeout(function () { controller.abort(); }, 30000);
    try {
      const response = await fetch(form.action, {
        method: 'POST', headers: { Accept: 'application/json' },
        body: new FormData(form), signal: controller.signal
      });
      const data = await response.json();
      if (response.ok && Number(data.code) === 200) {
        status.textContent = 'Request received. Opening your confirmation…';
        window.location.assign('/thank-you.html');
      } else {
        status.textContent = 'Your request was not accepted. Please check your details and try again, or email Matthew@websonfasteners.com or call (631) 243-1800.';
        reset();
      }
    } catch (error) {
      status.textContent = 'We could not confirm whether your request was received. Your entries are still here. To avoid a duplicate, please email Matthew@websonfasteners.com or call (631) 243-1800 before submitting again.';
      reset();
    } finally {
      window.clearTimeout(slow);
      window.clearTimeout(timeout);
    }
  });
  window.addEventListener('pageshow', reset);
}());
