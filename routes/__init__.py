from .admin import admin_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .repairs import repairs_bp

__all__ = ["auth_bp", "dashboard_bp", "repairs_bp", "admin_bp"]

