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
    let url = '/cart/'
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

let ad_fav = document.querySelectorAll('.add_to_fav')
ad_fav.forEach(btn => {
    btn.addEventListener('click', AddToFav)
})

function AddToFav(e) {
    if (e.target.id == 'to_fav') {
        item = ad_fav[0].getElementsByTagName('button')[0].value
    } else {
        item = e.target.value
    }
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

// Відповідь на відгук 
let show_textar = document.querySelectorAll('.answer button')
show_textar.forEach(btn => {
    btn.addEventListener('click', showtextarea)
})
function showtextarea(e) {
    e.originalTarget.style.display = 'none'
    e.target.nextElementSibling.style.display = 'block'
    let name = e.target.value.split(',')[0]
    let id = e.target.value.split(',')[1]
    e.target.nextElementSibling[2].value = id;
    e.target.nextElementSibling[1].innerText = `${name}, `
}

// materialize - збільшення головної картинки
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.materialboxed');
    M.Materialbox.init(elems);
});


//   Труш - доп. фото
document.querySelector('#thumbs').addEventListener('click', function (event) {
    event.preventDefault();
    let link = event.target.closest('a');
    document.querySelector('#largeImg').src = link.getAttribute('href');
    document.querySelector('#largeImg').alt = link.title;
})

// Повідомлення про добавлення товару до кошика
function Toast() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    let btn = document.getElementById('to_cart');
    btn.disabled = true;
    setTimeout(function(){ x.className = x.className.replace("show", ""); btn.disabled = false;}, 3000);

  }