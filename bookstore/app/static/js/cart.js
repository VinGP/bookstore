const formatNumber = (x) => x.toString().replace(/\B(?<!\.\d)(?=(\d{3})+(?!\d))/g, ' ');


function hash(string) {
    string = string.toString();
    let hash = 0;
    for (let i = 0; i < string.length; i++) {
        hash = (((hash << 5) - hash) + string.charCodeAt(i)) & 0xFFFFFFFF;
    }

    return hash;
}

function object(obj) {
    let result = 0;
    for (let property in obj) {
        if (obj.hasOwnProperty(property)) {
            result += hash(property + hashCode(obj[property]));
        }
    }

    return result;
}

function hashCode(value) {
    const types =
    {
        'string': hash,
        'number': hash,
        'boolean': hash,
        'object': object
    };
    const type = typeof value;

    return value != null && types[type] ? types[type](value) + hash(type) : 0;
}

function isDict(obj) {
    return typeof obj === "object" && obj !== null && !(obj instanceof Array) && !(obj instanceof Date);
}


function withUniqueArguments(func, delay) {
    const map = [], ids = {};

    return function wrapper() {
        const args = [];
        let uniqueArgumentKey = undefined;

        for (let key = 0; key < arguments.length; key++) {
            const arg = arguments[key];

            if (isDict(arg) && "uniqueArgumentKey" in arg)
                uniqueArgumentKey = arg["uniqueArgumentKey"];
            else
                args.push(arg);
        }

        const hash = hashCode(uniqueArgumentKey || args);

        if (!map.includes(hash))
            map.push(hash);

        clearTimeout(ids[hash]);
        ids[hash] = setTimeout(() => {
            func(...args);
            clearTimeout(ids[hash]);
            delete map[map.indexOf(hash)];
            ids[hash] = 0;
        }, delay);
    };
}




function update_count_book_in_cart(id) {
    $(`#${id}`).find(".counter__button").prop('disabled', true)
    $.ajax({
        type: 'post',
        url: "/update_count_book_in_cart",
        context: document.body,
        contentType: 'application/json',
        data: JSON.stringify({ "id": id, "count": $(`#${id}`).find(".counter__input").val() }),
        success: function (data) {
            if (data.success === true) {
                $(`#${data['id']}`).find(".counter__input").val(data.count);
                $(`#${data['id']}`).find(".subtotal").text(data.total_price_book + " руб.")
                $(`#total-price`).text(data.total_cart_price)
                $(`.js-basket-summary__item-weight`).text(data.cart_weight)
            }
            $(`#${id}`).find(".counter__button").prop('disabled', false)
        }
    });
}


update_count_book_in_cart_debounce = withUniqueArguments(update_count_book_in_cart, 500)

const calculateSeparateItem = (basketItem, action) => {
    const input = basketItem.querySelector('.counter__input')
    id = input.dataset.id
    switch (action) {
        case 'plus':
            input.value++;
            break;
        case 'minus':
            input.value--;
            break;
    }
    update_count_book_in_cart_debounce(id)
};


document.getElementById('basket').addEventListener('click', (event) => {

    if (event.target.classList.contains("counter__button_minus")) {
        const input = event.target.closest('.basket-item').querySelector('.counter__input');

        if (Number(input.value) !== 1) {
            calculateSeparateItem(event.target.closest('.basket-item'),
                'minus');
            const b = event.target.closest('.basket-item').querySelector('.counter__input')

        }
    }
    if (event.target.classList.contains("counter__button_plus")) {
        calculateSeparateItem(event.target.closest('.basket-item'),
            'plus');
    }
})

function plural(number, titles) {
    let cases = [2, 0, 1, 1, 1, 2];
    return titles[(number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number % 10 < 5) ? number % 10 : 5]];
}


function initCart() {
    $('.basket-item__btn-cart-del').on('click', delItem);
}

function delItem() {
    // удаляю товар из корзины
    let id = $(this).attr('data-id');
    $.ajax({
        type: 'post',
        url: "/delete_cart_book",
        context: document.body,
        contentType: 'application/json',
        data: JSON.stringify({ "id": id }),

        success: function (data) {
            if (data.success === true) {
                $(`#total-price`).text(data.total_cart_price)
                update_cart_counter()
                $(`.js-basket-summary__item-count`).text(data.count_books_in_cart)
                $(`.js-basket-summary__item-weight`).text(data.cart_weight)
                if (data.count_books_in_cart === 0) {
                    $(`#total-price`).text(data.total_cart_price)
                    $('.basket').html(`
            <div style="margin: auto;">
            <h2 align="center">Ваша корзина сейчас пуста</h2>
            </div>
            `);
                }
            }
        }
    });
    $(`div .basket-item#${id} `).remove()
}

$(document).ready(function () {
    initCart()
});




