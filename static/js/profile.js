

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
    // !!!!
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