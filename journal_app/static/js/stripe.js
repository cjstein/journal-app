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
        let annualBtn = document.querySelector("#price_1IVpLVEAWjMWH1Xh1LyZ2lx8");
        if (annualBtn !== null) {
            annualBtn.addEventListener("click", () => {
                var price = annualBtn.id
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
        // Event handler for Monthly Subscription
        let monthlyBtn = document.querySelector("#price_1IVpLVEAWjMWH1XhtRoR63IS");
        if (monthlyBtn !== null) {
            monthlyBtn.addEventListener("click", () => {
                var price = monthlyBtn.id
                // Get Checkout Session ID
                fetch(`/subscription/create-checkout-session/?price=${price}`)
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
