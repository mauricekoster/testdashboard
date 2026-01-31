import warnings

from pydantic import (
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", 
        env_ignore_empty=True, 
        extra="ignore"
    )
    ENVIRONMENT: str = "local"
    PROJECT_NAME: str
    BACKEND_API_URL: str = "http://localhost:8000"
    API_V1_STR: str = "/api/v1"
    STORAGE_SECRET: str = "changethis"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("STORAGE_SECRET", self.STORAGE_SECRET)

        return self


settings = Settings()  # type: ignore
