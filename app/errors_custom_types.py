class DatabaseError(Exception):
    pass


class UserNotFoundError(DatabaseError):
    pass


class UserUpdateError(DatabaseError):
    pass


class LegalEntityNotFoundError(DatabaseError):
    pass


class LegalEntityUpdateError(DatabaseError):
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
