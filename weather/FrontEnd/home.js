// Function to fetch user's profile and display name
async function getProfile() {
    try {
        const jwt = localStorage.getItem('jwt');
        const response = await fetch('http://192.168.0.106:8000/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ jwt: jwt })
        });
        if (!response.ok) {
            throw new Error('Failed to fetch user profile.');
        }
        const data = await response.json();
        document.getElementById('user-name').textContent = data.username; // Display user's name in the navbar
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to add a city and its weather data
async function addCity() {
    try {
        const jwt = localStorage.getItem('jwt');
        const city = document.getElementById('city-input').value;
        const response = await fetch('http://192.168.0.106:8000/add_city_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ jwt: jwt, city: city })
        });
        if (!response.ok) {
            throw new Error('Failed to add city weather data.');
        }
        // Reload the weather data after adding a city
        getWeatherList();
        document.getElementById('city-input').value = ''; // Clear the input field after adding city
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getWeatherList() {
    try {
        const jwt = localStorage.getItem('jwt');
        const response = await fetch('http://192.168.0.106:8000/weather_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ jwt: jwt })
        });
        if (!response.ok) {
            throw new Error('Failed to fetch weather data.');
        }
        const data = await response.json();

        // Map array of arrays to array of objects
        const mappedData = data.map(row => {
            return {
                id: row[0],
                city: row[1],
                temperature: row[2],
                humidity: row[3]
            };
        });

        const cardSection = document.querySelector('.card-section');
        // Clear existing cards
        cardSection.innerHTML = '';
        // Populate card section with mapped weather data
        mappedData.forEach(city => {
            const card = document.createElement('div');
            card.classList.add('weather-card');
            card.innerHTML = `
                <h2>${city.city}</h2>
                <p>Temperature: ${city.temperature}°C</p>
                <p>Humidity: ${city.humidity}%</p>
                <button class="delete-btn" onclick="deleteCity('${city.city}')">Delete</button>
            `;
            cardSection.appendChild(card);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to delete city and its weather data
async function deleteCity(city) {
    try {
        const jwt = localStorage.getItem('jwt');
        const response = await fetch('http://192.168.0.106:8000/delete_city_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ jwt: jwt, city: city })
        });
        if (!response.ok) {
            throw new Error('Failed to delete city weather data.');
        }
        // Reload the weather data after deleting a city
        getWeatherList();
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call getProfile function when the window loads
window.onload = function() {
    getProfile();
    getWeatherList(); // Load weather data initially
};

function logout() {
    localStorage.removeItem('jwt'); // Clear JWT from local storage
    window.location.href = 'index.html'; // Redirect to index.html page
}