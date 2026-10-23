import pytest
from playwright.async_api import expect

@pytest.mark.mock
async def test_mock_multistep_form_persists_values(page):
    await page.set_content("""
    <!doctype html><html><body>
      <h1>Trainer Mock Checkout</h1>
      <section id="step1">
        <label for="recipient">Test recipient</label>
        <input id="recipient" name="recipient">
        <button id="next" type="button">Continue</button>
      </section>
      <section id="step2" hidden>
        <label for="delivery">Delivery note</label>
        <input id="delivery" name="delivery">
        <button id="back" type="button">Back</button>
      </section>
      <script>
        document.querySelector('#next').onclick = () => {
          document.querySelector('#step1').hidden = true;
          document.querySelector('#step2').hidden = false;
        };
        document.querySelector('#back').onclick = () => {
          document.querySelector('#step2').hidden = true;
          document.querySelector('#step1').hidden = false;
        };
      </script>
    </body></html>
    """)
    await page.get_by_label("Test recipient").fill("Demo User")
    await page.get_by_role("button", name="Continue").click()
    await expect(page.get_by_label("Delivery note")).to_be_visible()
    await page.get_by_label("Delivery note").fill("Leave at demo desk")
    await page.get_by_role("button", name="Back").click()
    await expect(page.get_by_label("Test recipient")).to_have_value("Demo User")
    await page.get_by_role("button", name="Continue").click()
    await expect(page.get_by_label("Delivery note")).to_have_value("Leave at demo desk")
