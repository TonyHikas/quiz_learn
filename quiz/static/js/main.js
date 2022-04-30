let current_question = 0
let last_question = 0
let questions = []
let answers_result = {}
let answers_check = {}
let category_id = null
let email = null
let verify_code = null

document.addEventListener("DOMContentLoaded", function(event) {
    $('#category-select').select2({
        ajax: {
            url: '/api/quiz/category_autocomplete/',
            dataType: 'json',
        },
        width: '400px',
    });

    let welcome_section = document.getElementById("welcome");
    let auth_1_section = document.getElementById("auth-step-1");
    let auth_2_section = document.getElementById("auth-step-2");
    let question_section = document.getElementById("question");
    let result_section = document.getElementById("result");
    let start_section = document.getElementById("start");
    document.getElementById("welcome-next").onclick = function (e) {
        e.preventDefault()
        hide(welcome_section);
        if (check_auth()){
            show(start_section);
        }else{
            show(auth_1_section);
        }
    };
    document.getElementById("auth-1-back").onclick = function (e) {
        e.preventDefault()
        hide(auth_1_section);
        show(welcome_section);
    };
    document.getElementById("auth-1-next").onclick = function (e) {
        e.preventDefault()
        let email_input = document.getElementById('auth-email')
        email = email_input.value
        if(email== null || email=== '') {
            alert('Укажите email')
            return
        }
        const status = send_email(email)
        if (status===429){
            alert('Отправлять код можно только раз в минуту')
            return
        }else if(status===400) {
            alert('Email содержит ошибку')
            return
        }else if (status!==200){
            alert('Неизвестная ошибка')
            return
        }

        hide(auth_1_section);
        show(auth_2_section);
    };
    document.getElementById("auth-2-back").onclick = function (e) {
        e.preventDefault()
        hide(auth_2_section);
        show(auth_1_section);
    };
    document.getElementById("auth-2-next").onclick = function (e) {
        let code_input = document.getElementById('auth-code')
        verify_code = code_input.value
        if(verify_code== null || verify_code=== '') {
            alert('Укажите код из письма')
            return
        }
        const token = send_code(email, verify_code)
        if (token === null){
            return
        }else{
           localStorage.setItem('token', token)
        }
        e.preventDefault()
        hide(auth_2_section);
        show(start_section);
    };
    document.getElementById("start-next").onclick = function (e) {
        e.preventDefault()
        const category_input = document.getElementById('category-select')
        category_id = category_input.value
        if(category_id == null || category_id === ''){
            alert('Нужно выбрать категорию')
            return
        }
        hide(start_section);
        load_questions();
        show_question(0)
        show(question_section);
    };
    document.getElementById("next-question").onclick = function (e) {
        e.preventDefault()
        // todo save answer
        if (current_question === last_question){
            hide(question_section);
            // todo load result
            show(result_section);
        } else{
            current_question += 1
            show_question(current_question)
        }
    };
    document.getElementById("previous-question").onclick = function (e) {
        if (current_question === 0){
            // todo alert what test will be reset
            hide(question_section);
            // todo load result
            show(start_section);
        } else{
            current_question -= 1
            show_question(current_question)
        }
    };
    document.getElementById("result-select-category").onclick = function (e) {
        e.preventDefault()
        hide(result_section);
        show(start_section);
    };
    document.getElementById("result-retry").onclick = function (e) {
        e.preventDefault()
        hide(result_section);
        load_questions();
        show_question(0)
        show(question_section);
    };
});

function hide(element){
    element.style.display = 'none'
}
function show(element){
    element.style.display = 'block'
}
function send_email(user_email){
    let response = $.ajax({
        type: "GET",
        url: "/api/auth/",
        data: {
            email: user_email
        },
        async: false
    });
    return response.status
}
function send_code(user_email, code){
    let response = $.ajax({
        type: "POST",
        url: "/api/auth/",
        data: {
            email: user_email,
            code: code
        },
        async: false
    });

    if(response.status===400) {
        alert('Неверный код')
        return
    }else if (response.status!==200){
        alert('Неизвестная ошибка')
        return
    }
    response_data = response.responseJSON
    return response_data.token
}
function load_questions(){
    let response = $.ajax({
        type: "GET",
        url: "/api/quiz/get_questions/",
        data: {
            category_id: category_id,
            questions_count: 5
        },
        headers: { 'Authorization': 'Token '+ localStorage.getItem('token')},
        async: false
    });
    questions = response.responseJSON
    last_question = questions.length - 1
}
function show_question(question_number){
    let question = null
    try {
        question = questions[question_number]
    }
    catch (e){
        alert('Ошибка при получении вопроса')
        return
    }

    let title = document.getElementById('question-title')
    let images = document.getElementById('question-images')
    title.innerHTML = question.text
    images.innerHTML = ''
    question.images.forEach((img_src)=>{
        let image = document.createElement('img');
        image.src = img_src
        image.className = 'question-image'
        images.append(image)
    })
    // todo pass list of answers
    // todo select checked answer
}
function check_auth(){
    let token = localStorage.getItem('token')
    return token != null && token !== ''
}
