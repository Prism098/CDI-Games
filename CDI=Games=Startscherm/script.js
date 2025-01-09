document.getElementById('userForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const name = `${firstName} ${lastName}`;
    const status = 'not started';

    const userData = { name, email, status };

    try {
        const response = await fetch('http://localhost:4000/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            alert('Data succesvol opgeslagen!');
        } else {
            alert('Er is een fout opgetreden bij het opslaan.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Kan geen verbinding maken met de server.');
    }
});
