from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EscapeRoom(db.Model):
    """An escape room offered by the company (e.g. 'The Pharaoh's Curse')."""

    __tablename__ = "escape_rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    min_players = db.Column(db.Integer, nullable=False, default=2)
    max_players = db.Column(db.Integer, nullable=False, default=6)
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    difficulty = db.Column(db.String(20), nullable=False, default="Medium")
    price_per_person = db.Column(db.Float, nullable=False, default=20.0)

    sessions = db.relationship(
        "GameSession", backref="room", cascade="all, delete-orphan"
    )


class GameSession(db.Model):
    """A bookable time slot for a given room (e.g. Saturday 18:00)."""

    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("escape_rooms.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="available")
    # status values: available | full | cancelled

    reservations = db.relationship(
        "Reservation", backref="session", cascade="all, delete-orphan"
    )

    @property
    def booked_spots(self):
        return sum(
            r.party_size for r in self.reservations if r.status == "confirmed"
        )

    @property
    def available_spots(self):
        return max(self.capacity - self.booked_spots, 0)

    @property
    def is_full(self):
        return self.available_spots <= 0


class Team(db.Model):
    """A group of players making a reservation together."""

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    leader_name = db.Column(db.String(120), nullable=False)
    leader_email = db.Column(db.String(120), nullable=False)
    leader_phone = db.Column(db.String(40), nullable=True)

    reservations = db.relationship("Reservation", backref="team")


class Reservation(db.Model):
    """A booking of a team for a specific game session."""

    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer, db.ForeignKey("game_sessions.id"), nullable=False
    )
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="confirmed")
    # status values: confirmed | cancelled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
