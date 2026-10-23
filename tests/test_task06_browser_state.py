import pytest
from playwright.async_api import expect
from helpers import search_amazon, find_product_card, card_title

@pytest.mark.amazon
async def test_product_context_survives_navigation(amazon_page, product_keyword):
    page = amazon_page
    await search_amazon(page, product_keyword)
    card = await find_product_card(page, product_keyword)
    selected_title = await card_title(card)
    selected_href = await card.locator("h2 a").get_attribute("href")
    assert selected_href, "Selected product did not expose a link."

    await card.locator("h2 a").click()
    await page.wait_for_load_state("domcontentloaded")
    await expect(page.locator("#productTitle")).to_be_visible(timeout=15000)
    detail_title = " ".join((await page.locator("#productTitle").inner_text()).split())
    assert selected_title.casefold() in detail_title.casefold() or detail_title.casefold() in selected_title.casefold()

    # Back navigation verifies the search context remains usable.
    await page.go_back(wait_until="domcontentloaded")
    await expect(page.locator("#twotabsearchtextbox")).to_be_visible()
    assert product_keyword.casefold() in (await page.locator("#twotabsearchtextbox").input_value()).casefold()
