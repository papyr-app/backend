class AuthorizationError(Exception):
    def __init__(self, message="You are not authorized to access this resource."):
        self.message = message
        super().__init__(self.message)
