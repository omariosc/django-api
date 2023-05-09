"""This file contains helper functions."""


def get_param(param, request):
    """Gets a parameter from the request.

    Args:
        param (str): The parameter to get.
        request (Request): The request object.

    Returns:
        str: The parameter value.
    """

    query = request.query_params.get(param)
    return query if query else request.data.get(param)
