"""Import all models from the models package."""

from ..app_settings import OWM_USE_BUILTIN_CONCRETE_MODELS  # noqa: F401,F403
from .abstract import *  # noqa: F401,F403
from .base import *  # noqa: F401,F403


if OWM_USE_BUILTIN_CONCRETE_MODELS:
    from .concrete import *  # noqa: F401,F403
