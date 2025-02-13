import logging

_LOGGER_DEFAULT = logging.getLogger("Default")


# https://blog.stackademic.com/understanding-python-decorators-a-guide-to-using-class-decorators-7327c9b42916
def log_methods(cls, logger=None):
    if logger is None:
        logger = _LOGGER_DEFAULT
    for name, value in vars(cls).items():
        if callable(value):
            setattr(cls, name, log_method(logger, value))
    return cls


def log_method(logger, func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling method: '{func.__name__}' with '{len(args)}' args")
        return func(*args, **kwargs)

    return wrapper
