import os
from pathlib import Path

import click
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, logout_user
from flask_wtf.csrf import CSRFError
from sqlalchemy.engine import make_url
from werkzeug.middleware.proxy_fix import ProxyFix

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


def _ensure_storage_directories(app: Flask) -> None:
    upload_folder = Path(app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    database_url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    if database_url.drivername.startswith("sqlite") and database_url.database not in (None, "", ":memory:"):
        database_path = Path(database_url.database)
        if not database_path.is_absolute():
            database_path = Path(app.instance_path) / database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is required in production. Set it in the environment.")
    if app.config.get("TRUST_PROXY_HEADERS"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    os.makedirs(app.instance_path, exist_ok=True)
    _ensure_storage_directories(app)

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

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("errors/400.html"), 400

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
    def init_db():
        """Create missing database tables without deleting or seeding data."""
        db.create_all()
        click.echo("Database initialized.")

    @app.cli.command("seed-demo")
    def seed_demo():
        """Create demo accounts if they do not already exist."""
        from services import UserService

        db.create_all()
        UserService.seed_demo_users()
        click.echo("Demo accounts are ready.")

    @app.cli.command("create-admin")
    @click.option("--username", prompt="Admin username")
    @click.option("--fullname", prompt="Admin full name")
    @click.option("--email", prompt="Admin email")
    @click.option(
        "--password",
        prompt="Admin password",
        hide_input=True,
        confirmation_prompt=True,
    )
    def create_admin(username, fullname, email, password):
        """Create the first production administrator interactively."""
        from services import UserService

        db.create_all()
        try:
            UserService.create(username, password, fullname, email, "admin")
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(f"Administrator {username.strip().lower()} created.")

    return app


app = create_app()


if __name__ == "__main__":
    debug_enabled = os.getenv("FLASK_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}
    app.run(debug=debug_enabled and not app.config.get("PRODUCTION", False))
