"""全局配置：数据库路径、服务端口等。

所有可配置项都集中在这里，方便二次开发时修改。
"""
import os
from pathlib import Path

# server/ 目录
BASE_DIR = Path(__file__).resolve().parents[1]
# 数据目录（SQLite 文件存放位置）
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 数据库地址，可用环境变量 IRUN_DATABASE_URL 覆盖
DATABASE_URL = os.getenv("IRUN_DATABASE_URL", f"sqlite:///{(DATA_DIR / 'irun.db').as_posix()}")

# 服务端口
PORT = int(os.getenv("IRUN_PORT", "8000"))

# 允许的运动类型（新增类型改这里 + 前端 TYPE 常量即可）
WORKOUT_TYPES = ["跑步", "走路", "骑行"]
