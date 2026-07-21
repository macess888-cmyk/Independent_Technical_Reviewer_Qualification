from __future__ import annotations

import argparse
import importlib
import json
import sys
import threading
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterator


REDIRECT_STATUSES = (301, 302, 303, 307, 308)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    description: str
    observed_cookie: str | None
    observed_authorization: str | None
    observed_control: str | None
    response_status: int
    expected_cookie_forwarded: bool
    expected_authorization_forwarded: bool
    expected_control_forwarded: bool
    cookie_expectation_met: bool
    authorization_expectation_met: bool
    control_expectation_met: bool
    classification: str


class QuietHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: Any) -> None:
        return


class CaptureHandler(QuietHandler):
    captured_headers: dict[str, str] = {}

    def do_GET(self) -> None:
        type(self).captured_headers = {
            key: value for key, value in self.headers.items()
        }

        body = json.dumps(type(self).captured_headers).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_redirect_handler(
    location: str,
    status: int,
) -> type[QuietHandler]:
    class RedirectHandler(QuietHandler):
        def do_GET(self) -> None:
            self.send_response(status)
            self.send_header("Location", location)
            self.send_header("Content-Length", "0")
            self.end_headers()

    return RedirectHandler


def make_same_origin_handler(
    status: int,
) -> type[QuietHandler]:
    class SameOriginHandler(QuietHandler):
        captured_headers: dict[str, str] = {}

        def do_GET(self) -> None:
            if self.path.startswith("/redirect"):
                self.send_response(status)
                self.send_header("Location", "/capture")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

            type(self).captured_headers = {
                key: value for key, value in self.headers.items()
            }
            body = json.dumps(type(self).captured_headers).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return SameOriginHandler


def make_multihop_handler(
    second_url: str,
) -> type[QuietHandler]:
    class MultiHopHandler(QuietHandler):
        def do_GET(self) -> None:
            self.send_response(302)
            self.send_header("Location", second_url)
            self.send_header("Content-Length", "0")
            self.end_headers()

    return MultiHopHandler


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


def get_header(headers: dict[str, str], name: str) -> str | None:
    target = name.lower()

    for key, value in headers.items():
        if key.lower() == target:
            return value

    return None


def load_urllib3(package_path: Path, expected_version: str):
    resolved = package_path.resolve()

    if not resolved.exists():
        raise FileNotFoundError(f"Missing package path: {resolved}")

    for module_name in tuple(sys.modules):
        if module_name == "urllib3" or module_name.startswith("urllib3."):
            del sys.modules[module_name]

    sys.path.insert(0, str(resolved))

    try:
        urllib3 = importlib.import_module("urllib3")
    finally:
        sys.path.remove(str(resolved))

    if urllib3.__version__ != expected_version:
        raise RuntimeError(
            f"Expected urllib3 {expected_version}, imported "
            f"{urllib3.__version__} from {urllib3.__file__}"
        )

    return urllib3


def evaluate_case(
    *,
    case_id: str,
    description: str,
    captured_headers: dict[str, str],
    response_status: int,
    expected_cookie_forwarded: bool,
    expected_authorization_forwarded: bool,
    expected_control_forwarded: bool,
) -> CaseResult:
    cookie = get_header(captured_headers, "Cookie")
    authorization = get_header(captured_headers, "Authorization")
    control = get_header(captured_headers, "X-Review-Control")

    cookie_met = (cookie is not None) == expected_cookie_forwarded
    authorization_met = (
        authorization is not None
    ) == expected_authorization_forwarded
    control_met = (control is not None) == expected_control_forwarded

    classification = (
        "PASS"
        if cookie_met and authorization_met and control_met
        else "FAIL"
    )

    return CaseResult(
        case_id=case_id,
        description=description,
        observed_cookie=cookie,
        observed_authorization=authorization,
        observed_control=control,
        response_status=response_status,
        expected_cookie_forwarded=expected_cookie_forwarded,
        expected_authorization_forwarded=expected_authorization_forwarded,
        expected_control_forwarded=expected_control_forwarded,
        cookie_expectation_met=cookie_met,
        authorization_expectation_met=authorization_met,
        control_expectation_met=control_met,
        classification=classification,
    )


def run_cross_origin_case(
    urllib3,
    *,
    version: str,
    status: int,
    cookie_header_name: str = "Cookie",
    cookie_value: str = "review_session=secret-value",
    retries=None,
) -> CaseResult:
    CaptureHandler.captured_headers = {}

    with running_server(CaptureHandler) as destination:
        destination_url = (
            f"http://127.0.0.1:{destination.server_port}/capture"
        )
        redirect_handler = make_redirect_handler(destination_url, status)

        with running_server(redirect_handler) as redirect:
            initial_url = (
                f"http://localhost:{redirect.server_port}/redirect"
            )
            manager = urllib3.PoolManager()
            response = manager.request(
                "GET",
                initial_url,
                headers={
                    cookie_header_name: cookie_value,
                    "Authorization": "Bearer review-token",
                    "X-Review-Control": "preserve-me",
                },
                redirect=True,
                retries=retries,
            )

    fixed = version == "2.0.6"
    custom_preserve = retries is not None

    return evaluate_case(
        case_id=f"cross_origin_{status}_{cookie_header_name}",
        description=(
            f"Cross-origin {status} redirect using "
            f"{cookie_header_name} header"
        ),
        captured_headers=CaptureHandler.captured_headers,
        response_status=response.status,
        expected_cookie_forwarded=not fixed or custom_preserve,
        expected_authorization_forwarded=custom_preserve,
        expected_control_forwarded=True,
    )


def run_same_origin_case(
    urllib3,
    *,
    status: int,
) -> CaseResult:
    handler = make_same_origin_handler(status)

    with running_server(handler) as server:
        url = f"http://127.0.0.1:{server.server_port}/redirect"
        manager = urllib3.PoolManager()
        response = manager.request(
            "GET",
            url,
            headers={
                "Cookie": "review_session=secret-value",
                "Authorization": "Bearer review-token",
                "X-Review-Control": "preserve-me",
            },
            redirect=True,
        )

    return evaluate_case(
        case_id=f"same_origin_{status}",
        description=f"Same-origin {status} redirect",
        captured_headers=handler.captured_headers,
        response_status=response.status,
        expected_cookie_forwarded=True,
        expected_authorization_forwarded=True,
        expected_control_forwarded=True,
    )


def run_redirect_disabled_case(urllib3) -> CaseResult:
    CaptureHandler.captured_headers = {}

    with running_server(CaptureHandler) as destination:
        destination_url = (
            f"http://127.0.0.1:{destination.server_port}/capture"
        )
        redirect_handler = make_redirect_handler(destination_url, 302)

        with running_server(redirect_handler) as redirect:
            initial_url = (
                f"http://localhost:{redirect.server_port}/redirect"
            )
            manager = urllib3.PoolManager()
            response = manager.request(
                "GET",
                initial_url,
                headers={
                    "Cookie": "review_session=secret-value",
                    "Authorization": "Bearer review-token",
                    "X-Review-Control": "preserve-me",
                },
                redirect=False,
            )

    return evaluate_case(
        case_id="redirect_disabled",
        description="Redirect disabled control",
        captured_headers=CaptureHandler.captured_headers,
        response_status=response.status,
        expected_cookie_forwarded=False,
        expected_authorization_forwarded=False,
        expected_control_forwarded=False,
    )


def run_multihop_case(urllib3, *, version: str) -> CaseResult:
    CaptureHandler.captured_headers = {}

    with running_server(CaptureHandler) as destination:
        destination_url = (
            f"http://127.0.0.1:{destination.server_port}/capture"
        )

        second_handler = make_redirect_handler(destination_url, 302)
        with running_server(second_handler) as second:
            second_url = (
                f"http://127.0.0.1:{second.server_port}/second"
            )
            first_handler = make_multihop_handler(second_url)

            with running_server(first_handler) as first:
                initial_url = (
                    f"http://localhost:{first.server_port}/first"
                )
                manager = urllib3.PoolManager()
                response = manager.request(
                    "GET",
                    initial_url,
                    headers={
                        "Cookie": "review_session=secret-value",
                        "Authorization": "Bearer review-token",
                        "X-Review-Control": "preserve-me",
                    },
                    redirect=True,
                )

    fixed = version == "2.0.6"

    return evaluate_case(
        case_id="multiple_redirect_hops",
        description="Two-hop cross-origin redirect",
        captured_headers=CaptureHandler.captured_headers,
        response_status=response.status,
        expected_cookie_forwarded=not fixed,
        expected_authorization_forwarded=False,
        expected_control_forwarded=True,
    )


def run_matrix(package_path: Path, expected_version: str) -> dict[str, Any]:
    urllib3 = load_urllib3(package_path, expected_version)
    retry_class = urllib3.util.Retry

    results: list[CaseResult] = []

    for status in REDIRECT_STATUSES:
        results.append(
            run_cross_origin_case(
                urllib3,
                version=expected_version,
                status=status,
            )
        )

    results.append(
        run_cross_origin_case(
            urllib3,
            version=expected_version,
            status=302,
            cookie_header_name="cOoKiE",
        )
    )

    for status in REDIRECT_STATUSES:
        results.append(
            run_same_origin_case(
                urllib3,
                status=status,
            )
        )

    results.append(run_redirect_disabled_case(urllib3))

    results.append(
        run_cross_origin_case(
            urllib3,
            version=expected_version,
            status=302,
            cookie_value="",
        )
    )

    results.append(run_multihop_case(urllib3, version=expected_version))

    results.append(
        run_cross_origin_case(
            urllib3,
            version=expected_version,
            status=302,
            retries=retry_class(
                total=3,
                redirect=3,
                remove_headers_on_redirect=[],
            ),
        )
    )

    passed = sum(result.classification == "PASS" for result in results)
    failed = len(results) - passed

    return {
        "version": urllib3.__version__,
        "module_path": str(Path(urllib3.__file__).resolve()),
        "case_count": len(results),
        "passed": passed,
        "failed": failed,
        "overall_classification": "PASS" if failed == 0 else "FAIL",
        "results": [asdict(result) for result in results],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-path", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        payload = run_matrix(
            Path(args.package_path),
            args.expected_version,
        )
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "version": payload["version"],
                "case_count": payload["case_count"],
                "passed": payload["passed"],
                "failed": payload["failed"],
                "overall_classification": payload[
                    "overall_classification"
                ],
                "output": str(output_path),
            },
            indent=2,
            sort_keys=True,
        )
    )

    return 0 if payload["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())