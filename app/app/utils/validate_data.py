from typing import Any, Type, Union, Sequence

from fastapi import HTTPException

def data_or_error(
    data: Any,
    error: Union[Type[Exception], Type[HTTPException]],
    params: Sequence = (),
    key_params: dict[str, Any] = {}
    ):
    '''
    :param data: Переданные данные для проверки существования
    :type data: Any
    :param error: Передать объект класса предположительной ошибки
    :type error: Exception, HTTPException для вывода на поинт
    :param params: передаваемые последовательные параметры, в класс ошибки для иницилизации
    :type params: Sequence
    :default params: ()
    :param key_params: передаваемые ключивые параметры в класс ошибки для иницилизации
    :type key_params: dict[str, Any]
    :default key_params: {}
    '''
    try:
        assert data
        return data
    except AssertionError:
        raise error(*params, **key_params)