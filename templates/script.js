document.getElementById('contactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Grab elements
    const submitBtn = e.target.querySelector('button');
    const statusDiv = document.getElementById('status');
    
    // UI Loading state
    const originalText = submitBtn.innerText;
    submitBtn.innerText = 'Sending...';
    
    const name = document.getElementById('name').value;
    const message = document.getElementById('message').value;

    try {
        // Talk to the Python backend
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, message })
        });

        const result = await response.json();
        
        // Show success UI
        statusDiv.innerText = result.message;
        statusDiv.classList.remove('hidden');
        document.getElementById('contactForm').reset();
        
    } catch (error) {
        console.error("Error:", error);
        statusDiv.innerText = "Something went wrong.";
        statusDiv.classList.remove('hidden');
        statusDiv.classList.replace('text-green-400', 'text-red-400');
    } finally {
        // Reset button state
        submitBtn.innerText = originalText;
        
        // Hide the status message after 3 seconds
        setTimeout(() => {
            statusDiv.classList.add('hidden');
        }, 3000);
    }
});