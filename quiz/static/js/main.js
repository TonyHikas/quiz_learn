document.addEventListener("DOMContentLoaded", function(event) {
    let welcome_section = document.getElementById("welcome");
    let auth_1_section = document.getElementById("auth-step-1");
    let auth_2_section = document.getElementById("auth-step-2");
    let question_section = document.getElementById("question");
    document.getElementById("auth-1-next").onclick = function (e) {
        e.preventDefault()
        hide(auth_1_section);
        show(auth_2_section);
    };
});

function hide(element){
    element.style.display = 'none'
}
function show(element){
    element.style.display = 'block'
}
