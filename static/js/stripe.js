// إنشاء جلسة دفع
const session = stripe.createCheckoutSession({
    amount: {{ transaction.amount }} * 100,
    currency: "USD",
    payment_method_types: ["card"],
});

// إرجاع العميل إلى Stripe لإكمال الدفع
window.location.href = session.url;
