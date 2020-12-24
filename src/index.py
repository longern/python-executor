# -*- coding: utf-8 -*-

import base64
import logging
import sys
from io import BytesIO, StringIO


def config_matplotlib():
    def show_to_screen():
        figure_buffer = BytesIO()
        plt.savefig(figure_buffer, format="png")
        figure_base64 = base64.b64encode(figure_buffer.getvalue())
        print("data:image/png;base64," + figure_base64.decode())

    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    plt.show = show_to_screen


def execute_code(code: str) -> bytes:
    """Executes Python code and collects its output"""

    buffer = StringIO()
    sys.stdout = buffer
    sys.stderr = buffer

    exec(code, {})
    output = buffer.getvalue().encode()

    # Restore the original stdout
    sys.stdout = sys.__stdout__
    sys.stdout = sys.__stderr__

    return output


def handler(environ, start_response):
    context = environ["fc.context"]
    request_uri = environ["fc.request_uri"]

    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0
    request_body = environ["wsgi.input"].read(request_body_size)

    config_matplotlib()

    logging.info(request_body)
    output = execute_code(request_body)
    logging.info(output)

    # Construct response
    status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(status, response_headers)
    return [output]
