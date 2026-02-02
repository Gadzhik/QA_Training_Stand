from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

# Resolve root directory
# src/config/config.py -> src/config -> src -> root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

class AppConfig(BaseConfig):
    APP_BASE_URL: str = "http://localhost:8000"
    ENV: str = "local"

class DatabaseConfig(BaseConfig):
    POSTGRES_USER: str = "qa_user"
    POSTGRES_PASSWORD: str = "qa_password"
    POSTGRES_DB: str = "qa_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

class KafkaConfig(BaseConfig):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "test_topic"

class TestUserConfig(BaseConfig):
    TEST_USER_EMAIL: str = "test@example.com"
    TEST_USER_PASSWORD: str = "secret"

class PlaywrightConfig(BaseConfig):
    HEADLESS: bool = True
    BROWSER_CHANNEL: str = "chromium"
    SLOW_MO: int = 50
    VIEWPORT_WIDTH: int = 1920
    VIEWPORT_HEIGHT: int = 1080

class WireMockConfig(BaseConfig):
    WIREMOCK_URL: str = "http://localhost:8080"

class Settings:
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    kafka: KafkaConfig = KafkaConfig()
    test_user: TestUserConfig = TestUserConfig()
    playwright: PlaywrightConfig = PlaywrightConfig()
    wiremock: WireMockConfig = WireMockConfig()
    
    # Expose BASE_DIR for logger and others
    BASE_DIR: Path = BASE_DIR

settings = Settings()
