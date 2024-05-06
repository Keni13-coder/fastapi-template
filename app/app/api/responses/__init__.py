from .response_generator import generator_response
from .responses_data import ResponsesError

login_responses: dict = generator_response.create_responses_for_point(
    ResponsesError.server_500.value,
    ResponsesError.auth_403.value
)
register_responses: dict = generator_response.create_responses_for_point(
    ResponsesError.server_500.value,
    ResponsesError.register_400.value,
)
current_user_responses: dict = generator_response.create_responses_for_point(
    ResponsesError.server_500.value,
    ResponsesError.not_auth_401.value,
    ResponsesError.invalid_token_403.value
)
refresh_responses: dict = generator_response.create_responses_for_point(
    ResponsesError.not_found_400.value,
    ResponsesError.expired_token_403.value
)
refresh_responses.update(current_user_responses)

logout_responses = current_user_responses.copy()
