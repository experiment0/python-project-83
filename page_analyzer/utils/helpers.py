from typing import Optional
from urllib.parse import urlparse, urlunparse

MAX_TEXT_LENGTH = 255


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


def crop_text(text: Optional[str]) -> Optional[str]:
    """Обрезает текст до 255 символов

    Args:
        text (Optional[str]): исходный текст

    Returns:
        Optional[str]: обрезанный текст
    """
    if text is None:
        return None
    
    if len(text) < MAX_TEXT_LENGTH:
        return text
    
    return text[0:MAX_TEXT_LENGTH]
