import stripe
from app.config import STRIPE_SECRET_KEY
from datetime import datetime
from app.models.user import SubscriptionPlan

stripe.api_key = STRIPE_SECRET_KEY

FREE_PLAN_LIMIT = 20000
STARTER_PLAN_LIMIT = 250000
PAID_PLAN_LIMIT = 5000000

STARTER_PLAN_ID = ['price_1PaBdIC0V9GgAoCfI9gq9MSL']
PRO_PLAN_ID = ['price_1PbDLyC0V9GgAoCfSjpbPwD3', 'price_1PaBfwC0V9GgAoCfzrHuBtZs']

def get_subscription_end_date(user):
    user_email = user.email
    customers = stripe.Customer.list(email=user_email).data
    
    if not customers:
        return None
    
    customer_id = customers[0].id
    subscriptions = stripe.Subscription.list(customer=customer_id).data

    for subscription in subscriptions:
        if subscription.status in ['active', 'trialing', 'past_due']:
            return datetime.fromtimestamp(subscription.current_period_end)
    return None

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
        return SubscriptionPlan.free, None
    
    customer_id = customers[0].id
    subscriptions = stripe.Subscription.list(customer=customer_id).data

    for subscription in subscriptions:
        print("###### Subscription plan:", subscription.plan)
        print("###### Subscription status:", subscription.status)
        if subscription.status in ['active', 'trialing', 'past_due']:
            plan_id = subscription.plan.id
            end_date = datetime.fromtimestamp(subscription.current_period_end)
            if plan_id in STARTER_PLAN_ID:
                return SubscriptionPlan.starter, end_date
            elif plan_id in PRO_PLAN_ID:
                return SubscriptionPlan.pro, end_date
    return SubscriptionPlan.free, None
        
def refresh_user_subscription(current_user, session):
    user_subscription_plan, subscription_end_date = get_user_subscription(current_user)
    if current_user.subscription_plan != user_subscription_plan:
        current_user.subscription_plan = user_subscription_plan
        if current_user.subscription_plan == SubscriptionPlan.free:
            current_user.monthly_credit_limit = FREE_PLAN_LIMIT
        elif current_user.subscription_plan == SubscriptionPlan.starter:
            current_user.monthly_credit_limit = STARTER_PLAN_LIMIT
        elif current_user.subscription_plan == SubscriptionPlan.pro:
            current_user.monthly_credit_limit = PAID_PLAN_LIMIT
        current_user.monthly_credit_usage_crossed = False
        current_user.monthly_credit_limit_reset = datetime.now() if not subscription_end_date else subscription_end_date
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


def get_customer_portal_url(current_user):
    stripe_customer_id = current_user.stripe_customer_id

    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url='https://whowhywhen.com/'
    )
    return session.url
