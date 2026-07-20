import hashlib
import hmac
import json
from unittest.mock import patch
from urllib.error import URLError

from jwt import PyJWK
from jwt.algorithms import HMACAlgorithm
from jwt.api_jws import PyJWS
from jwt.exceptions import (
    DecodeError,
    InvalidAlgorithmError,
    InvalidKeyError,
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)
from jwt.jwks_client import PyJWKClient
from jwt.utils import base64url_encode


def require_exception(expected_type, action, message_fragment=None):
    try:
        action()
    except expected_type as exc:
        if message_fragment is not None:
            assert message_fragment.lower() in str(exc).lower(), str(exc)
        return exc
    except Exception as exc:
        raise AssertionError(
            f"Expected {expected_type.__name__}, received "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    raise AssertionError(f"Expected {expected_type.__name__}, but no exception occurred")


def test_c001_rejects_raw_jwk_json_as_hmac_secret():
    algorithm = HMACAlgorithm(hashlib.sha256)
    raw_jwk = json.dumps(
        {
            "kty": "oct",
            "k": "c2VjcmV0",
            "alg": "HS256",
        }
    )

    require_exception(
        InvalidKeyError,
        lambda: algorithm.prepare_key(raw_jwk),
        "looks like a JWK",
    )


def test_c001_preserves_normal_hmac_secret_use():
    algorithm = HMACAlgorithm(hashlib.sha256)
    assert algorithm.prepare_key("ordinary-secret") == b"ordinary-secret"


def test_c002_rejects_token_algorithm_mismatched_to_pyjwk():
    secret = b"reviewer-generated-secret-material-32-bytes-minimum"
    token = PyJWS().encode(
        b'{"sub":"review"}',
        secret,
        algorithm="HS256",
    )

    key = PyJWK(
        {
            "kty": "oct",
            "k": base64url_encode(secret).decode(),
            "alg": "HS512",
        }
    )

    require_exception(
        InvalidAlgorithmError,
        lambda: PyJWS().decode(
            token,
            key,
            algorithms=["HS256", "HS512"],
        ),
        "does not match",
    )


def test_c003_rejects_non_http_uri_schemes():
    rejected_uris = [
        "file:///etc/passwd",
        "ftp://example.org/keys.json",
        'data:application/json,{"keys":[]}',
        "ldap://internal.example/jwks",
        "/local/path/to/jwks.json",
    ]

    for uri in rejected_uris:
        require_exception(
            PyJWKClientError,
            lambda uri=uri: PyJWKClient(uri),
            "Invalid JWKS URI scheme",
        )


def test_c003_accepts_http_and_https_uri_schemes():
    PyJWKClient("http://localhost/jwks.json")
    PyJWKClient("https://example.test/jwks.json")
    PyJWKClient("HTTPS://Example.Test/jwks.json")


def test_c004_preserves_cached_jwk_set_after_fetch_failure():
    client = PyJWKClient("https://example.test/jwks.json")

    assert client.jwk_set_cache is not None

    original = {
        "keys": [
            {
                "kty": "oct",
                "k": "c2VjcmV0",
                "alg": "HS256",
                "kid": "review-key",
            }
        ]
    }
    client.jwk_set_cache.put(original)

    with patch(
        "jwt.jwks_client.urllib.request.urlopen",
        side_effect=URLError("reviewer-generated outage"),
    ):
        require_exception(
            PyJWKClientConnectionError,
            client.fetch_data,
            "Fail to fetch data",
        )

    preserved = client.jwk_set_cache.get()
    assert preserved == original


def make_b64_false_token(payload, middle_segment):
    secret = b"reviewer-generated-secret-material-32-bytes-minimum"
    header = {
        "typ": "JWT",
        "alg": "HS256",
        "b64": False,
        "crit": ["b64"],
    }
    header_segment = base64url_encode(
        json.dumps(header, separators=(",", ":")).encode()
    )
    signing_input = b".".join([header_segment, payload])
    signature = hmac.new(secret, signing_input, hashlib.sha256).digest()

    token = b".".join(
        [header_segment, middle_segment, base64url_encode(signature)]
    ).decode()

    return token, secret


def test_c005_rejects_nonempty_compact_payload_when_b64_false():
    payload = b"detached-review-payload"
    token, secret = make_b64_false_token(
        payload,
        b"A" * 4096,
    )

    require_exception(
        DecodeError,
        lambda: PyJWS().decode(
            token,
            secret,
            algorithms=["HS256"],
            detached_payload=payload,
        ),
        "Payload segment must be empty",
    )


def test_c005_requires_b64_to_be_declared_critical():
    secret = b"reviewer-generated-secret-material-32-bytes-minimum"
    payload = b"detached-review-payload"
    header = {
        "typ": "JWT",
        "alg": "HS256",
        "b64": False,
    }
    header_segment = base64url_encode(
        json.dumps(header, separators=(",", ":")).encode()
    )
    signing_input = b".".join([header_segment, payload])
    signature = hmac.new(secret, signing_input, hashlib.sha256).digest()
    token = b".".join(
        [header_segment, b"", base64url_encode(signature)]
    ).decode()

    require_exception(
        InvalidTokenError,
        lambda: PyJWS().decode(
            token,
            secret,
            algorithms=["HS256"],
            detached_payload=payload,
        ),
        "crit",
    )


TESTS = [
    test_c001_rejects_raw_jwk_json_as_hmac_secret,
    test_c001_preserves_normal_hmac_secret_use,
    test_c002_rejects_token_algorithm_mismatched_to_pyjwk,
    test_c003_rejects_non_http_uri_schemes,
    test_c003_accepts_http_and_https_uri_schemes,
    test_c004_preserves_cached_jwk_set_after_fetch_failure,
    test_c005_rejects_nonempty_compact_payload_when_b64_false,
    test_c005_requires_b64_to_be_declared_critical,
]


if __name__ == "__main__":
    failures = []

    for test in TESTS:
        try:
            test()
        except Exception as exc:
            failures.append((test.__name__, exc))
            print(f"FAIL: {test.__name__}: {type(exc).__name__}: {exc}")
        else:
            print(f"PASS: {test.__name__}")

    print()
    print(f"Executed: {len(TESTS)}")
    print(f"Passed: {len(TESTS) - len(failures)}")
    print(f"Failed: {len(failures)}")

    if failures:
        raise SystemExit(1)

    print("Independent reviewer counterexamples: PASS")
