import pyotp

def generate_totp_secret():
    return pyotp.random_base32()

def generate_totp_uri(secret, username, issuer_name):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(username, issuer_name=issuer_name)

def verify_totp_token(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
