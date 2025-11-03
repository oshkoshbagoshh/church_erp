import os, sys, pathlib


class Config:
    """ "Base configuration class."""

    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    NAME = os.getenv("NAME", "Pai Church ERP")
    DEBUG = os.getenv("DEBUG", False)

    def __str__(self) -> str:
        return f"Config(DEBUG={self.DEBUG}, SECRET_KEY={self.SECRET_KEY}, NAME={self.NAME})"


config = Config()

if __name__ == "__main__":
    print(config)
