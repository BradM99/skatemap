from pydantic import BaseModel, Field, PostgresDsn, computed_field


class Settings(BaseModel):
    """Application configuration."""

    ENV: str = Field("development")
    DEBUG: bool = Field(True)

    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("2569")
    POSTGRES_HOST: str = Field("localhost")
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_DB: str = Field("skatemap_db")

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()