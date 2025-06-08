class DatabaseError(Exception):
    pass

class NotFoundError(DatabaseError):
    def __init__(self, object_type, object_id):
        self.message = f"{object_type.upper()}_NOT_FOUND: {object_id}"
        super().__init__(self.message)

class UserUpdateError(DatabaseError):
    pass

class CompanyUpdateError(DatabaseError):
    pass

class FoundationUpdateError(DatabaseError):
    pass

class FundraisingUpdateError(DatabaseError):
    pass

class NewsUpdateError(DatabaseError):
    pass

class ConstrictionViolatedError(DatabaseError):
    pass

class InsufficientFundsError(DatabaseError):
    pass

class RegistrationError(Exception):
    pass