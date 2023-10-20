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

let ad_cart = document.querySelectorAll('.add_to_cart_btn button')
let ad_fav = document.querySelectorAll('.add_to_fav button')

ad_fav.forEach(btn => {
    btn.addEventListener('click', AddToFav)
})

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

function AddToFav(e) {
    let item = e.target.value
    let url = '/add_to_fav/' + item.toString()
    console.log(url)

    fetch(url, {
        'method': 'POST',
        'headers': { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken }
    })
        .then(res => res.json())
        .then(data => {
            // console.log(data.data)
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