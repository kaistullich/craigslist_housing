from typing import List, Union

import requests
from bs4 import BeautifulSoup

from listing import Listing
from models import CraigslistHousing, session

URL = 'https://sfbay.craigslist.org/search/sby/apa?hasPic=1&bundleDuplicates=1&min_price=1100&max_price=1800&availabilityMode=0&sale_date=all+dates'


def get_page(url: str = URL) -> Union[int, str]:
    """Send request to Craigslist

    Args:
        url: (Optional[str]), URL to send request to

    Returns:
        Union[int, str]: return HTML content if HTTP status code is 200, else
                        will return the HTTP status code
    """
    req = requests.get(url=url)
    if req.status_code == 200:
        return req.text
    return req.status_code


def get_all_listings(html: str) -> List[Listing]:
    """Gets each individual listing

    Args:
        html:

    Returns:

    """
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find('ul', class_='rows')
    all_listings = []
    for listing in ul.contents:
        # newline also gets created from ``.contents``
        if listing != '\n':
            post = Listing(html=listing)
            all_listings.append(post)
    return all_listings


def add_listings_to_db(all_listings: List[Listing]) -> int:
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


if __name__ == '__main__':
    # send request to URL
    html_content = get_page()
    # check that the HTTP status code is OK
    if isinstance(html_content, str):
        listings = get_all_listings(html=html_content)
        add_listings_to_db(all_listings=listings)
    else:
        raise Exception(f'Failure: HTTP Code --> {html_content}')
