// AgroExpert Weather JS
const apiKey = "7823f22773b516f7d45a291b745d30a2";

// ==============================
// Auto Load by GPS
// ==============================
window.addEventListener("DOMContentLoaded", () => {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(

            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;

                getWeatherByCoords(lat, lon);
            },

            () => {
                document.getElementById("locationName").innerText =
                    "Location blocked. Enter city manually.";
            }

        );

    } else {

        document.getElementById("locationName").innerText =
            "Geolocation not supported.";

    }

});

// ==============================
// Manual Search
// ==============================
function manualSearch() {

    const city = document.getElementById("cityInput").value.trim();

    if (!city) {
        alert("Enter city name");
        return;
    }

    fetchWeather(`q=${city}`);
}

// ==============================
// GPS Search
// ==============================
function getWeatherByCoords(lat, lon) {
    fetchWeather(`lat=${lat}&lon=${lon}`);
}

// ==============================
// Fetch Weather API
// ==============================
async function fetchWeather(query) {

    const container = document.getElementById("forecastContainer");

    container.innerHTML = `
        <div class="card">
            <h3>Loading forecast...</h3>
        </div>
    `;

    try {

        const response = await fetch(
            `https://api.openweathermap.org/data/2.5/forecast?${query}&units=metric&appid=${apiKey}`
        );

        const data = await response.json();

        if (data.cod !== "200") {

            container.innerHTML = `
                <div class="card">
                    <p style="color:red;">${data.message}</p>
                </div>
            `;
            return;
        }

        renderForecast(data);

    } catch (error) {

        container.innerHTML = `
            <div class="card">
                <p style="color:red;">Unable to fetch weather data.</p>
            </div>
        `;
    }
}

// ==============================
// Render Forecast
// ==============================
function renderForecast(data) {

    document.getElementById("locationName").innerText =
        `📍 ${data.city.name}, ${data.city.country}`;

    const container = document.getElementById("forecastContainer");
    container.innerHTML = "";

    const grouped = {};

    data.list.forEach(item => {

        const date = item.dt_txt.split(" ")[0];

        if (!grouped[date]) grouped[date] = [];

        grouped[date].push(item);

    });

    Object.keys(grouped).slice(0, 5).forEach(date => {

        const dayCard = document.createElement("div");
        dayCard.className = "day-card";

        const title = document.createElement("div");
        title.className = "day-title";
        title.innerText = new Date(date).toDateString();

        const grid = document.createElement("div");
        grid.className = "time-grid";

        grouped[date].forEach(item => {

            const time = item.dt_txt.split(" ")[1].slice(0, 5);

            const condition =
                item.weather[0].main.toLowerCase();

            let icon = "☀️";

            if (condition.includes("cloud")) icon = "☁️";
            if (condition.includes("rain")) icon = "🌧️";
            if (condition.includes("storm")) icon = "⛈️";
            if (condition.includes("snow")) icon = "❄️";
            if (condition.includes("mist")) icon = "🌫️";

            const card = document.createElement("div");
            card.className = "time-card";

            card.innerHTML = `
                <div class="time">${time}</div>
                <div class="weather-symbol">${icon}</div>
                <div class="temp">${item.main.temp}°C</div>
                <div class="desc">${item.weather[0].description}</div>

                <div class="details">
                    <div>💧 Humidity: ${item.main.humidity}%</div>
                    <div>💨 Wind: ${item.wind.speed} m/s</div>
                    <div>🌡 Feels: ${item.main.feels_like}°C</div>
                </div>
            `;

            grid.appendChild(card);

        });

        dayCard.appendChild(title);
        dayCard.appendChild(grid);

        container.appendChild(dayCard);

    });
}   