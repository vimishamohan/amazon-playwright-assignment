import pytest
from playwright.async_api import expect, TimeoutError as PlaywrightTimeoutError
from helpers import SEARCH_BOX, SEARCH_BUTTON, RESULT_CARD

@pytest.mark.amazon
async def test_autosuggest_or_fallback_to_search(amazon_page, product_keyword):
    page = amazon_page
    search = page.locator(SEARCH_BOX)
    await expect(search).to_be_visible()
    partial = product_keyword[:max(3, len(product_keyword) // 2)]
    await search.fill(partial)

    suggestions = page.locator('div[ role="row"], div.s-suggestion, div[role="option"]')
    try:
        await suggestions.first.wait_for(state="visible", timeout=2500)
        texts = [t.strip() for t in await suggestions.all_inner_texts() if t.strip()]
        print(f"Autocomplete suggestions shown: {texts[:8]}")
        matching = None
        for i in range(await suggestions.count()):
            item = suggestions.nth(i)
            text = " ".join((await item.inner_text()).split())
            if product_keyword.casefold() in text.casefold():
                matching = item
                break
        if matching:
            await matching.click()
        else:
            # A suggestion list exists, but no exact matching suggestion is exposed.
            await page.locator(SEARCH_BUTTON).click()
    except PlaywrightTimeoutError:
        print("Autocomplete was not visible in this session; using Search button fallback.")
        await page.locator(SEARCH_BUTTON).click()

    await page.wait_for_load_state("domcontentloaded")
    await expect(page.locator(RESULT_CARD).first).to_be_visible(timeout=15000)
