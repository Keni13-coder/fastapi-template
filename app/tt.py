from uuid import UUID


data_1 = {
    "sub": "8433f330-ef62-406a-9ef4-34ced4de755f",
    "iat": 1714418935,
    "exp": 1714418935,
    "device_id": "80f2a603-e359-4eb3-bb39-0026ce96b96e",
}
data_2 = {
    "sub": UUID("8433f330-ef62-406a-9ef4-34ced4de755f"),
    "device_id": UUID("80f2a603-e359-4eb3-bb39-0026ce96b96e"),
    "iat": 1714418939,
}


class TestATTR:
    device_id = "80f2a603-e359-4eb3-bb39-0026ce96b96e"
    user_id = "8433f330-ef62-406a-9ef4-34ced4de755f"
    iat = 1714418939


match data_1:
    case {
        "sub": TestATTR.user_id,
        "device_id": TestATTR.device_id,
        "iat": TestATTR.iat,
    }:
        print("ok")
    case _:
        print("Don ok")
