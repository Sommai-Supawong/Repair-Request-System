import os

import click
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, logout_user
from flask_wtf.csrf import CSRFError

from config import Config
from extensions import csrf, db, login_manager
from localization import (
    image_type_label,
    problem_type_label,
    role_label,
    status_label,
    thai_date,
    urgency_label,
)
from routes import admin_bp, auth_bp, dashboard_bp, repairs_bp


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    login_manager.login_message = "กรุณาเข้าสู่ระบบเพื่อใช้งานหน้านี้"

    app.jinja_env.filters.update(
        status_label=status_label,
        urgency_label=urgency_label,
        problem_type_label=problem_type_label,
        role_label=role_label,
        image_type_label=image_type_label,
        thai_date=thai_date,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(repairs_bp)
    app.register_blueprint(admin_bp)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.before_request
    def reject_disabled_session():
        if current_user.is_authenticated and not current_user.is_active:
            logout_user()
            if request.endpoint != "auth.login":
                return redirect(url_for("auth.login"))

    @app.get("/")
    def index():
        return redirect(url_for("dashboard.index" if current_user.is_authenticated else "auth.login"))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(413)
    def too_large(error):
        return render_template("errors/413.html"), 413

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        return render_template("errors/csrf.html"), 400

    @app.cli.command("init-db")
    @click.option("--seed/--no-seed", default=True, help="Create demo accounts.")
    def init_db(seed):
        """Create database tables and optional demo users."""
        from services import UserService

        db.create_all()
        if seed:
            UserService.seed_demo_users()
        click.echo("Database initialized.")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
