document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');
    const toast = document.getElementById('toast');
    const form = this;

    // UI Loading State
    btnText.classList.add('hidden');
    loader.classList.remove('hidden');
    toast.classList.add('hidden');

    const payload = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // UI Reset
        loader.classList.add('hidden');
        btnText.classList.remove('hidden');

        // Show Custom Notification
        toast.classList.remove('hidden', 'success', 'error');
        if(result.status === 'success') {
            toast.textContent = "🚀 " + result.message;
            toast.classList.add('success');
            form.reset(); // Clear the form
        } else {
            toast.textContent = "⚠️ " + result.message;
            toast.classList.add('error');
        }

    } catch (error) {
        loader.classList.add('hidden');
        btnText.classList.remove('hidden');
        toast.textContent = "⚠️ Network error. Please try again.";
        toast.classList.remove('hidden');
        toast.classList.add('error');
    }
});
