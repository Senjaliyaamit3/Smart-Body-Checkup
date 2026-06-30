// =========================================
// Smart Body Checkup System
// script.js
// =========================================

document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Disease Buttons
    // ===============================

    const diabetesBtn = document.getElementById("diabetesBtn");
    const heartBtn = document.getElementById("heartBtn");
    const kidneyBtn = document.getElementById("kidneyBtn");

    // ===============================
    // Disease Forms
    // ===============================

    const diabetesForm = document.getElementById("diabetesForm");
    const heartForm = document.getElementById("heartForm");
    const kidneyForm = document.getElementById("kidneyForm");

    // ===============================
    // Hide All Forms
    // ===============================

    function hideAllForms() {

        if (diabetesForm)
            diabetesForm.style.display = "none";

        if (heartForm)
            heartForm.style.display = "none";

        if (kidneyForm)
            kidneyForm.style.display = "none";
    }

    // ===============================
    // Remove Active Button
    // ===============================

    function removeActiveButtons() {

        if (diabetesBtn)
            diabetesBtn.classList.remove("active");

        if (heartBtn)
            heartBtn.classList.remove("active");

        if (kidneyBtn)
            kidneyBtn.classList.remove("active");
    }

    // ===============================
    // Show Form
    // ===============================

    function showForm(form, button) {

        hideAllForms();

        removeActiveButtons();

        if (form)
            form.style.display = "block";

        if (button)
            button.classList.add("active");

        if (form) {

            form.scrollIntoView({

                behavior: "smooth",

                block: "start"

            });

        }

    }

    // ===============================
    // Button Events
    // ===============================

    if (diabetesBtn) {

        diabetesBtn.addEventListener("click", function () {

            showForm(diabetesForm, diabetesBtn);

        });

    }

    if (heartBtn) {

        heartBtn.addEventListener("click", function () {

            showForm(heartForm, heartBtn);

        });

    }

    if (kidneyBtn) {

        kidneyBtn.addEventListener("click", function () {

            showForm(kidneyForm, kidneyBtn);

        });

    }

    // ===============================
    // Default Form
    // ===============================

    if (diabetesForm) {

        showForm(diabetesForm, diabetesBtn);

    }

});

// =========================================
// Loading Button
// =========================================

document.querySelectorAll("form").forEach(function(form){

    form.addEventListener("submit", function(){

        const btn = form.querySelector("button[type='submit']");

        if(btn){

            btn.innerHTML = "Predicting...";

            btn.disabled = true;

        }

    });

});

// =========================================
// Prevent Negative Numbers
// =========================================

document.querySelectorAll("input[type='number']").forEach(function(input){

    input.addEventListener("input", function(){

        if(this.value < 0){

            this.value = "";

        }

    });

});

// =========================================
// Navbar Shadow
// =========================================

window.addEventListener("scroll", function(){

    const navbar = document.querySelector(".navbar");

    if(!navbar)
        return;

    if(window.scrollY > 40){

        navbar.classList.add("shadow");

    }

    else{

        navbar.classList.remove("shadow");

    }

});

// =========================================
// Scroll To Top Button
// =========================================

const topBtn = document.createElement("button");

topBtn.innerHTML = "↑";

topBtn.id = "topBtn";

document.body.appendChild(topBtn);

topBtn.style.position = "fixed";
topBtn.style.bottom = "20px";
topBtn.style.right = "20px";
topBtn.style.width = "50px";
topBtn.style.height = "50px";
topBtn.style.borderRadius = "50%";
topBtn.style.border = "none";
topBtn.style.background = "#0d6efd";
topBtn.style.color = "#fff";
topBtn.style.fontSize = "20px";
topBtn.style.cursor = "pointer";
topBtn.style.display = "none";
topBtn.style.zIndex = "9999";

window.addEventListener("scroll", function(){

    if(window.scrollY > 300){

        topBtn.style.display = "block";

    }

    else{

        topBtn.style.display = "none";

    }

});

topBtn.addEventListener("click", function(){

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

});

// =========================================
// Fade Animation
// =========================================

const observer = new IntersectionObserver(function(entries){

    entries.forEach(function(entry){

        if(entry.isIntersecting){

            entry.target.classList.add("fade-in");

        }

    });

},{

    threshold:0.2

});

document.querySelectorAll(".card,.disease-card,.form-card,.stat-card,.recommendation-card").forEach(function(el){

    observer.observe(el);

});

// =========================================
// Smooth Anchor Scroll
// =========================================

document.querySelectorAll("a[href^='#']").forEach(function(anchor){

    anchor.addEventListener("click", function(e){

        const target = document.querySelector(this.getAttribute("href"));

        if(target){

            e.preventDefault();

            target.scrollIntoView({

                behavior:"smooth"

            });

        }

    });

});

// =========================================
// Console Message
// =========================================

console.log("Smart Body Checkup System Loaded Successfully");