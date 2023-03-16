$(document).ready(function() {
  const urlParams = new URLSearchParams(window.location.search);
  const productid = urlParams.get('productid');
  console.log(productid);

  $.get('/api/get_product_detail', { productid: productid }, (product) => {
    // Update the DOM to display the product details
    $('.product-name').text(`${product[0].name}`);
    $('.product-price').text(`$${product[0].price}`);
    $('.product-weight').text(product[0].weight);
    $('.product-image').attr('src', `/static/img/products/${product[0].image}`);
  });

  const cartQuantity = sessionStorage.getItem('cartQuantity');
  if (cartQuantity !== null) {
    $('#cart-quantity').text(cartQuantity);
  }

  $(document).off('click', '.add-to-cart-btn').on('click', '.add-to-cart-btn', function() {
    const card = $(this).closest('.card');
    const product = {
      productId: card.find('.product-id').text(),
      name: card.find('.card-title').text(),
      price: card.find('.product-price').text().slice(1),
      quantity: card.find('.product-quantity').val(),
      weight: card.find('.product-weight').text(),
      image: card.find('.product-image').attr('src'),
      productid: productid // include productid in the object
    };

    if (parseInt(product.quantity) > 0) {
      console.log('Product added:', product);
      card.find('.product-added-message').fadeIn(500, function() {
        $(this).fadeOut(500);
      });

      // Update cart icon and total
      const currentQuantity = parseInt($('#cart-quantity').text());
      const newQuantity = currentQuantity + parseInt(product.quantity);
      $('#cart-quantity').text(newQuantity);

      const currentTotal = parseFloat($('.cart-total').text().slice(1));
      const newTotal = currentTotal + parseFloat(product.price) * parseInt(product.quantity);
      $('.cart-total').text(`Total: $${newTotal.toFixed(2)}`);

      // Save product details to database
      console.log(product.productId); // check that productId is not empty
      $.ajax({
        url: '/api/add_to_cart',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(product),
        success: function(data) {
          console.log('Product saved to database:', data);
          sessionStorage.setItem('cartQuantity', newQuantity);
        },
        error: function(xhr, status, error) {
          console.error('Error saving product to database:', error);
        }
      });
    }
  });
});

function incrementQuantity(button) {
  const input = $(button).closest('.input-group').find('.product-quantity');
  input.val(parseInt(input.val()) + 1);
}

function decrementQuantity(button) {
  const input = $(button).closest('.input-group').find('.product-quantity');
  input.val(Math.max(parseInt(input.val()) - 1, 0));
}