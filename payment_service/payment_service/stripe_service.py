import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_stripe_payment(amount, currency, order_id):
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe expects amount in cents
            currency=currency,
            metadata={"order_id": str(order_id)}
        )
        return intent.client_secret
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return None