"""公共依赖。

MVP 阶段不做登录（产品原则：零设置起步），统一使用默认用户 id=1。
后续要接入账号体系，只需把 get_default_user 换成真实鉴权逻辑即可。
"""
from .database import SessionLocal
from .models import User

DEFAULT_USER_ID = 1


def get_default_user(db):
    """获取默认用户，不存在则自动创建（方便首次启动直接调试）。"""
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if user is None:
        user = User(
            id=DEFAULT_USER_ID,
            nickname="新手跑者",
            weight_kg=60.0,
            height_cm=170.0,
            goal_text="月减 2 kg",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


__all__ = ["get_default_user", "DEFAULT_USER_ID", "SessionLocal"]
