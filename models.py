"""数据模型（SQLAlchemy ORM）。

表结构说明：
- users        用户（体重等用于卡路里估算）
- workouts     一次运动记录
- track_points 该次运动的 GPS 轨迹点
- plans        预设训练计划（跑步/走路/骑行）
- enrollments  用户参加计划的状态与进度
"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), default="新手跑者")
    gender = Column(String(10), default="unknown")  # male / female / unknown
    birth_year = Column(Integer, nullable=True)
    weight_kg = Column(Float, default=60.0)  # 卡路里估算关键输入
    height_cm = Column(Float, default=170.0)
    goal_text = Column(String(100), default="月减 2 kg")
    created_at = Column(DateTime, default=datetime.now)

    workouts = relationship("Workout", back_populates="user", cascade="all, delete")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, default=1)
    type = Column(String(20), index=True)  # 跑步 / 走路 / 骑行
    started_at = Column(DateTime, index=True)
    ended_at = Column(DateTime)
    duration_sec = Column(Integer, default=0)  # 实际运动秒数（不含自动暂停）
    distance_m = Column(Float, default=0.0)
    avg_pace_sec = Column(Float, default=0.0)  # 秒/公里
    calories = Column(Float, default=0.0)
    avg_heart_rate = Column(Integer, nullable=True)
    note = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="workouts")
    points = relationship(
        "TrackPoint", back_populates="workout", cascade="all, delete-orphan"
    )


class TrackPoint(Base):
    __tablename__ = "track_points"

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), index=True)
    seq = Column(Integer, default=0)  # 点位顺序
    lat = Column(Float)
    lng = Column(Float)
    altitude = Column(Float, nullable=True)
    ts = Column(DateTime)  # 采样时间

    workout = relationship("Workout", back_populates="points")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(20), index=True)  # 跑步 / 走路 / 骑行
    weeks = Column(Integer, default=4)
    sessions_per_week = Column(Integer, default=3)
    level = Column(String(20), default="零基础")
    description = Column(Text, default="")
    is_preset = Column(Boolean, default=True)


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, default=1)
    plan_id = Column(Integer, ForeignKey("plans.id"), index=True)
    current_week = Column(Integer, default=1)
    status = Column(String(20), default="active")  # active / done / quit
    started_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    plan = relationship("Plan")
