import pytest
from playwright.async_api import expect, TimeoutError as PlaywrightTimeoutError
from helpers import search_amazon, RESULT_CARD

@pytest.mark.amazon
async def test_pagination_or_lazy_loaded_results(amazon_page, product_keyword):
    page = amazon_page
    await search_amazon(page, product_keyword)
    before = await page.locator(RESULT_CARD).count()
    assert before > 0, "No search result cards found on initial page."

    next_page = page.locator("a.s-pagination-next")
    if await next_page.count() and await next_page.first.is_visible() and await next_page.first.is_enabled():
        old_url = page.url
        await next_page.first.click()
        await page.wait_for_load_state("domcontentloaded")
        await expect(page.locator(RESULT_CARD).first).to_be_visible(timeout=15000)
        assert page.url != old_url or await page.locator(RESULT_CARD).count() != before, (
            "Next-page action did not appear to change the results."
        )
        print("Pagination pattern detected.")
        return

    await page.locator(RESULT_CARD).last.scroll_into_view_if_needed()
    try:
        await page.wait_for_function(
            "(selector, oldCount) => document.querySelectorAll(selector).length > oldCount",
            arg=[RESULT_CARD, before],
            timeout=4000,
        )
        after = await page.locator(RESULT_CARD).count()
        assert after > before
        print(f"Lazy loading detected: {before} -> {after} cards.")
    except PlaywrightTimeoutError:
        pytest.skip(
            "No enabled classic next-page control and no additional cards loaded after scrolling. "
            "Document the observed live-site pattern; use a trainer-approved demo page for this pattern."
        )
