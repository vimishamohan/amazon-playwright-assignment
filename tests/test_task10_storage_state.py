from pathlib import Path
import pytest
from playwright.async_api import expect

STATE_FILE = Path("auth_state.json")

@pytest.mark.amazon
async def test_reuse_storage_state_if_available(browser):
    if not STATE_FILE.exists():
        pytest.skip(
            "auth_state.json not found. If permitted, run setup_auth_state.py with an authorized "
            "test account; otherwise leave this test skipped."
        )
    context = await browser.new_context(storage_state=str(STATE_FILE))
    page = await context.new_page()
    try:
        await page.goto("https://www.amazon.in/", wait_until="domcontentloaded")
        # Account text varies by locale/session. Detect a sign-in route or account indicator.
        url = page.url.casefold()
        body = " ".join((await page.locator("body").inner_text()).split()).casefold()
        if "signin" in url or "sign in" in body:
            pytest.skip("Saved session appears expired; re-authentication is needed.")
        account_indicator = page.locator("#nav-link-accountList")
        await expect(account_indicator).to_be_visible()
        print("Account navigation is visible. Verify authenticated status manually if ambiguous.")
    finally:
        await context.close()
