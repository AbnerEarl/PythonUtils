from wsgiref.simple_server import make_server


def app(env, start_response):
    start_response("200 ok", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"test_one"]


class App:
    def __init__(self, env, start_response):
        self.e = env
        self.sr = start_response

    def __iter__(self):
        self.sr("200 ok", [("Content-Type", "text/plain; charset=utf-8")])
        yield b"test_two"


class Application:
    def __call__(self, env, start_response, *args, **kwargs):
        start_response("200 ok", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"test_three"]


# ws = make_server("127.0.0.1", 9999, app=app)
# ws = make_server("127.0.0.1", 9999, app=App)
ws = make_server("127.0.0.1", 9999, app=Application())
ws.serve_forever()
