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


// Функція розрахунку рейтингу товару

const ratings = document.querySelectorAll('.rating');
if (ratings.length > 0) {
    initRatings();
}

function initRatings() {
    let ratingActive, ratingValue;
    for (let index = 0; index < ratings.length; index++) {
        const rating = ratings[index];
        initRating(rating);
    }


    function initRating(rating) {
        initRatingVars(rating);
        setRatingActiveWidth();
    }

    function initRatingVars(rating) {
        ratingActive = rating.querySelector('.rating__active');
        ratingValue = rating.querySelector('.rating__value');
    }

    function setRatingActiveWidth(index = ratingValue.innerHTML) {
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }
}


// Додання до улюбленого

let ad_fav = document.querySelectorAll('.to_fav')
ad_fav.forEach(btn => {
    btn.addEventListener('click', AddToFav)
})

function AddToFav(e) {
    item = e.srcElement.attributes.value.value
    let url = '/add_to_fav/' + item.toString()

    fetch(url, {
        'method': 'POST',
        'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken }
    })
        .then(res => res.json())
        .then(data => {
            if (data.data) {
                document.getElementById(data.id).childNodes[0].className = 'fa-solid fa-heart fa-lg'
            }
            else {
                document.getElementById(data.id).childNodes[0].className = 'fa-regular fa-heart fa-lg';
            }
        })
        .catch(error => {
            console.log(error.data)
        })
}

// ordering
// Підставляемо в поля збереженні данні
document.addEventListener('DOMContentLoaded', function () {
    // Отримуємо збережене значення з localStorage
    var savedSortValue = localStorage.getItem('selectedSorting')
    var savedPriceValue = [localStorage.getItem('min_price'), localStorage.getItem('max_price')]

    // Встановлюємо збережене значення у селект
    if (savedSortValue) {
        document.getElementById('orderSelect').value = savedSortValue;
    }
    if (savedPriceValue) {
        document.getElementById('input-with-keypress-0').value = savedPriceValue[0];
        document.getElementById('input-with-keypress-1').value = savedPriceValue[1];
    }
    // якщо в url присутній шлях "api", то відаляємо блок сортування
    if (window.location.href.includes('api')){
        document.getElementsByClassName('catalog-settings')[0].style.display = 'none'
    }
});

function applyOrdering() {
    var selectedValue = document.getElementById('orderSelect').value;
    var currentUrl = window.location.href;

    // Зберегти обрану опцію сортування в локальному сховищі
    localStorage.setItem('selectedSorting', selectedValue);

    // Перевірити, чи містить URL параметр 'page'
    var regex = new RegExp('(ordering=.*?)($|&)');
    var match = currentUrl.match(regex);

    if (match) {
        // Заменяем значение параметра
        var newUrl = currentUrl.replace(regex, 'ordering=' + selectedValue + '$2');

        // Изменяем URL
        window.location.href = newUrl;
    } else {
        // Если параметр не найден, добавляем его к URL
        var separator = currentUrl.includes('?') ? '&' : '?';
        var newUrl = currentUrl + separator + 'ordering=' + selectedValue;

        // Изменяем URL
        window.location.href = newUrl;
    }
}

// ordering price


document.addEventListener('DOMContentLoaded', () => {
    var stepsSlider = document.getElementById('slider');
    var input0 = document.getElementById('input-with-keypress-0');
    var input1 = document.getElementById('input-with-keypress-1');
    var storedMinPrice = localStorage.getItem('min_price');
    var storedMaxPrice = localStorage.getItem('max_price');


    var startValues = [storedMinPrice ? parseFloat(storedMinPrice) : 0, storedMaxPrice ? parseFloat(storedMaxPrice) : 100];
    
    var inputs = [input0, input1];
    
    noUiSlider.create(stepsSlider, {
        start: [0, 50000],
        connect: true,
        tooltips: false,
        range: {
            'min': 0,
            'max': 50000
        },
        format: {
            to: function (value) {
                // Форматуємо значення, прибираючи десяткові знаки та поділяючи тисячі
                return Math.round(value);
            },
            from: function (value) {
                // Парсим значення назад до числа
                return parseFloat(value);
            }
        }
    });
    
    if (window.location.href.includes('min_price')) {
    stepsSlider.noUiSlider.updateOptions({
        start: startValues
    })};
    // Зв'язуємо поле введення з повзунком
    stepsSlider.noUiSlider.on('update', function (values, handle) {
        inputs[handle].value = values[handle];
    });

    // Обробляємо зміни у полях введення
    inputs.forEach(function (input, handle) {
        input.addEventListener('change', function () {
            var values = [input0.value, input1.value];
            stepsSlider.noUiSlider.set(values);
        });

    });
});

var priceform = document.getElementById('PriceOrdering')
priceform.addEventListener('submit', function (e) {
    var currentUrl = window.location.href;
    var minPrice = document.getElementById('input-with-keypress-0').value;
    var maxPrice = document.getElementById('input-with-keypress-1').value;

    var str_ord_price = 'min_price=' + minPrice + '&max_price=' + maxPrice

    localStorage.setItem('min_price', minPrice);
    localStorage.setItem('max_price', maxPrice);

    var regex_min = new RegExp('(min_price=.*?)($|&)');
    var regex_max = new RegExp('(max_price=.*?)($|&)');
    var match = currentUrl.match(regex_min) || currentUrl.match(regex_max);

    if (match) {
        var newUrl = currentUrl.replace(regex_min, 'min_price=' + minPrice + '$2').replace(regex_max, 'max_price=' + maxPrice + '$2');
        window.location.href = newUrl
    } else {
        // Если параметр не найден, добавляем его к URL
        var separator = currentUrl.includes('?') ? '&' : '?';
        var newUrl = currentUrl + separator + str_ord_price;

        // Изменяем URL
        window.location.href = newUrl;
    }

    e.preventDefault()

})