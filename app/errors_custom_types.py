class DatabaseError(Exception):
    pass

class NotFoundError(DatabaseError):
    def __init__(self, object_type, object_id):
        self.message = f"{object_type.upper()}_NOT_FOUND: {object_id}"
        super().__init__(self.message)

class UpdateError(DatabaseError):
    def __init__(self, object_type, object_id):
        self.message = f"{object_type.upper()}_UPDATE_ERROR: {object_id}"
        super().__init__(self.message)

class ConstrictionViolatedError(DatabaseError):
    pass

class InsufficientFundsError(DatabaseError):
    pass

class RegistrationError(Exception):
    pass

class CodeExpired(RegistrationError):
    pass

class CodeLocked(RegistrationError):
    pass

class CodeInvalid(RegistrationError):
    pass

class RefreshTokenExpired(Exception):
    pass