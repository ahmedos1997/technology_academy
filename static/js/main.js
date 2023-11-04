// استيراد Stripe
import Stripe from "stripe";

// تهيئة Stripe
Stripe.setPublishableKey(process.env.STRIPE_PUBLISHABLE_KEY);
