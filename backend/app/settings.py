from pydantic_settings import BaseSettings, SettingsConfigDict


# env variables for database

class DatabaseConfig(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env.db",
        env_file_encoding="utf-8"
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


database_config = DatabaseConfig()



# env variables for jwt auth

class JWTConfig(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env.jwt", env_file_encoding="utf-8")


jwt_config = JWTConfig()


