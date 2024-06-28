import stripe
from app.config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'API Usage Plan',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://whowhywhen.com/subscription/success',
        cancel_url='https://whowhywhen.com/subscription/cancel',
    )
    return session.id
