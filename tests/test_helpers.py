from page_analyzer.utils.helpers import (
    MAX_TEXT_LENGTH,
    PageSeoInfo,
    crop_text,
    get_page_seo_info,
    get_root_url,
)


def test_get_root_url():
    url = "https://example.com/path?param1=1&param2=2#hash"
    
    assert get_root_url(url) == "https://example.com"


def test_crop_none_text():
    assert crop_text(None) is None


def test_crop_short_text():
    short_text = "Short text"
    assert crop_text(short_text) == short_text
    
    
def test_crop_long_text(test_data_path):
    with open(f"{test_data_path}/text.txt", encoding="utf-8") as file:
        text = file.read()
        
        assert len(crop_text(text)) == MAX_TEXT_LENGTH


def test_get_page_seo_info(test_data_path):
    with open(f"{test_data_path}/page.html", encoding="utf-8") as file:
        page_html = file.read()
        
        expected_seo_info = PageSeoInfo(
            h1="Заголовок h1",
            title="Содержимое тега title",
            description="Содержимое мета-тега description"
        )
        
        assert get_page_seo_info(page_html) == expected_seo_info
