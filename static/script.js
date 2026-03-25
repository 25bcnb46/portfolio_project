// ── Read progress bar ──────────────────────────────────────────────────────
const progressBar = document.getElementById('progress-bar');
window.addEventListener('scroll', () => {
    const pct = window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100;
    progressBar.style.width = pct + '%';
});

// ── Scroll reveal ──────────────────────────────────────────────────────────
const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
    if (entry.isIntersecting) {
        // Stagger siblings within the same parent
        const siblings = Array.from(entry.target.parentElement.querySelectorAll('.reveal:not(.visible)'));
        const idx = siblings.indexOf(entry.target);
        setTimeout(() => entry.target.classList.add('visible'), idx * 90);
        revealObserver.unobserve(entry.target);
    }
    });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Highlight active nav section ───────────────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navAs    = document.querySelectorAll('.nav-links a[href^="#"]');
window.addEventListener('scroll', () => {
    let cur = '';
    sections.forEach(s => { if (window.scrollY >= s.offsetTop - 80) cur = s.id; });
    navAs.forEach(a => {
    const isActive = a.getAttribute('href') === '#' + cur;
    if (!a.classList.contains('nav-cta')) {
        a.style.color = isActive ? 'var(--ink)' : '';
        a.style.background = isActive ? 'var(--bg2)' : '';
    }
    });
});

// ── Contact Form (Wired to your Python Backend) ────────────────────────────
const FLASK_ENDPOINT = '/submit'; // Changed from /contact to match app.py

async function submitForm() {
    const name    = document.getElementById('f-name').value.trim();
    const email   = document.getElementById('f-email').value.trim();
    const message = document.getElementById('f-message').value.trim();
    const btn     = document.getElementById('submit-btn');

    hideError();

    if (!name || !email || !message) {
        return showError('Please fill in all required fields.');
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return showError('Please enter a valid email address.');
    }

    setLoading(true, btn);

    try {
        const res = await fetch(FLASK_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        });
        
        // This parses the {"status": "success", "message": "..."} from app.py
        const data = await res.json(); 
        
        if (data.status === 'success') {
            document.getElementById('contact-form-wrap').style.display = 'none';
            document.getElementById('form-success').style.display = 'block';
        } else {
            showError(data.message || 'Something went wrong. Please try again.');
        }
    } catch (err) {
        showError('Could not connect to the server. Ensure your Flask backend is running.');
    }

    setLoading(false, btn);
}

function setLoading(on, btn) {
    btn.disabled = on;
    document.getElementById('btn-text').style.display    = on ? 'none'   : 'inline';
    document.getElementById('btn-loading').style.display = on ? 'inline' : 'none';
}

function showError(msg) {
    const el = document.getElementById('form-error');
    el.textContent = msg;
    el.style.display = 'block';
}

function hideError() {
    document.getElementById('form-error').style.display = 'none';
}

function resetForm() {
    ['f-name','f-email','f-message'].forEach(id => document.getElementById(id).value = '');
    hideError();
    document.getElementById('contact-form-wrap').style.display = 'block';
    document.getElementById('form-success').style.display = 'none';
}