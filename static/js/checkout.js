document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe('pk_test_51Pv04PP40o7MRH4j6mYclNI0Ew5jUWjKeWrWze3eDqflhr86wFj7JUbV1b0aTZ9P3wYvftAonOz4IMQsAdSSt18700IzRuqSrm');
    var elements = stripe.elements();
    var cardElement = elements.create('card', {
        style: {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        }
    });
    cardElement.mount('#card-element');

    var form = document.getElementById('payment-form');
    var paymentContainer = document.getElementById('payment-container');
    var submitButton = document.getElementById('submit-button');
    var paymentMessage = document.getElementById('payment-message');
    var startPaymentButton = document.getElementById('start-payment-button');
    var productSelect = document.getElementById('product-select');
    var customerNameInput = document.getElementById('customer-name');
    var customerEmailInput = document.getElementById('customer-email');
    var totalPriceDiv = document.getElementById('total-price');

    // Update total price based on selected product
    productSelect.addEventListener('change', function() {
        var selectedOption = productSelect.options[productSelect.selectedIndex];
        var price = selectedOption.getAttribute('data-price');
        totalPriceDiv.textContent = 'Total: £' + price;
    });

    // Show the payment form when a product is selected and "Proceed to Payment" is clicked
    startPaymentButton.addEventListener('click', function() {
        var selectedProduct = productSelect.value;
        var customerName = customerNameInput.value.trim();
        var customerEmail = customerEmailInput.value.trim();

        if (selectedProduct && (sessionStorage.getItem('username') || customerName)) {
            paymentContainer.style.display = 'block';
        } else {
            alert('Please select a product and enter your name.');
        }
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        submitButton.disabled = true;

        var selectedProduct = productSelect.value; // Get the product price in pence
        var customerName = customerNameInput.value.trim(); // Get customer name
        var customerEmail = customerEmailInput.value.trim(); // Get customer email

        // Create PaymentIntent
        fetch('/create-payment-intent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: selectedProduct, customer_name: customerName, customer_email: customerEmail }) // Send selected product price, name, and email
        })
        .then(function(response) {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text); });
            }
            return response.json();
        })
        .then(function(paymentIntent) {
            return stripe.confirmCardPayment(paymentIntent.clientSecret, {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: customerName,  // Attach the customer's name to payment details
                    }
                }
            });
        })
        .then(function(result) {
            if (result.error) {
                paymentMessage.textContent = result.error.message;
                paymentMessage.classList.remove('hidden');
                submitButton.disabled = false;
            } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                paymentMessage.textContent = 'Payment successful!';
                paymentMessage.classList.remove('hidden');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            paymentMessage.textContent = 'Payment failed!';
            paymentMessage.classList.remove('hidden');
            submitButton.disabled = false;
        });
    });
});
