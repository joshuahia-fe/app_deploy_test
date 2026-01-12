from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path

class DataPaths(BaseModel):
    project_root: Path = Path(".") # Root directory for the project - can reference to Z: drive

    # All other paths relative to the project root
    data_root: Path = project_root / "data"
    raw: Path = data_root / "01_raw"
    processed: Path = data_root / "02_processed"
    final: Path = data_root / "03_final"
    output: Path = data_root / "04_output"
    models: Path = project_root / "models"
    logs: Path = project_root / "logs"


class DBSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    password: str = ""
    database: str = "mydb"


class APISettings(BaseModel):
    base_url: str = "https://api.example.com"
    key: str = ""


class Settings(BaseSettings):
    data: DataPaths = DataPaths()
    db: DBSettings = DBSettings()
    api: APISettings = APISettings()

    model_config = SettingsConfigDict(
        env_file=".env",  # Name of the .env file, for testing change to .env_template
        env_nested_delimiter="__",  # Use __ in your .env file, map value to sub-model
    )


settings = Settings()
