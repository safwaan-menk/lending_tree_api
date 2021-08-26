import main
from bs4 import BeautifulSoup
import pytest

mockSuccessfulUrls = [
    'https://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc/45102840',
    'https://www.lendingtree.com/reviews/personal/loanz/54243113',
    'https://www.lendingtree.com/reviews/mortgage/silver-fin-capital-group/37405089',
    'https://www.lendingtree.com/reviews/mortgage/pacific-beneficial-mortgage-company/44396611',
    'https://www.lendingtree.com/reviews/mortgage/triumph-lending/44068646',
    'https://www.facebook.com'
]

mockFailedUrls = [
    'ttps://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc/45102840',
    'https:/www.lendingtree.com/reviews/personal/loanz/54243113',
    'How to change a lightbulb for dummies',
    'https://www.lendingtree.con/reviews/mortgage/pacific-beneficial-mortgage-company/44396611',
]

mockSuccessfulSoups = [
    'https://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc/45102840',
    'https://www.lendingtree.com/reviews/personal/loanz/54243113',
    'https://www.lendingtree.com/reviews/mortgage/silver-fin-capital-group/37405089',
    'https://www.lendingtree.com/reviews/mortgage/pacific-beneficial-mortgage-company/44396611',
    'https://www.lendingtree.com/reviews/mortgage/triumph-lending/44068646',
]

mockFailedSoups = [
    'https://www.lendingtree.com/reviews/mortgage/reliance-first-capital-llc/45102840?sort=&pid=500',
    'https://www.lendingtree.com/reviews/personal/loanz/54243113a',
    'https://www.lendingtree.com/reviews/mortgage/safe-harbor-mortgage-company/31858872',
]

# Testing setting up api with valid URLs
@pytest.mark.parametrize("input", mockSuccessfulUrls)
def test_successful_urls(input):
     assert type(main.setup(input)) == BeautifulSoup 

# Testing setting up api with invalid URLs
@pytest.mark.parametrize("input", mockFailedUrls)
def test_failed_urls(input):
     assert main.setup(input) == 0

# Testing getting JSON output from api with valid URLs
@pytest.mark.parametrize("input", mockSuccessfulSoups)
def test_successful_soups(input):
    errors = []
    if type(main.extractsoup(main.setup(input))) != dict:
        errors.append("error: json not returning")
    if main.extractsoup(main.setup(input)) == 0:
        errors.append("error: no data available")

    assert not errors, "errors:\n{}".format("\n".join(errors))

# Testing getting JSON output from api with invalid URLs
@pytest.mark.parametrize("input", mockFailedSoups)
def test_failed_soups(input):
     assert main.extractsoup(main.setup(input)) == 0 