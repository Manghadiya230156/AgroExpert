// Soil Test JS - Django Version

document.addEventListener("DOMContentLoaded", function () {

    const labCards = document.querySelectorAll(".lab-card");
    const submitBtn = document.getElementById("submitBtn");
    const labInput = document.getElementById("labInput");
    const form = document.getElementById("soilForm");

    let selectedLab = null;

    // ==========================
    // Select Lab Card
    // ==========================
    labCards.forEach(card => {

        card.addEventListener("click", function () {

            labCards.forEach(c => c.classList.remove("selected"));

            this.classList.add("selected");

            selectedLab = this.getAttribute("data-lab");

            labInput.value = selectedLab;

            submitBtn.disabled = false;
            submitBtn.classList.add("active");
            submitBtn.innerHTML = "📩 Submit Soil Test Request";
        });

    });

    // ==========================
    // Submit Validation
    // ==========================
    form.addEventListener("submit", function (e) {

        if (!selectedLab) {
            e.preventDefault();
            alert("Please select a laboratory first.");
            return;
        }

        submitBtn.innerHTML = "⏳ Submitting...";
        submitBtn.disabled = true;
    });

    // ==========================
    // Auto Hide Success Message
    // ==========================
    const successBox = document.querySelector(".success-box");

    if (successBox) {
        setTimeout(() => {
            successBox.style.transition = "0.5s";
            successBox.style.opacity = "0";

            setTimeout(() => {
                successBox.style.display = "none";
            }, 500);

        }, 3000);
    }

});