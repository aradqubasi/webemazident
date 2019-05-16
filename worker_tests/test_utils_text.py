import pytest
from workeremazident import utils

def test_split_by_sentances():
    assert utils.text.split_by_sentences('First. Second. Third.') == ['First', ' Second', ' Third']

