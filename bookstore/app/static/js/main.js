let touchEvent = 'ontouchstart' in window ? 'touchstart' : 'click';


function update_cart_counter() {
    $.ajax({
        type: 'post',
        url: "/get_count_books_in_cart",
        context: document.body,
        contentType: 'application/json',
        success: function (data) {
            $(`#${data['id']}`).find('.js-product__btn-loading').css("display", "none");
            if (data.success === true) {

                $(`.cart__counter`).text(data.count)
            }
        }
    });
}


function addToCart() {
    // Добавление в корзину

    let id = $(this).attr('data-id')

    $(this).children("span").css("display", "none");
    $(this).children(".js-product__btn-loading").css("display", "block");
    $(this).prop('disabled', true);
    $.ajax({
        type: 'post',
        url: "/add",
        context: document.body,
        contentType: 'application/json',
        data: JSON.stringify({ "id": id }),

        success: function (data) {
            $(`#${data['id']}`).find('.js-product__btn-loading').css("display", "none");

            if (data.success === true) {
                $(`#${data['id']}`).replaceWith("<a href='/cart' class='product__btn _add'>Оформить</a>")
                $(`#${data['id']}`).replaceWith("<a href='/cart' class='product__btn _add'>Оформить</a>")

            } else {
                $(`#${data['id']}`).prop('disabled', false);
                $(`#${data['id']}`).find(".js-product__btn-text").css("display", "block");
            }
            if (data.redirect) {
                window.location.href = data.redirect;
            }
            $(`#${data['id']}`).find('.js-product__btn-loading').css("display", "none");

            update_cart_counter()

        },
    });

}

$(document).ready(function () {
    $('.js-product__btn').on('click touchstart onfocus', addToCart)
});
