// yield.js

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("yieldForm");
    const btn = document.querySelector(".predict-btn");

    // ==========================
    // Profile Menu
    // ==========================

    const profileBtn = document.getElementById("profileBtn");
    const profileMenu = document.getElementById("profileMenu");

    if (profileBtn && profileMenu) {

        profileBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            profileMenu.classList.toggle("show");
        });

        document.addEventListener("click", function () {
            profileMenu.classList.remove("show");
        });

        profileMenu.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }


    // ==========================
    // Submit Loading State
    // ==========================

    if (form && btn) {

        form.addEventListener("submit", function () {

            btn.innerHTML = "⏳ Predicting...";
            btn.disabled = true;

        });

    }


    // ==========================
    // Result Card Animation
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

        setTimeout(() => {

            resultCard.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

        }, 250);

    }


    // ==========================
    // Current Year
    // ==========================

    const yearInput =
        document.querySelector('input[name="crop_year"]');

    if (yearInput && yearInput.value === "") {

        yearInput.value = new Date().getFullYear();

    }


    // ==========================
    // Validation
    // ==========================

    if (form) {

        form.addEventListener("submit", function (e) {

            const area =
                parseFloat(
                    document.querySelector(
                        'input[name="area"]'
                    ).value
                );

            const rain =
                parseFloat(
                    document.querySelector(
                        'input[name="annual_rainfall"]'
                    ).value
                );

            const fert =
                parseFloat(
                    document.querySelector(
                        'input[name="fertilizer"]'
                    ).value
                );

            const pest =
                parseFloat(
                    document.querySelector(
                        'input[name="pesticide"]'
                    ).value
                );


            if (area <= 0) {

                alert("Area must be greater than 0");

                e.preventDefault();

                btn.innerHTML = "📈 Predict Yield";
                btn.disabled = false;

                return;
            }


            if (rain < 0 || fert < 0 || pest < 0) {

                alert("Negative values are not allowed");

                e.preventDefault();

                btn.innerHTML = "📈 Predict Yield";
                btn.disabled = false;

                return;
            }

        });

    }

});