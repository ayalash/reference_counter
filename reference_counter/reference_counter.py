import sys
import logbook
import itertools

from ._compat import reraise
from .exceptions import InvalidReferenceCount

_logger = logbook.Logger(__name__)


class ReferenceCounter(object):
    def __init__(self):
        super(ReferenceCounter, self).__init__()
        self._reference = 0
        self._depends_on = []
        self._zero_refcount_callbacks = []

    def add_zero_refcount_callback(self, callback):
        self._zero_refcount_callbacks.append(lambda: callback(self))

    def add_reference(self):
        self._reference += 1
        if self._reference == 1:
            for dep in self._depends_on:
                dep.add_reference()

    def depend_on_counter(self, counter):
        if self._reference > 0:
            counter.add_reference()
        self._depends_on.append(counter)

    def remove_reference(self):
        if self._reference <= 0:
            raise InvalidReferenceCount(self)

        self._reference -= 1
        if self._reference == 0:
            _logger.debug("Last reference dropped for {0!r}", self)
            thrown = None
            for callback in itertools.chain(
                    self._zero_refcount_callbacks,
                    (ref_count.remove_reference for ref_count in reversed(self._depends_on)),
                    ):
                try:
                    callback()
                except BaseException:
                    _logger.debug("Exception caught during remove_reference", exc_info=True)
                    if thrown is None:
                        thrown = sys.exc_info()
            if thrown is not None:
                reraise(*thrown)

    def get_reference_count(self):
        return self._reference
