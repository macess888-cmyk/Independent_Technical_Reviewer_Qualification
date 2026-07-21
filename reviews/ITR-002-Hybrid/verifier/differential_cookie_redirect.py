from __future__ import annotations

import argparse
import json
import sys
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterator


class QuietHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


class DestinationHandler(QuietHandler):
    received_headers: dict[str, str] = {}

    def do_GET(self) -> None:
        type(self).received_headers = {
            key: value for key, value in self.headers.items()
        }

        body = json.dumps(type(self).received_headers).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_redirect_handler(destination_url: str) -> type[QuietHandler]:
    class RedirectHandler(QuietHandler):
        def do_GET(self) -> None:
            self.send_response(302)
            self.send_header("Location", destination_url)
            self.send_header("Content-Length", "0")
            self.end_headers()

    return RedirectHandler


@contextmanager
def running_server(
    handler: type[BaseHTTPRequestHandler],
) -> Iterator[ThreadingHTTPServer]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def header_value(headers: dict[str, str], name: str) -> str | None:
    expected = name.lower()

    for key, value in headers.items():
        if key.lower() == expected:
            return value

    return None


def run_probe(package_path: Path, expected_version: str) -> dict[str, Any]:
    resolved_package_path = package_path.resolve()

    if not resolved_package_path.exists():
        raise FileNotFoundError(
            f"Package directory does not exist: {resolved_package_path}"
        )

    sys.path.insert(0, str(resolved_package_path))

    import urllib3  # noqa: PLC0415

    if urllib3.__version__ != expected_version:
        raise RuntimeError(
            f"Expected urllib3 {expected_version}, imported "
            f"{urllib3.__version__} from {urllib3.__file__}"
        )

    DestinationHandler.received_headers = {}

    with running_server(DestinationHandler) as destination_server:
        destination_url = (
            f"http://127.0.0.1:{destination_server.server_port}/capture"
        )
        redirect_handler = make_redirect_handler(destination_url)

        with running_server(redirect_handler) as redirect_server:
            # localhost and 127.0.0.1 are deliberately different origins.
            initial_url = (
                f"http://localhost:{redirect_server.server_port}/redirect"
            )

            manager = urllib3.PoolManager()
            response = manager.request(
                "GET",
                initial_url,
                headers={
                    "Cookie": "review_session=secret-value",
                    "X-Review-Control": "preserve-me",
                },
                redirect=True,
            )

    received = DestinationHandler.received_headers
    cookie = header_value(received, "Cookie")
    control = header_value(received, "X-Review-Control")

    return {
        "version": urllib3.__version__,
        "module_path": str(Path(urllib3.__file__).resolve()),
        "initial_url": initial_url,
        "destination_url": destination_url,
        "response_status": response.status,
        "cookie_received": cookie,
        "cookie_forwarded": cookie is not None,
        "control_header_received": control,
        "control_header_preserved": control == "preserve-me",
        "received_headers": received,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-path", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        result = run_probe(
            package_path=Path(args.package_path),
            expected_version=args.expected_version,
        )
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())