import pytest
from playwright.async_api import expect, TimeoutError as PlaywrightTimeoutError
from helpers import search_amazon, find_product_card, open_card_product

@pytest.mark.amazon
async def test_cart_journey_stops_before_purchase(amazon_page, product_keyword):
    page = amazon_page
    await search_amazon(page, product_keyword)
    card = await find_product_card(page, product_keyword)
    selected_title = await open_card_product(page, card)

    add_button = page.locator("#add-to-cart-button")
    if not await add_button.is_visible():
        pytest.skip("Add to Cart is not visible for this product/session; no cart action taken.")
    if not await add_button.is_enabled():
        pytest.skip("Add to Cart is disabled; product may be unavailable.")

    await add_button.click()
    cart_link = page.locator("#nav-cart")
    await expect(cart_link).to_be_visible()
    await cart_link.click()
    await page.wait_for_load_state("domcontentloaded")

    cart_text = " ".join((await page.locator("body").inner_text()).split())
    if selected_title.casefold() not in cart_text.casefold():
        # The cart may use a shortened product title; make the mismatch explicit.
        assert selected_title.split()[0].casefold() in cart_text.casefold(), (
            f"Selected product not found in cart page text. Selected title: {selected_title!r}"
        )
    print("Cart validated. Test intentionally stops before purchase/Place Order.")
