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
                            <img class="product-image card-img-top mx-auto d-block" src="/static/img/products/${product.image}" style="width: 100px; height: 100px;">
                            <div class="card-body h-100">
                                <h6 class="card-title product-name">${product.name}</h6>
                            </div>
                            </a>
                            <div class="card-body">
                                <p class="card-text product-price">$${product.price}</p>
                                <p class="card-text product-weight text-secondary">${product.weight}</p>
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
$(document).ready(function() {
$('#cart-quantity').text(cart_quantity);
$(document).on('click', '.product-link', function(event) {
    event.preventDefault();  // prevent the default link behavior
    const productid = $(this).attr('id').replace('product-link-', '');  // extract the product ID from the anchor tag ID
    window.location.href = `/product_detail?productid=${productid}`;  // navigate to the product details page for the clicked product
});

$(document).off('click', '.add-to-cart-btn').on('click', '.add-to-cart-btn', function() {
    if (!user) {
        showAlertIfNotSignedIn();
    } else {
        addToCart(this);
    }
}
);})

function addToCart(clickedButton) {
    const card = $(clickedButton).closest('.card');
    const productid = $(clickedButton).closest('.card').find('.product-link').attr('id').replace('product-link-', '');
    const product = {
      productId: card.find('.product-id').text(),
      name: card.find('.product-name').text(),
      price: card.find('.product-price').text().slice(1),
      quantity: card.find('.product-quantity').val(),
      weight: card.find('.product-weight').text(), 
      image: card.find('.product-image').attr('src'),
      productid: productid,
      cartQuantity: cart_quantity, 
    };
    if (parseInt(product.quantity) > 0) {
      console.log('Product added:', product);
      card.find('.product-added-message').fadeIn(500, function() {
        $(this).fadeOut(500);
      });

      // Update cart icon and total
      const newQuantity =  cart_quantity + parseInt(product.quantity);
      $('#cart-quantity').text(newQuantity);
      product.cartQuantity = newQuantity;
      cart_quantity = newQuantity;

      // Save product details to database
      console.log(product.productId); // check that productId is not empty
      $.ajax({
        url: '/api/add_to_cart',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(product),
        success: function(data) {
          console.log('Product saved to database:', data);
        },
        error: function(xhr, status, error) {
          console.error('Error saving product to database:', error);
        }
      });
    }
}

function showAlertIfNotSignedIn() {
    alert("Please sign in to add products to cart!");
}

function incrementQuantity(button) {
    const input = $(button).closest('.input-group').find('.product-quantity');
    input.val(parseInt(input.val()) + 1);
}

function decrementQuantity(button) {
    const input = $(button).closest('.input-group').find('.product-quantity');
    input.val(Math.max(parseInt(input.val()) - 1, 0));
}