function ProductViewer(numRows, productsPerRow) {
    this.update = (products) => {
        $('#cards').empty();

        for (let row = 0; row < numRows; row++){
            const deck = $('<div class="card-deck"></div>');

            for (let col = 0; col < productsPerRow; col++){
                const product = products[row * productsPerRow + col];
                
                const card = $(`
                    <div class="card text-center" style="width: 20rem;">
                        <img class="card-img-top mx-auto d-block" src="/static/img/products/${product.image}" style="width: 100px; height: 100px;">
                        <div class="card-body h-100">
                            <h6 class="card-title">${product.name}</h6>
                        </div>
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
            this.update(products)
        });
    }
    
      
}

$(document).on('click', '.add-to-cart-btn', function() {
    const card = $(this).closest('.card');
    const product = {
      name: card.find('.card-title').text(),
      price: card.find('.card-text').eq(0).text().slice(1),
      quantity: card.find('.product-quantity').val()
    };

    if (parseInt(product.quantity) > 0) {  // check if quantity is greater than 0
        console.log('Product added:', product);
        card.find('.product-added-message').fadeIn(500, function() {
          $(this).fadeOut(500);
        });

        // Update cart icon
        const currentQuantity = parseInt($('#cart-quantity').text());
        const newQuantity = currentQuantity + parseInt(product.quantity);
        $('#cart-quantity').text(newQuantity);
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

