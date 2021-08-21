// static/main.js

console.log("Sanity check!");

function checkout(price) {
// Get Stripe publishable key
    fetch("/subscription/config/")
        .then((result) => { return result.json(); })
        .then((data) => {
            // Initialize Stripe.js
            const stripe = Stripe(data.publicKey);
            // Get Checkout Session ID
            fetch("/subscription/create-checkout-session/?price=" + price)
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    console.log(data);
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
                .then((res) => {
                    console.log(res);
                });
        });
}

