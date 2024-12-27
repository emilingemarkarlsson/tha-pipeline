import dash_auth

# Lista över giltiga användarnamn och lösenord
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'password123',
    'user': 'userpassword'
}

def add_authentication(app):
    """
    Lägger till Basic Authentication till Dash-appen.
    """
    dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)