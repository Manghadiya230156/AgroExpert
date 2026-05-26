// ELEMENTS
const form = document.getElementById("cropForm");
const resultBox = document.getElementById("resultBox");

// OPTIONAL: chart (safe init)


let chart = null;
const ctx = document.getElementById("trendChart");

if (ctx) {
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: chartLabels,
            datasets: [{
                data: chartData,
                backgroundColor: ["#16a34a", "#2563eb", "#f59e0b", "#9333ea"]
            }]
        },
        options: {
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// SHOW MESSAGE
function showResult(msg, error = false) {
    if (!resultBox) return;

    resultBox.style.display = "block";
    resultBox.innerText = msg;

    resultBox.classList.remove("result-success", "result-error");
    resultBox.classList.add(error ? "result-error" : "result-success");
}

// VALIDATION
function valid(id, min, max, name) {
    const el = document.getElementById(id);
    if (!el) return true;

    const v = parseFloat(el.value);

    if (isNaN(v) || v < min || v > max) {
        showResult(`${name} must be between ${min} and ${max}`, true);
        return false;
    }

    return true;
}

// FORM SUBMIT
if (form) {
    form.addEventListener("submit", function (event) {

        let isValid =
            valid("n", 0, 140, "Nitrogen") &&
            valid("p", 5, 145, "Phosphorus") &&
            valid("k", 5, 205, "Potassium") &&
            valid("temp", 9, 50, "Temperature") &&
            valid("humidity", 14, 100, "Humidity") &&
            valid("ph", 3.5, 10, "pH") &&
            valid("rain", 20, 300, "Rainfall");

        if (!isValid) {
            event.preventDefault(); // stop only if invalid
        } else {
            showResult("Submitting data...");
        }
    });
}