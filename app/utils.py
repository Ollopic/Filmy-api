import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def validate_boolean_param(param):
    """Helper function to validate boolean-like parameters."""
    return param in ["true", "false", "True", "False", "1", "0"]


def validate_state_param(state):
    """Helper function to validate state parameter."""
    return state in ["Physique", "Numérique"]
