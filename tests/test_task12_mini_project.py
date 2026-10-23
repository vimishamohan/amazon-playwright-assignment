import pytest
from playwright.async_api import expect
from helpers import search_amazon, find_product_card, card_title, open_card_product

@pytest.mark.amazon
async def test_mini_project_search_select_and_conditional_cart(amazon_page, product_keyword, failure_screenshot):
    page = amazon_page
    try:
        await search_amazon(page, product_keyword)
        card = await find_product_card(page, product_keyword)
        result_title = await card_title(card)
        detail_title = await open_card_product(page, card)
        assert result_title.casefold() in detail_title.casefold() or detail_title.casefold() in result_title.casefold()

        add_button = page.locator("#add-to-cart-button")
        if not await add_button.is_visible() or not await add_button.is_enabled():
            pytest.skip(f"Product unavailable or Add to Cart disabled for {detail_title!r}.")
        await add_button.click()
        await page.locator("#nav-cart").click()
        await page.wait_for_load_state("domcontentloaded")
        body = " ".join((await page.locator("body").inner_text()).split()).casefold()
        assert detail_title.split()[0].casefold() in body, (
            f"Selected product {detail_title!r} not found in cart."
        )
        # Never proceed to checkout's final review/place-order action.
    except Exception:
        path = await failure_screenshot("mini_project")
        print(f"Failure screenshot saved to: {path}")
        raise
