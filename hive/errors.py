import colorama


class InvalidCredentialsError(Exception):
    """Exception raised for invalid credentials."""
    def __init__(self, message=(
           colorama.Fore.RED +
           "ERROR (LOGIN_FAILED): Invalid username or password"
           + colorama.Style.RESET_ALL
                 )):
        self.message = message
        super().__init__(self.message)
