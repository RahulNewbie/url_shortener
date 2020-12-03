import short_url


def url_shortener(url_id):
    """
    Method to short url using url id
    url_id = id of the url
    """
    domain = 'tier.app'
    shortened_url = "http://{}/{}".format(
                                     domain,
                                     short_url.encode_url(url_id)
                               )
    print(shortened_url)
    return shortened_url
