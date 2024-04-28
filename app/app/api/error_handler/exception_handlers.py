from .error_500 import server_error

exception_handlers = {
    500: server_error,
}
