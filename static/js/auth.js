let currentUser = null;

auth.onAuthStateChanged((user) => {
    if (user) {
        currentUser = user;
        if (window.location.pathname === '/login' || window.location.pathname === '/signup' || window.location.pathname === '/') {
            window.location.href = '/notes';
        }
    } else {
        currentUser = null;
        if (window.location.pathname === '/notes') {
            window.location.href = '/';
        }
    }
});

if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const pwd = document.getElementById('password').value;
        const errMsg = document.getElementById('errorMsg');
        
        try {
            const userCred = await auth.signInWithEmailAndPassword(email, pwd);
            const token = await userCred.user.getIdToken();
            const res = await fetch('/api/verify-token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token })
            });
            if (res.ok) {
                window.location.href = '/notes';
            } else {
                throw new Error('Authentication failed');
            }
        } catch (err) {
            errMsg.textContent = err.message;
            errMsg.classList.add('show');
        }
    });
}

if (document.getElementById('signupForm')) {
    document.getElementById('signupForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const pwd = document.getElementById('password').value;
        const errMsg = document.getElementById('errorMsg');
        
        try {
            const userCred = await auth.createUserWithEmailAndPassword(email, pwd);
            await userCred.user.updateProfile({ displayName: name });
            const token = await userCred.user.getIdToken();
            const res = await fetch('/api/verify-token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token })
            });
            if (res.ok) {
                window.location.href = '/notes';
            } else {
                throw new Error('Registration failed');
            }
        } catch (err) {
            errMsg.textContent = err.message;
            errMsg.classList.add('show');
        }
    });
}

if (document.getElementById('logoutBtn')) {
    document.getElementById('logoutBtn').addEventListener('click', async () => {
        try {
            await auth.signOut();
            await fetch('/api/logout', { method: 'POST' });
            window.location.href = '/';
        } catch (err) {
            console.error('Logout error:', err);
        }
    });
}

