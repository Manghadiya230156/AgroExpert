
const form = document.querySelector(".contact-form");

form.addEventListener("submit", function(e){

    const name = form.querySelector("[name='name']").value.trim();
    const email = form.querySelector("[name='email']").value.trim();
    const subject = form.querySelector("[name='subject']").value.trim();
    const message = form.querySelector("[name='message']").value.trim();

    if(name.length < 3){
        alert("Name must be at least 3 characters.");
        e.preventDefault();
        return;
    }

    if(!email.includes("@") || !email.includes(".")){
        alert("Enter a valid email.");
        e.preventDefault();
        return;
    }

    if(subject.length < 5){
        alert("Subject too short.");
        e.preventDefault();
        return;
    }

    if(message.length < 10){
        alert("Message must be at least 10 characters.");
        e.preventDefault();
        return;
    }
});

