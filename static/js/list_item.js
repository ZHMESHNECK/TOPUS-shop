
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
        console.log(index)
        const ratingActiveWidth = index / 0.05;
        console.log(ratingActiveWidth)
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }
}
