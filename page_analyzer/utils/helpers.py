from urllib.parse import urlparse, urlunparse


def get_root_url(url: str) -> str:
    """Убирает из url путь, параметры запроса, и хеш.
    Т.е. оставляет только url до корня сайта.

    Args:
        url (str): исходный url

    Returns:
        str: url до корня сайта
    """
    parsed_url = urlparse(url)
    root_url = parsed_url._replace(fragment="", query="", path="")
    
    return urlunparse(root_url)
