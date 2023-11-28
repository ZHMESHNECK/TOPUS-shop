

// csrf_token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Зберігання персональних даних
const formElement = document.getElementById('personal_data');
formElement.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(formElement);

    let url = '/api/profile/' + formData.get('username').textContent + '/'
    let data = {
        username: formData.get('username'),
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        surname: formData.get('surname'),
        email: formData.get('email'),
        city: formData.get('city'),
        adress: formData.get('adress'),
        phone_number_0: formData.get('phone_number_0'),
        phone_number_1: formData.get('phone_number_1'),
        department: formData.get('department'),
    }
    fetch(url, {
        'method': 'POST',
        'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        'body': JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data => {
            window.location.href = '/api/profile/' + data.username + '/'
        })
        .catch(error => {
            console.log(error)
        })
});

// Для поля телефону
var backspacePressedLast = false;

document.addEventListener('keydown', function (e) {
    var target = e.target;
    if (target && target.id == 'id_phone_number_1') {
        var currentKey = e.which;

        if (currentKey === 8 || currentKey === 46) {
            backspacePressedLast = true;
        } else {
            backspacePressedLast = false;
        }
    }
});

document.addEventListener('input', function (e) {
    var target = e.target;

    if (target && target.id == 'id_phone_number_1') {
        if (backspacePressedLast) return;

        var currentValue = target.value,
            newValue = currentValue.replace(/\D+/g, ''),
            formattedValue = formatToTelephone(newValue);

        target.value = formattedValue;
    }
});

function formatToTelephone(str) {
    var splitString = str.split(''),
        returnValue = '';

    for (var i = 0; i < splitString.length; i++) {
        var currentLoop = i,
            currentCharacter = splitString[i];

        switch (currentLoop) {
            case 0:
                returnValue = returnValue.concat('(');
                returnValue = returnValue.concat(currentCharacter);
                break;
            case 2:
                returnValue = returnValue.concat(currentCharacter);
                returnValue = returnValue.concat(') ');
                break;
            case 5:
                returnValue = returnValue.concat(currentCharacter);
                returnValue = returnValue.concat('-');
                break;
            default:
                returnValue = returnValue.concat(currentCharacter);
        }
    }

    return returnValue;
}

// help-text
var help_btn = document.getElementsByClassName('help-text-i')[0]
var help_text = document.getElementById('help-text')
help_btn.addEventListener('click', (e) => {

    if (help_text.style.display == 'none') {
        help_text.style.display = 'block'
    } else {
        help_text.style.display = 'none'
    };
})
