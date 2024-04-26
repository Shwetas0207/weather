document.getElementById('toggle-register').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
});

document.getElementById('toggle-login').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
});

const togglePasswordIcons = document.querySelectorAll('.toggle-password');

togglePasswordIcons.forEach(icon => {
  icon.addEventListener('click', () => {
    const passwordInput = icon.previousElementSibling;
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
  });
});


document.getElementById('login-btn').addEventListener('click', function(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    fetch('http://192.168.0.106:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Invalid username or password.');
        }
        return response.json();
    })
    .then(data => {
        // Store JWT token in local storage
        localStorage.setItem('jwt', data.jwt);

        // handle successful login, for example:
        console.log(data); // log the response
        alert('Login successful!'); // show an alert

        // Redirect to home page or perform other actions
        window.location.href = 'home.html'; // Redirect to home page
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed. ' + error.message); // show an alert with error message
    });
});

// Function to fetch data using JWT token
function fetchData() {
    const jwt = localStorage.getItem('jwt');
    if (!jwt) {
        console.error('JWT token not found in local storage.');
        return;
    }
    fetch('http://192.168.0.106:8000/some-api-endpoint', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${jwt}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch data.');
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Log fetched data
        // Handle the fetched data as needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Call the fetchData function when the window loads, for example:
window.onload = fetchData;


document.getElementById('register-btn').addEventListener('click', function(event) {
    event.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    fetch('http://192.168.0.106:8000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Registration failed.');
        }
        return response.json();
    })
    .then(data => {
        // handle successful registration, for example:
        console.log(data); // log the response
        alert('Registration successful!'); // show an alert
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Registration failed. ' + error.message); // show an alert with error message
    });
});