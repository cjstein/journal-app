// static/main.js

console.log("Sanity check!");

// Get Stripe publishable key
fetch("/subscription/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // new
        // Event handler for Annual Subscription
        let Btn = document.querySelector(".stripe-button");
        if (Btn !== null) {
            Btn.addEventListener("click", () => {
                var price = Btn.id
                // Get Checkout Session ID
                fetch("/subscription/create-checkout-session/?price=" + price)
                    .then((result) => { return result.json(); })
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
    });

