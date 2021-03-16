# -*- coding: utf-8 -*-

import base64
import json
import logging
import sys
import traceback
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


def execute_code(code: str, code_input: str = "") -> str:
    """Executes Python code and collects its output"""

    if not code_input.endswith("\n"):
        code_input += "\n"
    input_buffer = StringIO()
    input_buffer.write(code_input)
    input_buffer.seek(0)
    sys.stdin = input_buffer

    output_buffer = StringIO()
    sys.stdout = output_buffer
    sys.stderr = output_buffer

    try:
        exec(code, {})
    except Exception as e:
        traceback.print_exc()
    output = output_buffer.getvalue()

    # Restore the original stdin and stdout
    sys.stdin = sys.__stdin__
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
    request_body: bytes = environ["wsgi.input"].read(request_body_size)

    request_obj: dict = json.loads(request_body)
    source = request_obj.get("source", "")
    code_input = request_obj.get("input", "")

    config_matplotlib()

    logging.info(request_body)
    output = execute_code(source, code_input)
    logging.info(output)

    # Construct response
    status = "200 OK"
    response_headers = [("Content-type", "application/json")]
    start_response(status, response_headers)
    return [json.dumps(output).encode()]
