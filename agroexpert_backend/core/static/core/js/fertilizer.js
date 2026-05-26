// // const form = document.getElementById("fertForm");
// // const resultBox = document.getElementById("resultBox");
// // const fertName = document.getElementById("fertName");
// // const historyTable = document.querySelector("#historyTable tbody");

// // let fertCounts = {};
// // let chart;

// // const ctx = document.getElementById("trendChart").getContext("2d");

// // chart = new Chart(ctx,{
// // type:"bar",
// // data:{labels:[],datasets:[{data:[],backgroundColor:["#16a34a","#2563eb","#f59e0b","#9333ea"]}]},
// // options:{plugins:{legend:{display:false}}}
// // });

// // function showResult(msg,error=false){
// // resultBox.style.display="block";
// // resultBox.innerText=msg;
// // resultBox.style.background=error?"#fee2e2":"#dcfce7";
// // resultBox.style.color=error?"#991b1b":"#166534";
// // }

// // function valid(id,min,max,name){
// // let v=parseFloat(document.getElementById(id).value);
// // if(v<min||v>max){
// // showResult(`${name} must be between ${min} and ${max}`,true);
// // return false;
// // }
// // return true;
// // }

// // form.addEventListener("submit",(e)=>{
// // e.preventDefault();

// // if(
// // !valid("temp",0,38,"Temperature")||
// // !valid("humidity",50,95,"Humidity")||
// // !valid("moisture",25,65,"Moisture")||
// // !valid("n",0,126,"Nitrogen")||
// // !valid("p",0,54,"Phosphorus")||
// // !valid("k",0,59,"Potassium")
// // )return;

// // let soil=document.getElementById("soil").value;
// // let crop=document.getElementById("crop").value;

// // if(!soil||!crop){
// // showResult("Select soil and crop type",true);
// // return;
// // }

// // showResult("Analyzing soil nutrients...");

// // let n=+document.getElementById("n").value;
// // let p=+document.getElementById("p").value;
// // let k=+document.getElementById("k").value;

// // let fertilizer="Balanced NPK";

// // // prediction logic
// // if(n<30) fertilizer="Urea";
// // else if(p<20) fertilizer="DAP";
// // else if(k<20) fertilizer="MOP";
// // else if(moisture<30) fertilizer="Organic Compost";
// // else if(soil==="Clayey") fertilizer="Gypsum";
// // else if(crop==="Rice") fertilizer="Ammonium Sulfate";

// // fertName.innerText=fertilizer;

// // // table row
// // let row=`
// // <tr>
// // <td>${new Date().toLocaleString()}</td>
// // <td>${fertilizer}</td>
// // <td>${n}</td>
// // <td>${p}</td>
// // <td>${k}</td>
// // </tr>`;
// // historyTable.innerHTML=row+historyTable.innerHTML;

// // // chart update
// // fertCounts[fertilizer]=(fertCounts[fertilizer]||0)+1;
// // chart.data.labels=Object.keys(fertCounts);
// // chart.data.datasets[0].data=Object.values(fertCounts);
// // chart.update();

// // showResult("Recommendation complete!");
// // });

// // fertilizer.js

// const form = document.getElementById("fertForm");
// const resultBox = document.getElementById("resultBox");
// const fertName = document.getElementById("fertName");
// const historyTable = document.querySelector("#historyTable tbody");

// let fertCounts = {};
// let chart;

// // ===============================
// // Chart
// // ===============================
// const ctx = document.getElementById("trendChart").getContext("2d");

// chart = new Chart(ctx, {
//     type: "bar",
//     data: {
//         labels: [],
//         datasets: [{
//             data: [],
//             backgroundColor: [
//                 "#16a34a",
//                 "#2563eb",
//                 "#f59e0b",
//                 "#9333ea",
//                 "#ef4444",
//                 "#14b8a6",
//                 "#f97316"
//             ],
//             borderRadius: 8
//         }]
//     },
//     options: {
//         responsive: true,
//         plugins: {
//             legend: {
//                 display: false
//             }
//         },
//         scales: {
//             y: {
//                 beginAtZero: true
//             }
//         }
//     }
// });

// // ===============================
// // Result Box
// // ===============================
// function showResult(msg, error = false) {
//     resultBox.style.display = "block";
//     resultBox.innerText = msg;
//     resultBox.style.background = error ? "#fee2e2" : "#dcfce7";
//     resultBox.style.color = error ? "#991b1b" : "#166534";
// }

// // ===============================
// // Validation
// // ===============================
// function valid(id, min, max, name) {
//     let value = parseFloat(document.getElementById(id).value);

//     if (isNaN(value)) {
//         showResult(`${name} is required`, true);
//         return false;
//     }

//     if (value < min || value > max) {
//         showResult(`${name} must be between ${min} and ${max}`, true);
//         return false;
//     }

//     return true;
// }

// // ===============================
// // CSRF Token
// // ===============================
// function getCookie(name) {
//     let cookieValue = null;

//     if (document.cookie && document.cookie !== "") {
//         const cookies = document.cookie.split(";");

//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();

//             if (cookie.substring(0, name.length + 1) === (name + "=")) {
//                 cookieValue = decodeURIComponent(
//                     cookie.substring(name.length + 1)
//                 );
//                 break;
//             }
//         }
//     }

//     return cookieValue;
// }

// // ===============================
// // Submit Form
// // ===============================
// form.addEventListener("submit", async function (e) {
//     e.preventDefault();

//     // validation
//     if (
//         !valid("temp", 0, 60, "Temperature") ||
//         !valid("humidity", 0, 100, "Humidity") ||
//         !valid("moisture", 0, 100, "Moisture") ||
//         !valid("n", 0, 200, "Nitrogen") ||
//         !valid("p", 0, 200, "Phosphorous") ||
//         !valid("k", 0, 200, "Potassium")
//     ) return;

//     let soil = document.getElementById("soil").value;
//     let crop = document.getElementById("crop").value;

//     if (!soil || !crop) {
//         showResult("Please select Soil Type and Crop Type", true);
//         return;
//     }

//     showResult("Analyzing data and predicting fertilizer...");

//     const payload = {
//         temperature: document.getElementById("temp").value,
//         humidity: document.getElementById("humidity").value,
//         moisture: document.getElementById("moisture").value,
//         soil: soil,
//         crop: crop,
//         nitrogen: document.getElementById("n").value,
//         phosphorous: document.getElementById("p").value,
//         potassium: document.getElementById("k").value
//     };

//     try {
//         const response = await fetch("/fertilizer-predict/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "X-CSRFToken": getCookie("csrftoken")
//             },
//             body: JSON.stringify(payload)
//         });

//         const data = await response.json();

//         if (data.success) {

//             const fertilizer = data.fertilizer;

//             // Main Result
//             fertName.innerText = fertilizer;
//             showResult("Recommendation complete!");

//             // Add History Row
//             const row = `
//                 <tr>
//                     <td>${new Date().toLocaleString()}</td>
//                     <td>${fertilizer}</td>
//                     <td>${payload.nitrogen}</td>
//                     <td>${payload.phosphorous}</td>
//                     <td>${payload.potassium}</td>
//                 </tr>
//             `;

//             historyTable.innerHTML = row + historyTable.innerHTML;

//             // Update Chart
//             fertCounts[fertilizer] = (fertCounts[fertilizer] || 0) + 1;

//             chart.data.labels = Object.keys(fertCounts);
//             chart.data.datasets[0].data = Object.values(fertCounts);
//             chart.update();

//         } else {
//             showResult(data.error || "Prediction failed", true);
//         }

//     } catch (error) {
//         showResult("Server error. Please try again.", true);
//         console.error(error);
//     }

// });



// fertilizer.js
// Only UI enhancements + chart.
// Prediction is handled by Django backend form POST.

// document.addEventListener("DOMContentLoaded", function () {

//     const form = document.getElementById("fertForm");
//     const btn = document.querySelector(".predict-btn");
//     const resultBox = document.getElementById("resultBox");

//     // ===============================
//     // Submit Loading State
//     // ===============================
//     if (form) {
//         form.addEventListener("submit", function () {
//             btn.innerHTML = "⏳ Predicting...";
//             btn.disabled = true;
//         });
//     }

//     // ===============================
//     // Auto Hide Result Box
//     // ===============================
//     if (resultBox) {
//         setTimeout(() => {
//             resultBox.style.transition = "0.5s";
//             resultBox.style.opacity = "0";
//         }, 4000);
//     }

//     // ===============================
//     // Chart Data from History Table
//     // ===============================
//     const ctx = document.getElementById("trendChart");

//     if (ctx) {

//         let counts = {};

//         const rows = document.querySelectorAll("#historyTable tbody tr");

//         rows.forEach(row => {
//             const fert = row.cells[1].innerText.trim();

//             if (fert) {
//                 counts[fert] = (counts[fert] || 0) + 1;
//             }
//         });

//         const labels = Object.keys(counts);
//         const values = Object.values(counts);

//         new Chart(ctx, {
//             type: "bar",
//             data: {
//                 labels: labels,
//                 datasets: [{
//                     label: "Recommendations",
//                     data: values,
//                     backgroundColor: [
//                         "#16a34a",
//                         "#2563eb",
//                         "#f59e0b",
//                         "#9333ea",
//                         "#ef4444",
//                         "#14b8a6",
//                         "#f97316"
//                     ],
//                     borderRadius: 8
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 plugins: {
//                     legend: {
//                         display: false
//                     }
//                 },
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

// });



// fertilizer.js
// Django version: backend handles prediction + DB save
// JS only handles chart + UI effects

document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Result message auto hide
    // ===============================
    const resultBox = document.querySelector(".result-box");

    if (resultBox) {
        setTimeout(() => {
            resultBox.style.transition = "0.4s";
            resultBox.style.opacity = "0";

            setTimeout(() => {
                resultBox.style.display = "none";
            }, 400);
        }, 3500);
    }

    // ===============================
    // Submit button loading state
    // ===============================
    const form = document.querySelector("form");
    const btn = document.querySelector(".predict-btn");

    if (form && btn) {
        form.addEventListener("submit", function () {
            btn.innerHTML = "⏳ Predicting...";
            btn.disabled = true;
        });
    }

    // ===============================
    // Build Chart from history table
    // ===============================
    const chartCanvas = document.getElementById("trendChart");

    if (chartCanvas) {

        const rows = document.querySelectorAll(".recent-card tbody tr");

        let counts = {};

        rows.forEach(row => {

            const cells = row.querySelectorAll("td");

            if (cells.length >= 2) {

                const fertilizer = cells[1].innerText.trim();

                if (
                    fertilizer &&
                    fertilizer !== "No history yet"
                ) {
                    counts[fertilizer] =
                        (counts[fertilizer] || 0) + 1;
                }
            }
        });

        const labels = Object.keys(counts);
        const values = Object.values(counts);

        new Chart(chartCanvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Recommendations",
                    data: values,
                    backgroundColor: [
                        "#16a34a",
                        "#2563eb",
                        "#f59e0b",
                        "#9333ea",
                        "#ef4444",
                        "#14b8a6",
                        "#f97316"
                    ],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

});