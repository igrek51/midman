import re
from typing import Tuple, Optional

from nuclear.sublog import log

from xman.cache import sorted_dict_trait
from xman.config import Config
from xman.request import HttpRequest
from xman.response import HttpResponse


def transform_request(request: HttpRequest) -> HttpRequest:
    """Transforms each incoming Request before further processing (caching, forwarding)."""
    match = re.match(r'^/some/path/(.+?)(/[a-z]+)(/.*)', request.path)
    if match:
        request.path = match.expand(r'\3')
        log.debug('request path transformed', path=request.path)
    return request


def immediate_responder(request: HttpRequest) -> Optional[HttpResponse]:
    """Returns immediate response for matched request instead of proxying it further or searching in cache"""
    if request.path.startswith('/some/api'):
        return HttpResponse(status_code=200, headers={'Content-Type': 'application/json'}, content=''.encode())
    return None


def transform_response(request: HttpRequest, response: HttpResponse) -> HttpResponse:
    """Transforms each Response before sending it."""
    if request.path.startswith('/some/api'):
        log.debug('Found Ya', path=request.path)
        response = response.set_content('{"payload": "anythingyouwish"}"')
    return response


def can_be_cached(request: HttpRequest, response: HttpResponse) -> bool:
    """Indicates whether particular request with response could be saved in cache."""
    return response.status_code == 200


def cache_request_traits(request: HttpRequest) -> Tuple:
    """Gets tuple denoting request uniqueness. Requests with same results are treated as the same when caching."""
    if request.path.endswith('/some/path'):
        return request.method, request.path, sorted_dict_trait(request.headers)
    return request.method, request.path, request.content


def override_config(config: Config):
    """Overrides default parameters in config."""
    # config.listen_port = 8080
    # config.listen_ssl = True
    # config.dst_url = 'http://127.0.0.1:8000'
    # config.record = False
    # config.record_file = 'tape.json'
    # config.replay = False
    # config.replay_throttle = False
    # config.replay_clear_cache = False
    # config.replay_clear_cache_seconds = 60
    # config.allow_chunking = True
    # config.proxy_timeout = 10
    config.verbose = 0
