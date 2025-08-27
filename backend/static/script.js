(function () {
  const sendBtn = document.getElementById('sendBtn');
  const csvFileEl = document.getElementById('csvFile');
  const csvPreviewEl = document.getElementById('csvPreview');
  const subjectEl = document.getElementById('subject');
  const messageEl = document.getElementById('message');
  const resultEl = document.getElementById('result');

  let csvContent = '';

  function parseCSV(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const content = e.target.result;
          // Basic CSV validation
          const lines = content.split('\n');
          if (lines.length < 2) {
            reject('CSV must have at least a header row and one data row');
            return;
          }
          
          const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
          if (!headers.includes('company_name') || !headers.includes('email')) {
            reject('CSV must contain "company_name" and "email" columns');
            return;
          }
          
          resolve(content);
        } catch (error) {
          reject('Error reading CSV file: ' + error.message);
        }
      };
      reader.onerror = () => reject('Error reading file');
      reader.readAsText(file);
    });
  }

  function showCSVPreview(content) {
    const lines = content.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const dataRows = lines.slice(1, 6); // Show first 5 data rows
    
    let tableHTML = '<table><thead><tr>';
    headers.forEach(header => {
      tableHTML += `<th>${header}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';
    
    dataRows.forEach(row => {
      if (row.trim()) {
        tableHTML += '<tr>';
        row.split(',').forEach(cell => {
          tableHTML += `<td>${cell.trim()}</td>`;
        });
        tableHTML += '</tr>';
      }
    });
    
    tableHTML += '</tbody></table>';
    
    if (lines.length > 6) {
      tableHTML += `<div style="margin-top: 8px; color: var(--muted);">... and ${lines.length - 6} more rows</div>`;
    }
    
    csvPreviewEl.innerHTML = tableHTML;
    csvPreviewEl.hidden = false;
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
    const skippedCount = (payload && payload.skipped ? payload.skipped.length : 0) || 0;
    
    let summaryText = `Sent: ${sentCount}, Failed: ${failedCount}`;
    if (skippedCount > 0) {
      summaryText += `, Skipped (already sent): ${skippedCount}`;
    }
    summary.textContent = summaryText;
    resultEl.appendChild(summary);

    const details = document.createElement('pre');
    details.textContent = JSON.stringify(payload, null, 2);
    resultEl.appendChild(details);
  }

  // Handle CSV file upload
  csvFileEl.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) {
      csvPreviewEl.hidden = true;
      csvContent = '';
      return;
    }

    try {
      csvContent = await parseCSV(file);
      showCSVPreview(csvContent);
    } catch (error) {
      alert('Error: ' + error);
      csvFileEl.value = '';
      csvPreviewEl.hidden = true;
      csvContent = '';
    }
  });

  sendBtn.addEventListener('click', async () => {
    if (!csvContent) {
      alert('Please upload a CSV file.');
      return;
    }
    if (!subjectEl.value.trim()) {
      alert('Please enter a subject.');
      return;
    }
    if (!messageEl.value) {
      alert('Please enter a message template.');
      return;
    }

    setLoading(true);
    resultEl.hidden = true;

    try {
      const res = await fetch('/send-emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          csv_content: csvContent,
          subject: subjectEl.value.trim(), 
          message: messageEl.value 
        }),
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


