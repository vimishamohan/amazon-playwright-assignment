import json
from pathlib import Path
import pytest
from playwright.async_api import expect
from helpers import search_amazon, find_product_card, card_title

MOCK_API_FILE = Path(__file__).parent / "fixtures" / "product_api.json"

@pytest.mark.mock
async def test_ui_title_matches_trainer_mock_api(amazon_page, product_keyword):

    if not MOCK_API_FILE.exists():
        pytest.skip(f"Trainer mock API fixture missing: {MOCK_API_FILE}")
    data = json.loads(MOCK_API_FILE.read_text(encoding="utf-8"))
    raw_title = data["product"]["title"]
    if raw_title.startswith("REPLACE WITH"):
        pytest.skip("Replace the sample mock API title with trainer-approved data before comparison.")
    api_title = " ".join(raw_title.split())
    endpoint = data["source_endpoint"]
    field = "product.title"

    page = amazon_page
    await search_amazon(page, product_keyword)
    card = await find_product_card(page, product_keyword)
    ui_title = " ".join((await card_title(card)).split())

    assert api_title.casefold() == ui_title.casefold(), (
        f"UI/API mismatch for {field}. Source={endpoint}; API={api_title!r}; UI={ui_title!r}. "
        "Confirm that both values describe the same product and update approved test data."
    )
