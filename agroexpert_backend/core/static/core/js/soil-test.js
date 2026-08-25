document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Soil Test Elements
    // ==========================

    const labCards = document.querySelectorAll(".lab-card");
    const submitBtn = document.getElementById("submitBtn");
    const labInput = document.getElementById("labInput");
    const form = document.getElementById("soilForm");

    let selectedLab = null;


    // ==========================
    // Select Laboratory
    // ==========================

    labCards.forEach(card => {

        card.addEventListener("click", function () {

            labCards.forEach(c => {
                c.classList.remove("selected");
            });

            this.classList.add("selected");

            selectedLab = this.getAttribute("data-lab");

            if (labInput) {
                labInput.value = selectedLab;
            }

            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.add("active");
                submitBtn.innerHTML = "📩 Submit Soil Test Request";
            }

        });

    });


    // ==========================
    // Form Submit
    // ==========================

    if (form) {

        form.addEventListener("submit", function (e) {

            if (!selectedLab) {

                e.preventDefault();

                alert("Please select a laboratory first.");

                return;
            }

            if (submitBtn) {
                submitBtn.innerHTML = "⏳ Submitting...";
                submitBtn.disabled = true;
            }

        });

    }


    // ==========================
    // Success Message
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


    // ==========================
    // Mobile Profile Menu
    // ==========================

    const profileBtn = document.getElementById("profileBtn");
    const profileMenu = document.getElementById("profileMenu");

    console.log("Profile button:", profileBtn);
    console.log("Profile menu:", profileMenu);


    if (profileBtn && profileMenu) {

        profileBtn.addEventListener("click", function (e) {

            e.preventDefault();
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

});