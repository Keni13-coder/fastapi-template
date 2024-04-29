from pydantic import BaseModel


def create_responses_for_point(*responses: BaseModel):
    create_data = dict()
    for response in responses:
        create_data.update(response.model_dump())
    return create_data
