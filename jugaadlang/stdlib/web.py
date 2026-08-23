"""
web — JugaadLang Web client requests and micro web framework (JugaadWeb).
"""

from __future__ import annotations

import json
from types import FunctionType
from typing import Any, Callable

import requests

# Re-export client requests
get = requests.get
post = requests.post
put = requests.put
delete = requests.delete

# Global request query params and body dictionary
params: dict[str, Any] = {}
body: dict[str, Any] = {}


class JugaadWeb:
    """
    JugaadWeb — The official micro web framework for JugaadLang.
    Wraps Flask if available, falls back to Python's standard http.server otherwise.
    """

    def __init__(self) -> None:
        self.routes: dict[str, tuple[Callable, list[str]]] = {}
        try:
            from flask import Flask

            self.flask_app = Flask("JugaadWeb")
        except ImportError:
            self.flask_app = None

    def route(self, path: str, methods: list[str] = ["GET"]) -> Callable:
        """Register a route decorator."""

        def decorator(func: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                global params, body
                if self.flask_app:
                    from flask import has_request_context

                    if has_request_context():
                        from flask import request as flask_request

                        # Populate query params
                        params = dict(flask_request.args)
                        # Populate body
                        body = {}
                        if flask_request.is_json:
                            body = dict(flask_request.json or {})
                        elif flask_request.form:
                            body = dict(flask_request.form)
                        elif flask_request.data:
                            try:
                                body = json.loads(flask_request.data.decode("utf-8"))
                            except Exception:
                                pass

                res = func(*args, **kwargs)

                # Auto-serialize returned dictionary or list response to JSON
                if isinstance(res, (dict, list)):
                    from flask import has_request_context

                    if self.flask_app and has_request_context():
                        from flask import jsonify

                        return jsonify(res)
                    else:
                        return json.dumps(res)
                return res

            # Update wrapper function name for Flask compatibility
            if isinstance(func, FunctionType):
                wrapper.__name__ = func.__name__

            self.routes[path] = (wrapper, methods)
            if self.flask_app:
                # Register wrapper in Flask
                func_name = func.__name__ if isinstance(func, FunctionType) else str(id(func))
                self.flask_app.add_url_rule(path, func_name, wrapper, methods=methods)
            return wrapper

        return decorator

    def run(self, port: int = 5000, host: str = "127.0.0.1") -> None:
        """Start the web server."""
        if self.flask_app:
            print(f"🚀 JugaadWeb is running on http://{host}:{port} using Flask backend!")
            self.flask_app.run(host=host, port=port, debug=False)
        else:
            print("⚠️ Flask is not installed. Falling back to basic Python http.server.")
            print(
                "💡 Tip: Install Flask for full web features: `jug install web` or `pip install flask`.\n"
            )
            print(f"🚀 JugaadWeb running on http://{host}:{port}...")

            from http.server import BaseHTTPRequestHandler, HTTPServer
            from urllib.parse import parse_qs, urlparse

            # Save self reference for handler
            routes_map = self.routes

            class JugaadHTTPHandler(BaseHTTPRequestHandler):
                def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
                    # Suppress default server logs for cleaner output
                    pass

                def handle_http(self, method: str) -> None:
                    parsed_url = urlparse(self.path)
                    route_path = parsed_url.path

                    func_tuple = routes_map.get(route_path)
                    if func_tuple and method in func_tuple[1]:
                        try:
                            global params, body
                            # Parse query params
                            params = {
                                k: v[0] if len(v) == 1 else v
                                for k, v in parse_qs(parsed_url.query).items()
                            }

                            # Parse request body
                            body = {}
                            content_length = int(self.headers.get("Content-Length", 0))
                            if content_length > 0:
                                raw_data = self.rfile.read(content_length).decode("utf-8")
                                try:
                                    body = json.loads(raw_data)
                                except Exception:
                                    body = {
                                        k: v[0] if len(v) == 1 else v
                                        for k, v in parse_qs(raw_data).items()
                                    }

                            res = func_tuple[0]()

                            self.send_response(200)
                            if isinstance(res, str) and (
                                res.startswith("{") or res.startswith("[")
                            ):
                                self.send_header("Content-type", "application/json; charset=utf-8")
                            else:
                                self.send_header("Content-type", "text/html; charset=utf-8")
                            self.end_headers()
                            self.wfile.write(str(res).encode("utf-8"))
                        except Exception as e:
                            self.send_response(500)
                            self.end_headers()
                            self.wfile.write(f"Server error: {e}".encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(b"404 - Route gayab ho gaya!")

                def do_GET(self) -> None:
                    self.handle_http("GET")

                def do_POST(self) -> None:
                    self.handle_http("POST")

                def do_PUT(self) -> None:
                    self.handle_http("PUT")

                def do_DELETE(self) -> None:
                    self.handle_http("DELETE")

            server = HTTPServer((host, port), JugaadHTTPHandler)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Server stopped.")
                server.server_close()


# Global default app instance
_default_app = JugaadWeb()


def agar_route(path: str, methods: list[str] = ["GET"]) -> Callable:
    """Decorator to register a route on the default global app."""
    return _default_app.route(path, methods)


def chalao(port: int = 5000, host: str = "127.0.0.1") -> None:
    """Start the default global app web server."""
    _default_app.run(port=port, host=host)
