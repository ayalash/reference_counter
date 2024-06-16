import pytest
import logbook

from reference_counter import ReferenceCounter


@pytest.fixture(autouse=True)
def redirect_logs(request):
    handler = logbook.StderrHandler()
    handler.push_application()
    request.addfinalizer(handler.pop_application)


def _get_ref_counter():
    counter = ReferenceCounter()
    assert counter.get_reference_count() == 0
    return counter

@pytest.fixture
def ref_count(request):
    return _get_ref_counter()


@pytest.fixture
def primary_counter(ref_count):
    return ref_count


@pytest.fixture
def secondary_counter(request, primary_counter, ref_count):
    deps = _get_ref_counter()
    assert primary_counter != deps
    primary_counter.depend_on_counter(deps)
    return deps


class Callbacks(object):
    def __init__(self):
        self._callbacks = []

    def __call__(self, ref_count):
        self._callbacks.append(ref_count)

    def was_called(self):
        return bool(self._callbacks)

    def assert_expected(self, *expected_ref_counters):
        assert self._callbacks == list(expected_ref_counters)


@pytest.fixture
def callbacks(request):
    callbacks = Callbacks()
    assert not callbacks.was_called()
    return callbacks
