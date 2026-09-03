import functools

from starlette.concurrency import run_in_threadpool


class _Compute:
    """Descriptor wrapping a CPU-bound function. Sync callers call it
    directly - fine from a sync route, since FastAPI already runs those in
    a threadpool. Async callers must explicitly await .async_(...), which
    routes the call through a threadpool so the event loop isn't blocked.
    Nothing prevents an async caller from calling it directly instead -
    that would block the loop; there's no lint rule for this, it's a
    review-time convention.

    Implemented as a descriptor (not a plain function attribute) so that
    `instance.method.async_(...)` binds `self` correctly for instance
    methods, same as `instance.method(...)` does.
    """

    def __init__(self, fn):
        functools.update_wrapper(self, fn)
        self._fn = fn

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        bound_fn = self._fn.__get__(obj, objtype)
        return _BoundCompute(bound_fn)

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

    async def async_(self, *args, **kwargs):
        return await run_in_threadpool(self._fn, *args, **kwargs)


class _BoundCompute:

    def __init__(self, bound_fn):
        self._bound_fn = bound_fn

    def __call__(self, *args, **kwargs):
        return self._bound_fn(*args, **kwargs)

    async def async_(self, *args, **kwargs):
        return await run_in_threadpool(self._bound_fn, *args, **kwargs)


def compute(fn):
    return _Compute(fn)
