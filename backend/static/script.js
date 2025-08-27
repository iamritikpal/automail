(function () {
  const sendBtn = document.getElementById('sendBtn');
  const emailsEl = document.getElementById('emails');
  const subjectEl = document.getElementById('subject');
  const messageEl = document.getElementById('message');
  const resultEl = document.getElementById('result');

  function parseEmails(raw) {
    if (!raw) return [];
    const unique = new Set();
    raw.split(',').forEach((e) => {
      const trimmed = e.trim();
      if (trimmed) unique.add(trimmed);
    });
    return Array.from(unique);
  }

  function setLoading(isLoading) {
    sendBtn.disabled = isLoading;
    sendBtn.textContent = isLoading ? 'Sending…' : 'Send Emails';
  }

  function showResult(payload, isError) {
    resultEl.hidden = false;
    resultEl.className = 'result ' + (isError ? 'error' : 'success');
    resultEl.innerHTML = '';

    const title = document.createElement('div');
    title.textContent = isError ? 'Completed with errors' : 'Completed';
    resultEl.appendChild(title);

    const summary = document.createElement('div');
    const sentCount = (payload && payload.sent ? payload.sent.length : 0) || 0;
    const failedCount = (payload && payload.failed ? payload.failed.length : 0) || 0;
    summary.textContent = `Sent: ${sentCount}, Failed: ${failedCount}`;
    resultEl.appendChild(summary);

    const details = document.createElement('pre');
    details.textContent = JSON.stringify(payload, null, 2);
    resultEl.appendChild(details);
  }

  sendBtn.addEventListener('click', async () => {
    const emails = parseEmails(emailsEl.value);
    const subject = subjectEl.value.trim();
    const message = messageEl.value;

    if (!emails.length) {
      alert('Please enter at least one email address.');
      return;
    }
    if (!subject) {
      alert('Please enter a subject.');
      return;
    }
    if (!message) {
      alert('Please enter a message.');
      return;
    }

    setLoading(true);
    resultEl.hidden = true;

    try {
      const res = await fetch('/send-emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emails, subject, message }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        showResult(data, true);
      } else {
        showResult(data, (data.failed || []).length > 0);
      }
    } catch (err) {
      showResult({ error: String(err) }, true);
    } finally {
      setLoading(false);
    }
  });
})();


