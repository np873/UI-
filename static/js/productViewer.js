function ProductViewer(numRows, productsPerRow) {
    let product;
    this.update = (products) => {
        $('#cards').empty();

        for (let row = 0; row < numRows; row++){
            const deck = $('<div class="card-deck"></div>');

            for (let col = 0; col < productsPerRow; col++){
                
                product = products[row * productsPerRow + col];
                
                const card = $(`
                    <div class="card text-center" style="width: 20rem;">
                    <a href="#" class="product-link" data-toggle="collapse" data-target="#product-details-${product.productid}" id="product-link-${product.productid}">
                            <img class="card-img-top mx-auto d-block" src="/static/img/products/${product.image}" style="width: 100px; height: 100px;">
                            <div class="card-body h-100">
                                <h6 class="card-title product-name">${product.name}</h6>
                            </div>
                            </a>
                            <div class="card-body">
                                <p class="card-text">$${product.price}</p>
                                <p class="card-text text-secondary">${product.weight}</p>
                            </div>
                        

                        <div class="card-footer bg-transparent">
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <button class="btn btn-outline-secondary" type="button" onclick="decrementQuantity(this)">-</button>
                                </div>
                                <input type="text" class="form-control product-quantity text-center" value="0" min="0">
                                
                                <div class="input-group-append">
                                    <button class="btn btn-outline-secondary" type="button" onclick="incrementQuantity(this)">+</button>
                                </div>
                                
                            </div>
                            <div style="padding-top: 1.5rem;">
                                <button type="button" class="btn btn-primary text-center add-to-cart-btn" style="width: 50%;">Add to cart</button>
                            </div>
                            <p class="product-added-message" style="display: none; padding: 0.5rem;">Added to cart</p>
                        </div>
                        
                    </div>
                `);

                $(deck).append(card);
            }
            $('#cards').append(deck);
        }
    }
     

    this.load = (categoryid) => {
        console.log('Category ID:', categoryid);
    
        $.get('/api/get_products', {
            categoryid: categoryid || '',
            n: numRows * productsPerRow
        }, (products) => {
            // add productid property to each product object
            
            this.update(products);
        });
    }
}

$(document).on('click', '.product-link', function(event) {
    event.preventDefault();  // prevent the default link behavior
    const productid = $(this).attr('id').replace('product-link-', '');  // extract the product ID from the anchor tag ID
    window.location.href = `/product_detail?productid=${productid}`;  // navigate to the product details page for the clicked product
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

  
function incrementQuantity(button) {
    const input = $(button).closest('.input-group').find('.product-quantity');
    input.val(parseInt(input.val()) + 1);
}

function decrementQuantity(button) {
    const input = $(button).closest('.input-group').find('.product-quantity');
    input.val(Math.max(parseInt(input.val()) - 1, 0));
}