import pytest
from reference_counter import InvalidReferenceCount


def test_get_reference_counter(ref_count):
    ref_count.add_reference()
    assert ref_count.get_reference_count() == 1

    ref_count.remove_reference()
    assert ref_count.get_reference_count() == 0


def test_removing_reference_to_zero_counter(ref_count):
    assert ref_count.get_reference_count() == 0
    with pytest.raises(InvalidReferenceCount) as caught:
        ref_count.remove_reference()
    assert ref_count is caught.value.args[0]
    assert ref_count.get_reference_count() == 0


def test_depend_on_counter(primary_counter, secondary_counter):
    primary_counter.add_reference()
    assert primary_counter.get_reference_count() == 1
    assert secondary_counter.get_reference_count() == 1

    primary_counter.add_reference()
    assert primary_counter.get_reference_count() == 2
    assert secondary_counter.get_reference_count() == 1

    primary_counter.remove_reference()
    assert primary_counter.get_reference_count() == 1
    assert secondary_counter.get_reference_count() == 1

    primary_counter.remove_reference()
    assert primary_counter.get_reference_count() == 0
    assert secondary_counter.get_reference_count() == 0


def test_add_zero_refcount_callback(ref_count, callbacks):
    ref_count.add_zero_refcount_callback(callbacks)
    ref_count.add_reference()
    assert not callbacks.was_called()
    ref_count.remove_reference()
    callbacks.assert_expected(ref_count)


def test_mixing_zero_refcount_callbacks_with_depend_on_counter(primary_counter, secondary_counter, callbacks):
    primary_counter.add_zero_refcount_callback(callbacks)
    secondary_counter.add_zero_refcount_callback(callbacks)

    primary_counter.add_reference()
    assert not callbacks.was_called()
    primary_counter.remove_reference()
    callbacks.assert_expected(primary_counter, secondary_counter)
