import json


def format_sse(
    event: str,
    data
):

    return (

        f"event: {event}\n"

        f"data: {json.dumps(data)}\n\n"

    )