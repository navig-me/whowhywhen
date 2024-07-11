import stripe
from app.config import STRIPE_SECRET_KEY
from app.models.user import SubscriptionPlan

stripe.api_key = STRIPE_SECRET_KEY

FREE_PLAN_LIMIT = 20000
STARTER_PLAN_LIMIT = 250000
PAID_PLAN_LIMIT = 5000000

STARTER_PLAN_ID = ['price_1PaBdIC0V9GgAoCfI9gq9MSL']
PRO_PLAN_ID = ['price_1PbDLyC0V9GgAoCfSjpbPwD3', 'price_1PaBfwC0V9GgAoCfzrHuBtZs']

def create_stripe_customer(name: str, email: str):
    customer = stripe.Customer.create(
        name=name,
        email=email
    )
    return customer.id

def get_user_subscription(current_user):
    user_email = current_user.email
    customers = stripe.Customer.list(email=user_email).data
    
    if not customers:
        return SubscriptionPlan.free
    
    print("Stripe customer found:", customers[0])

    customer_id = customers[0].id
    subscriptions = stripe.Subscription.list(customer=customer_id).data

    print("Subscriptions:", subscriptions)

    for subscription in subscriptions:
        if subscription.status == 'active':
            print("Subscription item:", subscription.plan)
            if subscription.plan.id == STARTER_PLAN_ID:
                return SubscriptionPlan.starter
            elif subscription.plan.id in PRO_PLAN_ID:
                return SubscriptionPlan.pro
    return SubscriptionPlan.free
        
def refresh_user_subscription(current_user, session):
    user_subscription_plan = current_user.subscription_plan
    stripe_subscription = get_user_subscription(current_user)
    if user_subscription_plan != stripe_subscription:
        # Update user's subscription plan in the database, update monthly limit, and credit reset date
        current_user.subscription_plan = stripe_subscription
        if current_user.subscription_plan == SubscriptionPlan.free:
            current_user.monthly_credit_limit = FREE_PLAN_LIMIT
        elif current_user.subscription_plan == SubscriptionPlan.starter:
            current_user.monthly_credit_limit = STARTER_PLAN_LIMIT
        elif current_user.subscription_plan == SubscriptionPlan.pro:
            current_user.monthly_credit_limit = PAID_PLAN_LIMIT
        current_user.monthly_credit_usage_crossed = False
        session.add(current_user)
        session.commit()

def get_payment_link(current_user, plan_name, session):
    if plan_name == SubscriptionPlan.free:
        return None
    elif plan_name == SubscriptionPlan.starter:
        price_id = STARTER_PLAN_ID[0]
    elif plan_name == SubscriptionPlan.pro:
        price_id = PRO_PLAN_ID[0]

    # Return subscription link with price_id
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card', 'link'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://whowhywhen.com/',
        customer_email=str(current_user.email),
        allow_promotion_codes=True,
    )
    return checkout_session.url

def cancel_subscription(current_user, session):
    # Retrieve the Stripe customer ID from the current user
    stripe_customer_id = current_user.stripe_customer_id

    # Get the user's subscriptions from Stripe
    subscriptions = stripe.Subscription.list(customer=stripe_customer_id).data
    
    for subscription in subscriptions:
        if subscription.status == 'active':
            # Cancel the subscription immediately and refund the prorated amount
            stripe.Subscription.delete(
                subscription.id,
                prorate=True
            )
            break

    # Update the user's subscription plan in the database to free
    current_user.subscription_plan = SubscriptionPlan.free
    current_user.monthly_credit_limit = FREE_PLAN_LIMIT
    current_user.monthly_credit_usage_crossed = False
    
    # Save the changes to the database
    session.add(current_user)
    session.commit()

def get_customer_portal_url(current_user):
    stripe_customer_id = current_user.stripe_customer_id

    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url='https://whowhywhen.com/'
    )
    return session.url
