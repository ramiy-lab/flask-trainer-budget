from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from dotenv import load_dotenv


BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
DATA_DIR: Final[Path] = BASE_DIR / "data"


load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """
    アプリケーション全体の設定をまとめる DTO
    """

    # --- 環境 ---
    env: str

    # --- データパス ---
    foods_json_path: Path
    protein_json_path: Path
    phase_json_path: Path

    # --- アプリ設定 ---
    debug: bool


def load_config() -> AppConfig:
    """
    環境変数から設定を読み込み AppConfig を生成する
    """
    env: str = os.getenv("APP_ENV", "development")

    debug_str: str = os.getenv("DEBUG", "false")
    debug: bool = debug_str.lower() == "true"

    return AppConfig(
        env=env,
        foods_json_path=DATA_DIR / "foods.json",
        proteins_json_path=DATA_DIR / "proteins.json",
        phase_json_path=DATA_DIR / "phase.json",
        debug=debug,
    )
