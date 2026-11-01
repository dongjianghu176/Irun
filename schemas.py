"""Pydantic 出入参模型（接口契约）。

前端和后端都以此为准，改接口先看这里。
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------- 用户 ----------------
class UserBase(BaseModel):
    nickname: Optional[str] = None
    gender: Optional[str] = None
    birth_year: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    goal_text: Optional[str] = None


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None


# ---------------- 运动记录 ----------------
class TrackPointIn(BaseModel):
    lat: float
    lng: float
    ts: Optional[datetime] = None
    altitude: Optional[float] = None


class WorkoutCreate(BaseModel):
    type: str = Field(default="跑步", description="跑步 / 走路 / 骑行")
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_sec: int = Field(default=0, ge=0)
    distance_m: float = Field(default=0, ge=0)
    calories: Optional[float] = None  # 不传则由服务端按体重/配速估算
    avg_heart_rate: Optional[int] = None
    note: str = ""
    points: List[TrackPointIn] = []


class WorkoutOut(BaseModel):
    id: int
    type: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_sec: int = 0
    duration_text: str = ""
    distance_m: float = 0
    distance_km: float = 0
    avg_pace_sec: float = 0
    pace_text: str = "--"
    calories: float = 0
    avg_heart_rate: Optional[int] = None
    note: str = ""
    point_count: int = 0


class TrackPointOut(BaseModel):
    seq: int
    lat: float
    lng: float
    altitude: Optional[float] = None
    ts: Optional[datetime] = None


# ---------------- 统计 ----------------
class StatSummary(BaseModel):
    range: str
    count: int
    distance_m: float
    distance_km: float
    duration_sec: int
    calories: float


class ChartItem(BaseModel):
    label: str
    value: float


class ChartOut(BaseModel):
    range: str
    unit: str
    items: List[ChartItem]


class StreakOut(BaseModel):
    current_streak: int
    best_streak: int
    todays_done: bool
    active_days: int


# ---------------- 训练计划 ----------------
class PlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    weeks: int
    sessions_per_week: int
    level: str
    description: str


class EnrollmentOut(BaseModel):
    id: int
    plan_id: int
    plan_name: str
    plan_type: str
    current_week: int
    weeks: int
    status: str
    progress_percent: int
