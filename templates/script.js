const contactForm = document.getElementById('portfolio-form');
const formMessage = document.getElementById('form-message');

contactForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const userName = document.getElementById('name').value;
    
    formMessage.style.display = 'block';
    formMessage.style.color = 'green';
    formMessage.innerText = `Thank you, ${userName}! Your message was successfully submitted.`;

    contactForm.reset();

    setTimeout(() => {
        formMessage.style.display = 'none';
    }, 5000);
});