import tomllib
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_PATH = Path("config.toml")


@dataclass(frozen=True)
class Config:
    title: str = "example.xyz"
    description: str = "An example image gallery"
    tags_whitelist: list[str] = field(default_factory=list)
    tags_blacklist: list[str] = field(default_factory=list)
    tags_custom_order: bool = False


def load_config(path: Path = CONFIG_PATH) -> Config:
    if not path.is_file():
        return Config()
    with open(path, "rb") as file:
        data = tomllib.load(file)
    tags = data.pop("tags", {})
    return Config(**data, **{f"tags_{key}": value for key, value in tags.items()})


config = load_config()
