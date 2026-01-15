from typing import Optional
from pydantic import BaseModel, Field
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup


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


class PageSeoInfo(BaseModel):
    h1: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    
def get_page_seo_info(page_html: str) -> PageSeoInfo:
    """Возвращает данные из значимых seo-тегов страницы

    Args:
        page_html (str): html страницы

    Returns:
        PageSeoInfo: объект с собранной из тегов информацией
    """
    h1 = None
    title = None
    description = None
    
    soup = BeautifulSoup(page_html, "html.parser")
    
    if soup.title is not None:
        title = soup.title.text
    
    h1_tag = soup.find("h1")
    if h1_tag is not None:
        h1 = h1_tag.text
    
    meta_tag = soup.find("meta", {"name": "description"})
    if meta_tag is not None:
        description = str(meta_tag.get("content"))
    
    return PageSeoInfo(h1=h1, title=title, description=description)
