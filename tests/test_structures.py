from conftest import SCOPUS_FIELDS, WOS_FIELDS
from model.structures import ScopusPublication, WosPublication
import pytest


@pytest.mark.parametrize('pub_class, fields', [(ScopusPublication, SCOPUS_FIELDS),
                                               (WosPublication, WOS_FIELDS)])
def test_required_fields_are_correct(pub_class, fields):
    assert pub_class.required_fields() == set(fields)