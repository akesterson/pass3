class DecryptionError(Exception):
    """
    An error occurred while trying to decrypt a message
    """
    pass

class EncryptionError(Exception):
    """
    An error occurred while trying to encrypt a message
    """
    pass

class PasswordException(Exception):
    """
    An error occurred while checking the user's password
    """
    pass
