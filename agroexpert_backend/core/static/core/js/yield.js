// yield.js
// Django version - backend handles ML prediction

document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Submit button loading state
    // ==========================
    const form = document.getElementById("yieldForm");
    const btn = document.querySelector(".predict-btn");

    if (form && btn) {
        form.addEventListener("submit", function () {
            btn.innerHTML = "⏳ Predicting...";
            btn.disabled = true;
        });
    }

    // ==========================
    // Animate result card if shown
    // ==========================
    const resultCard = document.querySelector(".result-card");

    if (resultCard) {
        resultCard.style.opacity = "0";
        resultCard.style.transform = "translateY(15px)";

        setTimeout(() => {
            resultCard.style.transition = "0.45s ease";
            resultCard.style.opacity = "1";
            resultCard.style.transform = "translateY(0)";
        }, 120);

        // auto scroll to result
        setTimeout(() => {
            resultCard.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }, 250);
    }

    // ==========================
    // Auto set current year if empty
    // ==========================
    const yearInput = document.querySelector('input[name="crop_year"]');

    if (yearInput && yearInput.value === "") {
        yearInput.value = new Date().getFullYear();
    }

    // ==========================
    // Basic client validation
    // ==========================
    if (form) {
        form.addEventListener("submit", function (e) {

            const area = parseFloat(document.querySelector('input[name="area"]').value);
            const rain = parseFloat(document.querySelector('input[name="annual_rainfall"]').value);
            const fert = parseFloat(document.querySelector('input[name="fertilizer"]').value);
            const pest = parseFloat(document.querySelector('input[name="pesticide"]').value);

            if (area <= 0) {
                alert("Area must be greater than 0");
                e.preventDefault();
                btn.innerHTML = "Predict Yield";
                btn.disabled = false;
                return;
            }

            if (rain < 0 || fert < 0 || pest < 0) {
                alert("Negative values are not allowed");
                e.preventDefault();
                btn.innerHTML = "Predict Yield";
                btn.disabled = false;
                return;
            }
        });
    }

});