let current_question = 0
let last_question = 0
let questions = []
let user_answers = {}
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
        const saved = save_answer()
        if (!saved){
            alert('Вы не выбрали ответ')
            return
        }
        if (current_question === last_question){
            hide(question_section);
            // todo load result
            send_answers()
            show(result_section);
        } else{
            current_question += 1
            show_question(current_question)
        }
    };
    document.getElementById("previous-question").onclick = function (e) {
        save_answer()
        if (current_question === 0){
            if (confirm('Выйти из теста? Прогресс будет сброшен')){
                hide(question_section);
                show(start_section);
            }
        } else{
            current_question -= 1
            show_question(current_question)
        }
    };
    document.getElementById("result-select-category").onclick = function (e) {
        e.preventDefault()
        hide(result_section);
        user_answers = {}
        show(start_section);
    };
    document.getElementById("result-retry").onclick = function (e) {
        e.preventDefault()
        hide(result_section);
        user_answers = {}
        load_questions();
        current_question = 0
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

    let question_id = document.getElementById('question-id')
    let title = document.getElementById('question-title')
    let images = document.getElementById('question-images')
    let answers = document.getElementById('question-answers')
    question_id.value = question.id
    title.innerHTML = question.text
    images.innerHTML = ''
    answers.innerHTML = ''
    question.images.forEach((img_src)=>{
        let image = document.createElement('img');
        image.src = img_src
        image.className = 'question-image'
        images.append(image)
    })
    question.answers.forEach((answer)=>{
        let label = document.createElement('label');
        label.className = 'answer-label'
        let input = document.createElement('input');
        input.name = 'answer'
        input.type = 'radio'
        input.value = answer.id
        input.className = 'answer-radio'
        if (user_answers[question_number+1] === answer.id){
            input.checked = true
        }else{
            input.checked = false
        }
        label.append(input)
        label.append(answer.text)
        answers.append(label)
    })
}
function check_auth(){
    let token = localStorage.getItem('token')
    return token != null && token !== ''
}
function save_answer(){
    let question_id = document.getElementById('question-id')
    const checked_input = document.querySelector('.answer-radio:checked');
    if (checked_input === null){
        return false
    }
    user_answers[question_id.value] = Number(checked_input.value)
    return true
}
function send_answers(){
    let data = []
    Object.keys(user_answers).forEach(key=>{
        data.push({
            question_id: key,
            answer_id: user_answers[key]
        })
    })
    let response = $.ajax({
        type: "POST",
        url: "/api/quiz/check_answers/",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        headers: { 'Authorization': 'Token '+ localStorage.getItem('token')},
        async: false
    });
    let result = response.responseJSON
    let total_right= document.getElementById('total-right')
    total_right.innerText = 'Правильных ответов: '+ result.right + ' из ' + result.total

    let questions_result = document.getElementById('questions-result')
    questions_result.innerHTML = ''
    // show questions with result
    let i = 0
    questions.forEach((question)=>{
        let check_result = result.check_result[i]
        let title = document.createElement('div')
        title.className = 'question-title'
        let images = document.createElement('div')
        images.className = 'question-images'
        let answers = document.createElement('div')
        answers.className = 'question-answers'
        title.innerHTML = question.text
        images.innerHTML = ''
        answers.innerHTML = ''
        question.images.forEach((img_src)=>{
            let image = document.createElement('img');
            image.src = img_src
            image.className = 'question-image'
            images.append(image)
        })
        question.answers.forEach((answer)=>{
            let label = document.createElement('label');
            label.className = 'answer-label'
            let input = document.createElement('input');
            input.name = 'answer'
            input.type = 'radio'
            input.disabled = true
            input.value = answer.id
            input.className = 'answer-radio'
            if (user_answers[i+1] === answer.id){
                input.checked = true
            }
            if (answer.id === check_result.right_answer_id){
                label.style.backgroundColor = 'green'
            }
            if (!check_result.is_right && answer.id === check_result.user_answer_id){
                label.style.backgroundColor = 'red'
            }
            label.append(input)
            label.append(answer.text)
            answers.append(label)
        })
        questions_result.append(title)
        questions_result.append(images)
        questions_result.append(answers)
        questions_result.append(document.createElement('hr'))
        i++
    })
}