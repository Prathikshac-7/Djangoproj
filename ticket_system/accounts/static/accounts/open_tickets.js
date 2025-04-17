function enableEdit(ticketId) {
  const subjectSpan = document.getElementById(`subject${ticketId}`);
  const descSpan = document.getElementById(`description${ticketId}`);
  const saveBtn = document.getElementById(`saveBtn${ticketId}`);

  const currentSubject = subjectSpan.innerText;
  const currentDesc = descSpan.innerText;

  subjectSpan.innerHTML = `<input type="text" id="editSubject${ticketId}" class="form-control" value="${currentSubject}">`;
  descSpan.innerHTML = `<textarea id="editDesc${ticketId}" class="form-control">${currentDesc}</textarea>`;

  saveBtn.classList.remove('d-none');
}

function saveEdit(ticketId) {
  const updatedSubject = document.getElementById(`editSubject${ticketId}`).value;
  const updatedDesc = document.getElementById(`editDesc${ticketId}`).value;

  fetch(`/tickets/update/${ticketId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({
      subject: updatedSubject,
      description: updatedDesc
    }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById(`subject${ticketId}`).innerText = updatedSubject;
      document.getElementById(`description${ticketId}`).innerText = updatedDesc;
      document.getElementById(`saveBtn${ticketId}`).classList.add('d-none');
    } else {
      alert('Update failed.');
    }
  });
}

function deleteTicket(ticketId) {
  if (confirm("Are you sure you want to delete this ticket?")) {
    fetch(`/tickets/delete/${ticketId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
      },
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        const row = document.querySelector(`#ticketModal${ticketId}`).closest("tr");
        if (row) row.remove();
        document.getElementById(`ticketModal${ticketId}`).remove();
      } else {
        alert('Delete failed.');
      }
    });
  }
}

// Helper to get CSRF token
function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    if (cookie.trim().startsWith(name + '=')) {
      return decodeURIComponent(cookie.trim().substring(name.length + 1));
    }
  }
  return '';
}
