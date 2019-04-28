from bs4.element import Tag


class Listing:
    """ Represents a single listing on Craigslist """

    def __init__(self, html: Tag):
        """Initialization method

        Args:
            html: (Tag), the HTML that is inside of each listing
        """
        self.__listing = html
        self.listing_id = self.__parse_listing_for_id()
        self.price = self.__parse_listing_for_price()
        self.listing_url = self.__parse_listing_for_url()

    def __parse_listing_for_price(self) -> str:
        """Get the pricing for each listing

        Returns:
            str: price of the listing
        """
        price = self.__listing.find('span', class_='result-price')
        if price:
            return price.text

    def __parse_listing_for_id(self) -> int:
        """Get the assigned ID from each listing

        Returns:
            int: the ID of each listing
        """
        post_id = self.__listing.find('li', class_='result-row')
        if post_id:
            return int(post_id.get('data-pid'))

    def __parse_listing_for_url(self) -> str:
        """Get the URL to each listing

        Returns:
            str: URL associated the listing
        """
        url = self.__listing.find('a', class_='result-image gallery')
        if url:
            return url.get('href')
