class DatabaseError(Exception):
    pass


class UserNotFoundError(DatabaseError):
    pass


class UserUpdateError(DatabaseError):
    pass


class CompanyNotFoundError(DatabaseError):
    pass


class CompanyUpdateError(DatabaseError):
    pass


class FoundationNotFoundError(DatabaseError):
    pass


class FoundationUpdateError(DatabaseError):
    pass

class FundraisingNotFoundError(DatabaseError):
    pass


class FundraisingUpdateError(DatabaseError):
    pass


class NewsNotFoundError(DatabaseError):
    pass


class NewsUpdateError(DatabaseError):
    pass

class ConstrictionViolatedError(DatabaseError):
    pass

class InsufficientFundsError(DatabaseError):
    pass