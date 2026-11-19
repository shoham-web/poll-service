
class VoteNotFoundError(Exception):
    pass


class VoteAlreadyExistsError(Exception):
    pass


class UserNotRegisteredError(Exception):
    pass


class VoteAccessDeniedError(Exception):
    pass
