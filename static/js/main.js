function switchPaymentMethod(type, content) {
   const stripeCard = document.getElementById('stripe-card');
   const stripePaymentElement = document.getElementById('payment-element');
   const paypalCard = document.getElementById('paypal-card');
   if (type === 'stripe') {
       paypalCard.style.display = 'none'
       stripeCard.style.display = 'block'
       paypalCard.innerHTML = ''
   } else {
       stripeCard.style.display = 'none'
       paypalCard.style.display = 'block'
       stripePaymentElement.innerHTML = ''
       paypalCard.innerHTML = content
   }
}

async function createPaypalSession() {
   try {
       const form = document.getElementById('form-user-info');
       const formData = new FormData(form);
       const { data } = await axios.post("/checkout/paypal", formData);
       switchPaymentMethod('paypal', data)
   } catch (e) {
       notyf.error(e.response.data.message);
   }
 }
