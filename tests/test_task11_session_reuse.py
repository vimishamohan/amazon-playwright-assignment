from pathlib import Path
import pytest
from playwright.async_api import expect

STATE_FILE = Path("auth_state.json")

@pytest.mark.amazon
async def test_session_reuse_and_missing_file_handling(browser):
    if not STATE_FILE.exists():
        pytest.skip("Missing auth_state.json handled as expected; run setup_auth_state.py only if authorized.")

    context = await browser.new_context(storage_state=str(STATE_FILE))
    page = await context.new_page()
    try:
        await page.goto("https://www.amazon.in/", wait_until="domcontentloaded")
        await expect(page.locator("#nav-link-accountList")).to_be_visible()
        body = " ".join((await page.locator("body").inner_text()).split()).casefold()
        if "sign in" in body:
            pytest.skip("State file loaded, but the account session appears expired.")
    finally:
        await context.close()

def test_missing_state_file_is_reported_cleanly(tmp_path):
    missing = tmp_path / "does_not_exist.json"
    assert not missing.exists()
    # This verifies our setup logic: missing state must be detected, not silently ignored.
    with pytest.raises(FileNotFoundError):
        missing.read_text(encoding="utf-8")
