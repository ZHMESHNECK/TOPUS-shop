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


// Додання до кошика

let ad_cart = document.querySelectorAll('.add_to_cart_btn button')
ad_cart.forEach(btn => {
    btn.addEventListener('click', AddToCart)
})

function AddToCart(e) {
    let item = e.target.value
    let url = '/cart'

    let data = {
        product_id: Number(item),
        quantity: 1
    }

    fetch(url, {
        'method': 'POST',
        'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        'body': JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('num_of_cart').innerHTML = data.len
        })
        .catch(error => {
            console.log(error)
        })
}

// Додання до улюбленого

let ad_fav = document.querySelectorAll('.add_to_fav button')
ad_fav.forEach(btn => {
    btn.addEventListener('click', AddToFav)
})

function AddToFav(e) {
    let item = e.target.value
    let url = '/add_to_fav/' + item.toString()

    fetch(url, {
        'method': 'POST',
        'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken }
    })
        .then(res => res.json())
        .then(data => {
            if (data.data) {
                document.getElementById('to_fav').className = 'fa-solid fa-heart fa-lg'
            }
            else {
                document.getElementById('to_fav').className = 'fa-regular fa-heart fa-lg';
            }
        })
        .catch(error => {
            console.log(error.data)
        })

}

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


// google pay

var paymentsClient =
    new google.payments.api.PaymentsClient({ environment: 'TEST' });

const baseRequest = {
    apiVersion: 2,
    apiVersionMinor: 0
};

const allowedCardNetworks = ["MASTERCARD", "VISA"];

const baseCardPaymentMethod = {
    type: 'CARD',
    parameters: {
        allowedAuthMethods: allowedCardAuthMethods,
        allowedCardNetworks: allowedCardNetworks
    }
};

const isReadyToPayRequest = Object.assign({}, baseRequest);
isReadyToPayRequest.allowedPaymentMethods = [baseCardPaymentMethod];

paymentsClient.isReadyToPay(isReadyToPayRequest)
    .then(function (response) {
        if (response.result) {
            // add a Google Pay payment button
        }
    })
    .catch(function (err) {
        // show error in developer console for debugging
        console.error(err);
    });