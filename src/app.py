import os
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from models import EscapeRoom, GameSession, Reservation, Team, db

BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'escape_room.db'}"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app


def register_routes(app):
    # ---------- public pages ----------

    @app.route("/")
    def index():
        rooms = EscapeRoom.query.order_by(EscapeRoom.name).all()
        return render_template("index.html", rooms=rooms)

    @app.route("/rooms/<int:room_id>")
    def room_detail(room_id):
        room = EscapeRoom.query.get_or_404(room_id)
        upcoming = (
            GameSession.query.filter(
                GameSession.room_id == room.id,
                GameSession.start_time >= datetime.now(),
                GameSession.status != "cancelled",
            )
            .order_by(GameSession.start_time)
            .all()
        )
        return render_template("room_detail.html", room=room, sessions=upcoming)

    @app.route("/sessions/<int:session_id>/reserve", methods=["GET", "POST"])
    def reserve(session_id):
        session_obj = GameSession.query.get_or_404(session_id)

        if request.method == "POST":
            team_name = request.form.get("team_name", "").strip()
            leader_name = request.form.get("leader_name", "").strip()
            leader_email = request.form.get("leader_email", "").strip()
            leader_phone = request.form.get("leader_phone", "").strip()
            party_size = int(request.form.get("party_size", 0))

            if not team_name or not leader_name or not leader_email:
                flash("Please fill in the team name, leader name and email.", "error")
                return render_template(
                    "reserve.html", session=session_obj, room=session_obj.room
                )

            if party_size < 1 or party_size > session_obj.available_spots:
                flash(
                    f"This session only has {session_obj.available_spots} spot(s) left.",
                    "error",
                )
                return render_template(
                    "reserve.html", session=session_obj, room=session_obj.room
                )

            team = Team(
                name=team_name,
                leader_name=leader_name,
                leader_email=leader_email,
                leader_phone=leader_phone,
            )
            db.session.add(team)
            db.session.flush()  # get team.id before commit

            reservation = Reservation(
                session_id=session_obj.id, team_id=team.id, party_size=party_size
            )
            db.session.add(reservation)

            if session_obj.available_spots - party_size <= 0:
                session_obj.status = "full"

            db.session.commit()
            flash("Reservation confirmed!", "success")
            return redirect(url_for("reservation_detail", reservation_id=reservation.id))

        return render_template("reserve.html", session=session_obj, room=session_obj.room)

    @app.route("/reservations/<int:reservation_id>")
    def reservation_detail(reservation_id):
        reservation = Reservation.query.get_or_404(reservation_id)
        return render_template("confirmation.html", reservation=reservation)

    @app.route("/reservations/<int:reservation_id>/cancel", methods=["POST"])
    def cancel_reservation(reservation_id):
        reservation = Reservation.query.get_or_404(reservation_id)
        reservation.status = "cancelled"
        if reservation.session.status == "full":
            reservation.session.status = "available"
        db.session.commit()
        flash("Reservation cancelled.", "success")
        return redirect(url_for("reservation_detail", reservation_id=reservation.id))

    # ---------- admin pages (no auth yet - planned for a later sprint) ----------

    @app.route("/admin")
    def admin_index():
        rooms = EscapeRoom.query.order_by(EscapeRoom.name).all()
        return render_template("admin/index.html", rooms=rooms)

    @app.route("/admin/rooms/new", methods=["GET", "POST"])
    def admin_new_room():
        if request.method == "POST":
            room = EscapeRoom(
                name=request.form["name"].strip(),
                theme=request.form["theme"].strip(),
                description=request.form.get("description", "").strip(),
                min_players=int(request.form["min_players"]),
                max_players=int(request.form["max_players"]),
                duration_minutes=int(request.form["duration_minutes"]),
                difficulty=request.form["difficulty"],
                price_per_person=float(request.form["price_per_person"]),
            )
            db.session.add(room)
            db.session.commit()
            flash(f"Room '{room.name}' created.", "success")
            return redirect(url_for("admin_index"))
        return render_template("admin/new_room.html")

    @app.route("/admin/rooms/<int:room_id>/sessions/new", methods=["GET", "POST"])
    def admin_new_session(room_id):
        room = EscapeRoom.query.get_or_404(room_id)
        if request.method == "POST":
            start_time = datetime.strptime(
                request.form["start_time"], "%Y-%m-%dT%H:%M"
            )
            capacity = int(request.form.get("capacity") or room.max_players)
            session_obj = GameSession(
                room_id=room.id, start_time=start_time, capacity=capacity
            )
            db.session.add(session_obj)
            db.session.commit()
            flash("Session added.", "success")
            return redirect(url_for("admin_index"))
        return render_template("admin/new_session.html", room=room)

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
