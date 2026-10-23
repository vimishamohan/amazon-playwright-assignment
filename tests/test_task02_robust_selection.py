import pytest
from playwright.async_api import expect
from helpers import search_amazon, find_product_card, card_title

@pytest.mark.amazon
async def test_select_product_by_visible_title(amazon_page, product_keyword):
    page = amazon_page
    await search_amazon(page, product_keyword)
    card = await find_product_card(page, product_keyword)
    title = await card_title(card)
    assert product_keyword.casefold() in title.casefold(), (
        f"Matched card title {title!r} did not contain {product_keyword!r}"
    )
    # Interaction stays scoped to the matched card; do not click a global Add-to-cart.
    link = card.locator("h2 a").first
    await expect(link).to_be_visible()
    assert await link.get_attribute("href"), f"Product title link has no href: {title!r}"
