function removeFromCart(productid) {
  fetch('/api/remove_from_cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      productid: productid
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    return response.json();
  })
  .then(data => {
    console.log(data.message);
    // Refresh cart view
    loadCart();
  })
  .catch(error => {
    console.error(error);
  });
}
