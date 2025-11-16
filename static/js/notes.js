let notes = [];
let currNoteId = null;
const modal = document.getElementById('noteModal');
const noteForm = document.getElementById('noteForm');
const notesGrid = document.getElementById('notesGrid');
const emptyState = document.getElementById('emptyState');

auth.onAuthStateChanged(async (user) => {
    if (user) {
        const token = await user.getIdToken();
        await fetch('/api/verify-token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });
        loadNotes();
    }
});

async function loadNotes() {
    try {
        const res = await fetch('/api/notes');
        if (res.ok) {
            notes = await res.json();
            renderNotes();
        }
    } catch (err) {
        console.error('Error loading notes:', err);
    }
}

function renderNotes() {
    notesGrid.innerHTML = '';
    if (notes.length === 0) {
        emptyState.classList.add('show');
        return;
    }
    emptyState.classList.remove('show');
    notes.forEach(note => {
        const card = document.createElement('div');
        card.className = 'note-card';
        card.innerHTML = `
            <h3>${escapeHtml(note.title || 'Untitled')}</h3>
            <p>${escapeHtml(note.content || '')}</p>
            <div class="note-date">${formatDate(note.updated || note.created)}</div>
        `;
        card.addEventListener('click', () => openNote(note));
        notesGrid.appendChild(card);
    });
}

function openNote(note = null) {
    currNoteId = note ? note.id : null;
    document.getElementById('modalTitle').textContent = note ? 'Edit Note' : 'New Note';
    document.getElementById('noteTitle').value = note ? note.title : '';
    document.getElementById('noteContent').value = note ? note.content : '';
    document.getElementById('deleteNoteBtn').style.display = note ? 'block' : 'none';
    modal.classList.add('show');
}

function closeModal() {
    modal.classList.remove('show');
    currNoteId = null;
    noteForm.reset();
}

noteForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('noteTitle').value;
    const content = document.getElementById('noteContent').value;
    
    try {
        if (currNoteId) {
            const res = await fetch(`/api/notes/${currNoteId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, content })
            });
            if (res.ok) {
                loadNotes();
                closeModal();
            }
        } else {
            const res = await fetch('/api/notes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, content })
            });
            if (res.ok) {
                loadNotes();
                closeModal();
            }
        }
    } catch (err) {
        console.error('Error saving note:', err);
    }
});

document.getElementById('newNoteBtn').addEventListener('click', () => openNote());
document.getElementById('closeModal').addEventListener('click', closeModal);
document.getElementById('cancelBtn').addEventListener('click', closeModal);

document.getElementById('deleteNoteBtn').addEventListener('click', async () => {
    if (!currNoteId) return;
    if (!confirm('Are you sure you want to delete this note?')) return;
    
    try {
        const res = await fetch(`/api/notes/${currNoteId}`, { method: 'DELETE' });
        if (res.ok) {
            loadNotes();
            closeModal();
        }
    } catch (err) {
        console.error('Error deleting note:', err);
    }
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(timestamp) {
    if (!timestamp) return '';
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

