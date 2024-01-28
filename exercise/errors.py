class CoreError(Exception):
    pass


class ErrorDeviceAlreadyExists(CoreError):
    pass


class ErrorDeviceNotFound(CoreError):
    pass

class ErrorJobAlreadyExists(CoreError):
    pass

