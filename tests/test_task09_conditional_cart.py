import pytest
from playwright.async_api import expect
from helpers import search_amazon, find_product_card, open_card_product

@pytest.mark.amazon
async def test_add_to_cart_only_when_available(amazon_page, product_keyword):
    page = amazon_page
    await search_amazon(page, product_keyword)
    card = await find_product_card(page, product_keyword)
    title = await open_card_product(page, card)

    add_button = page.locator("#add-to-cart-button")
    if not await add_button.is_visible():
        pytest.skip(f"Skipped cart check: Add to Cart not visible for {title!r}.")
    if not await add_button.is_enabled():
        pytest.skip(f"Skipped cart check: Add to Cart disabled for {title!r}.")

    await add_button.click()
    await page.locator("#nav-cart").click()
    await page.wait_for_load_state("domcontentloaded")
    body = " ".join((await page.locator("body").inner_text()).split())
    assert title.split()[0].casefold() in body.casefold(), (
        f"Expected product {title!r} was not found in the cart."
    )
