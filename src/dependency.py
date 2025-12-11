from starlette.requests import Request


def get_redis_client(request: Request):
    return request.app.state.redis_client
