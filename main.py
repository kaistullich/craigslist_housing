import urllib
from typing import List, Union

import requests
from bs4 import BeautifulSoup

from listing import Listing
from models import CraigslistHousing, session


def build_url(**kwargs):
    """Build the URL with query parameters

    Args:
        **kwargs: (dict), any more query parameters can be passed to the URL

    Returns:
        str: the built URL
    """
    base_url = 'https://sfbay.craigslist.org/search/sby/apa?'

    query_params = {
        'hasPic': '1',
        'bundleDuplicates': '1',
        'min_price': '1100',
        'max_price': '1800',
        'availabilityMode': '0',
        'sale_date': 'all+dates',
    }

    # more query parameters passed, add them to the dict
    if kwargs:
        query_params.update(kwargs)

    return base_url + urllib.parse.urlencode(query_params)


def get_page_html(url: str) -> Union[int, str]:
    """Send request to Craigslist and get the HTML content

    Args:
        url: (str), URL to send request to

    Returns:
        Union[int, str]: return HTML content if HTTP status code is 200, else
                        will return the HTTP status code

    Raises:
        requests.exceptions.RequestException: if HTTP status code != 200
    """
    req = requests.get(url=url)
    if req.status_code == 200:
        return req.text
    raise requests.exceptions.RequestException('')


def get_all_listings(html: str) -> Union[List[Listing], bool]:
    """Get all listings on the page and parse them with ``listing.Listing()``

    Args:
        html: (str), all HTML returned from the page that was requested

    Returns:
        Union[List[Listing], bool]: Either all parsed listings or ``False`` if
                            we have reached the end of all listings and should
                            not continue to parse.
    """
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find('ul', class_='rows')
    if not check_if_empty_page(ul.contents):
        all_listings = []
        for listing in ul.contents:
            # newline also gets created from ``.contents``
            if listing != '\n':
                post = Listing(html=listing)
                all_listings.append(post)
        return all_listings
    return False


def add_listings_to_db(all_listings: List[Listing]) -> int:
    """Adds listings to the DB table

    Args:
        all_listings: (List[Listing]), listings that should be added

    Returns:
        int: if adding listing to DB was successful

    Raises:
        Exception: if committing to the DB went wrong
    """
    for listing in all_listings:
        session.add(CraigslistHousing(
                id=listing.listing_id,
                price=listing.price,
                url=listing.listing_url
        ))
    try:
        session.commit()
        return 1
    except Exception as e:
        raise e


def check_if_empty_page(content: list) -> bool:
    """Checks to see if there are any listings in the `ul` HTML

    Args:
        content: (list), HTML content inside of the `ul`

    Returns:
        bool: whether there are listings or not
    """
    return True if len(content) > 1 else False


if __name__ == '__main__':
    # build the URL with the query parameters
    req_url = build_url()
    # send request to URL
    html_content = get_page_html(url=req_url)
    while True:
        # get listings
        listings = get_all_listings(html=html_content)
        # add them to the DB
        add_listings_to_db(all_listings=listings)
