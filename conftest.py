import pytest
import asyncio
import sys
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from playwright.async_api import Page, async_playwright

from src.config.config import settings
from infrastructure.db.connector import engine, AsyncSessionLocal, Base
from infrastructure.clients.api_client import APIClient

# Helper for Sync DB access
def get_sync_db_url():
    # Replace async driver with default (psycopg2)
    return settings.db.DATABASE_URL.replace("+asyncpg", "")

@pytest.fixture(scope="session")
def prepare_database():
    """Create tables before tests and drop after (Sync)"""
    sync_engine = create_engine(get_sync_db_url())
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    yield
    Base.metadata.drop_all(sync_engine)
    sync_engine.dispose()

@pytest.fixture
async def db_session(prepare_database) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def api_client() -> AsyncGenerator[APIClient, None]:
    client = APIClient(base_url=settings.wiremock.WIREMOCK_URL)
    yield client
    await client.close()

@pytest.fixture
async def page() -> AsyncGenerator[Page, None]:
    async with async_playwright() as p:
        # Launch browser manually
        browser = await p.chromium.launch(
            headless=settings.playwright.HEADLESS,
            slow_mo=settings.playwright.SLOW_MO
        )
        context = await browser.new_context(
            viewport={"width": settings.playwright.VIEWPORT_WIDTH, "height": settings.playwright.VIEWPORT_HEIGHT}
        )
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()
