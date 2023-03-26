
const formatNumber = (x) => x.toString().replace(/\B(?<!\.\d)(?=(\d{3})+(?!\d))/g, ' ');



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
    $.ajax({
        type: 'post',
        url: "/update_count_book_in_cart",
        context: document.body,
        contentType: 'application/json',
        data: JSON.stringify({ "id": id, "count": input.value }),
        success: function (data) {
            if (data.success === true) {
                $(`#${data['id']}`).find(".counter__input").val(data.count);
                $(`#${data['id']}`).find(".subtotal").text(data.total_price_book + " руб.")
                $(`#total-price`).text(data.total_cart_price)
                $(`.js-basket-summary__item-weight`).text(data.cart_weight)
            }
        }
    });
};


document.getElementById('basket').addEventListener('click', (event) => {

    if (event.target.classList.contains("counter__button_minus")) {
        const input = event.target.closest('.basket-item').querySelector('.counter__input');

        if (Number(input.value) !== 1) {
            calculateSeparateItem(event.target.closest('.basket-item'),
                'minus');
            const b = event.target.closest('.basket-item').querySelector('.counter__input')
            console.log(b);
            console.log(b.dataset.id);

        }
    }
    if (event.target.classList.contains("counter__button_plus")) {
        calculateSeparateItem(event.target.closest('.basket-item'),
            'plus');
        console.log(event.target.dataset.id);
    }
})

function plural(number, titles) {
    let cases = [2, 0, 1, 1, 1, 2];
    return titles[(number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number % 10 < 5) ? number % 10 : 5]];
}


function initCart() {
    $('.basket-item__btn-cart-del').on('click', delItem);

    //    $('#quantityOfGoods').html(cart["count"] + ' ' + plural(Number(cart["count"]), ['товар', 'товара', 'товаров']));

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




