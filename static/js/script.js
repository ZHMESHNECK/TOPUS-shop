
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


// Корегування кількості товару
const buttons = document.querySelectorAll(".input button");
const minValue = 1;
const maxValue = 10;

buttons.forEach((button) => {
    button.addEventListener("click", (event) => {
        // 1. Get the clicked element
        const element = event.currentTarget;
        // 2. Get the parent
        const parent = element.parentNode;
        // 3. Get the number (within the parent)
        const numberContainer = parent.querySelector(".number");
        const number = parseFloat(numberContainer.textContent);
        // 4. Get the minus and plus buttons
        const increment = parent.querySelector(".plus");
        const decrement = parent.querySelector(".minus");
        // 5. Change the number based on click (either plus or minus)
        const newNumber = element.classList.contains("plus")
            ? number + 1
            : number - 1;
        numberContainer.textContent = newNumber;
        // 6. Disable and enable buttons based on number value (and undim number)
        if (newNumber === minValue) {
            decrement.disabled = true;
            numberContainer.classList.add("dim");
            // Make sure the button won't get stuck in active state (Safari)
            element.blur();
        } else if (newNumber > minValue && newNumber < maxValue) {
            decrement.disabled = false;
            increment.disabled = false;
            numberContainer.classList.remove("dim");
        } else if (newNumber === maxValue) {
            increment.disabled = true;
            numberContainer.textContent = `${newNumber}`;
            element.blur();
        }

        // send quantity of product to Back-end
        let url = '/cart/'
        let data = {
            product_id: numberContainer.id,
            quantity: newNumber,
            overide_quantity: true
        }
        // console.log(data)
        fetch(url, {
            'method': 'POST',
            'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            'body': JSON.stringify(data)
        })
            .then(res => res.json())
            .then(data => {
                // console.log(data)
                document.getElementById('full_cart_price').textContent = 'До сплати: ' + data.to_pay.toFixed(2) + ' грн'
                var price = document.getElementById('price_' + numberContainer.id).value
                var correct_price = price.replace(/,/g, '.')
                document.getElementById('span_' + numberContainer.id).textContent = (Number(correct_price) * newNumber).toFixed(2)
                document.getElementById('quantity_' + numberContainer.id).value = data.len
                document.getElementById('num_of_cart').innerHTML = data.len
                document.getElementById('count_in_cart').innerHTML = data.len

            })
            .catch(error => {
                console.log(error)
            })
    });
});


// Перевірка заповнення необхідних полів
const formorder = document.getElementById('order');
formorder.addEventListener('submit', (e) => {
    e.preventDefault();
    let delivery_block = document.getElementsByClassName('delivery-block')[0]
    let deliv_to_cstmr = document.getElementById('del_to_custumer')
    let pay_block = document.getElementsByClassName('pay-block')[0]
    let contact_block = document.getElementById('personal_data')

    let valid = true

    // не обрано спосіб доставки
    if (delivery_block.querySelectorAll('input[type="radio"]:checked').length == 0) {
        document.getElementById('eror_delivery').style.display = 'block'
        document.getElementById('eror_delivery').scrollIntoView()
        valid = false
    } else {
        document.getElementById('eror_delivery').style.display = 'none'
    }

    // не вказан номер відділення поштової служби
    let nova = document.getElementById('self_f_nova')
    if (nova.querySelector('input[type="radio"]:checked')) {

        if (!nova.getElementsByTagName('input')[1].value) {
            document.getElementById('eror_nova_del').style.display = 'block'
            valid = false
        } else {
            document.getElementById('eror_nova_del').style.display = 'none'
        }
    }

    let ukr = document.getElementById('self_f_ukr')
    if (ukr.querySelector('input[type="radio"]:checked')) {

        if (!ukr.getElementsByTagName('input')[1].value) {
            document.getElementById('eror_ukr_del').style.display = 'block'
            valid = false
        } else {
            document.getElementById('eror_ukr_del').style.display = 'none'
        }
    }

    // Кур'ер - не обрано адрес
    if (deliv_to_cstmr.querySelector('input[type="radio"]:checked')) {
        for (let val of document.getElementsByClassName('option2')[0].getElementsByTagName('input')) {
            if (!val.value) {
                document.getElementById('eror_adress_del').style.display = 'block'
                valid = false
                break
            } else {
                document.getElementById('eror_adress_del').style.display = 'none'
            }
        }
    };

    // не обрано спосіб оплати
    if (pay_block.querySelectorAll('input[type="radio"]:checked').length == 0) {
        document.getElementById('eror_pay').style.display = 'block'
        document.getElementById('eror_pay').scrollIntoView()
        valid = false
    } else {
        document.getElementById('eror_pay').style.display = 'none'
    }

    // блок персональних данних
    const formData = new FormData(contact_block);
    for (let value of formData.values()) {
        if (!value) {
            document.getElementById('message_pers').style.display = 'block'
            document.getElementById('message_pers').scrollIntoView()
            valid = false
            break
        } else {
            document.getElementById('message_pers').style.display = 'none'
        }
    }
    // console.log(valid)
    if (valid) {
        let hid_in = document.getElementById('send_data')
        hid_in.value = sendform()
        formorder.submit()
        return valid
    };
    return valid
});

// Показ форм обраних параметрів
let radios = document.querySelectorAll('input[type="radio"]');
function show() {
    for (let radio of radios) {
        var form = document.getElementsByClassName(radio.id)[0];
        if (radio.checked && form) {
            form.style.display = 'block';
        }
        if (!radio.checked && form) {
            form.style.display = 'none';
        }
    }
};


// Зберігання персональних даних
const formElement = document.getElementById('personal_data');
formElement.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(formElement);
    // console.log(formData)

    let url = '/api/profile/' + document.getElementsByClassName('header-shadow__btn')[0].textContent + '/'
    let data = {
        cart: true,
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        surname: formData.get('surname'),
        phone_number_0: formData.get('phone_number_0'),
        phone_number_1: formData.get('phone_number_1'),
        email: formData.get('email'),
    }
    // console.log(data)

    fetch(url, {
        'method': 'POST',
        'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        'body': JSON.stringify(data)
    })
        .then(res => { res.json(), location.reload(true) })
        .catch(error => {
            console.log(error)
        })
});

// форма відправки данних
function sendform() {
    let pers_data = document.getElementById('personal_data')
    let deliv_data = document.getElementsByClassName('delivery-block')[0].querySelector('input[type="radio"]:checked')
    let pay_info = document.getElementsByClassName('pay-block')[0].querySelector('input[type="radio"]:checked').value
    let product_data = document.getElementsByClassName('product')

    if (deliv_data.value == 'Самовивіз') {
        deliv_info = {
            'Самовивіз': document.getElementsByClassName(deliv_data.id)[0].getElementsByTagName('select')[0].value
        }

    } else if (deliv_data.value == 'Кур\'єр') {
        let info = document.getElementsByClassName(deliv_data.id)[0]
        deliv_info = {
            До_замовника: {
                Місто: info.getElementsByTagName('input').item(0).value,
                Вулиця: info.getElementsByTagName('input').item(1).value,
                Будинок: info.getElementsByTagName('input').item(2).value,
                Квартира: info.getElementsByTagName('input').item(3).value,
                Поверх: info.getElementsByTagName('select')[0].value,
                Ліфт: info.getElementsByTagName('select')[1].value,
            }
        }
    } else if ((deliv_data.value == 'Нова пошта')) {
        deliv_info = {
            'Нова пошта': document.getElementsByClassName(deliv_data.id)[0].getElementsByTagName('input')[0].value
        }

    } else if ((deliv_data.value == 'Укр пошта')) {
        deliv_info = {
            'Укр пошта': document.getElementsByClassName(deliv_data.id)[0].getElementsByTagName('input')[0].value
        }
    };

    let product_info = {}
    for (let item of product_data) {
        product_info[item.getElementsByTagName('input')[0].value] = item.getElementsByTagName('input')[1].value
    }

    let data = {
        client_info: {
            profile: pers_data.querySelector('input[name="profile"]').value,
            first_name: pers_data.querySelector('input[name="first_name"]').value,
            last_name: pers_data.querySelector('input[name="last_name"]').value,
            surname: pers_data.querySelector('input[name="surname"]').value,
            phone_number: pers_data.querySelector('select[name="phone_number_0"]').selectedOptions[0].innerHTML.split(' ')[1] + pers_data.querySelector('input[name="phone_number_1"]').value,
            email: pers_data.querySelector('input[name="email"]').value,
        },
        delivery: deliv_info,
        how_to_pay: pay_info,
        product: product_info
    };

    // console.log(data)
    return JSON.stringify(data)
};

// Видаляє нижній border останнього елемента в кошику
var myList = document.getElementsByClassName('cart-item')
if (myList.length > 0) {
    var lastItem = myList[myList.length - 1];
    lastItem.style.border = 'none'
}


// //  input - number phone
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
