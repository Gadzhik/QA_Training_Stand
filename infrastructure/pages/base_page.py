import allure
from playwright.async_api import Page, Locator, expect
from infrastructure.logger import get_logger

logger = get_logger("BasePage")

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def open(self, url: str):
        logger.info(f"Opening URL: {url}")
        with allure.step(f"Open URL: {url}"):
            await self.page.goto(url)

    async def get_element(self, selector: str) -> Locator:
        return self.page.locator(selector)

    async def click(self, selector: str):
        logger.info(f"Clicking element: {selector}")
        with allure.step(f"Click element: {selector}"):
            await self.page.click(selector)

    async def fill(self, selector: str, text: str):
        logger.info(f"Filling element {selector} with text: {text}")
        with allure.step(f"Fill {selector} with '{text}'"):
            await self.page.fill(selector, text)

    async def get_text(self, selector: str) -> str:
        text = await self.page.inner_text(selector)
        logger.info(f"Got text from {selector}: {text}")
        return text

    async def is_visible(self, selector: str) -> bool:
        visible = await self.page.is_visible(selector)
        logger.info(f"Element {selector} visible: {visible}")
        return visible
        
    async def screenshot(self, name: str):
        png_bytes = await self.page.screenshot()
        allure.attach(
            png_bytes, 
            name=name, 
            attachment_type=allure.attachment_type.PNG
        )
