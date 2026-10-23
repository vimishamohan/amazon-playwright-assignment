import pytest
from playwright.async_api import expect
from helpers import search_amazon, find_product_card, card_title, visible_price, open_card_product

@pytest.mark.amazon
async def test_end_to_end_product_discovery(amazon_page, product_keyword):
    page = amazon_page
    await search_amazon(page, product_keyword)
    card = await find_product_card(page, product_keyword)
    result_title = await card_title(card)
    price = await visible_price(card)
    detail_title = await open_card_product(page, card)

    assert result_title.casefold() in detail_title.casefold() or detail_title.casefold() in result_title.casefold(), (
        f"Search-result title and detail title differ. Result={result_title!r}; detail={detail_title!r}"
    )
    print({"title": detail_title, "price_when_visible": price, "url": page.url})
    assert page.url.startswith("https://www.amazon.in/")
