

$(document).ready(function(){
    $('form').change(function(){
        price = parseFloat($("input[name='delivery_method']:checked").attr("price"))
        total_products_price = parseFloat($("#total_products_price").text())
        delivery_price = $("#delivery_price")
        total_order_price = $("#total_order_price")
        delivery_price.text(price)
        total_order_price.text(total_products_price+price)
})});
