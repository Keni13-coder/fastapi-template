from .response_generator import generator_response
from .responses_data import ResponsesError

login_responses = generator_response.create_responses_for_point(
    ResponsesError.server_500.value,
    ResponsesError.auth_403.value
)
register_responses = generator_response.create_responses_for_point(
    ResponsesError.server_500.value,
    ResponsesError.register_400.value,
)