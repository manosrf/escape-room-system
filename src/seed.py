"""Fills the database with a few sample rooms and sessions so the prototype
is not empty the first time you run it.

Usage:
    python seed.py
"""

from datetime import datetime, timedelta

from app import create_app
from models import EscapeRoom, GameSession, db

SAMPLE_ROOMS = [
    dict(
        name="The Pharaoh's Curse",
        theme="Ancient Egypt",
        description=(
            "An archaeologist has gone missing inside a newly discovered tomb. "
            "Your team has one hour to find the Pharaoh's seal before the "
            "chamber reseals itself forever."
        ),
        min_players=2,
        max_players=6,
        duration_minutes=60,
        difficulty="Medium",
        price_per_person=22.0,
    ),
    dict(
        name="Lockdown: Zero Hour",
        theme="Heist / Thriller",
        description=(
            "You've been locked inside a bank vault during a simulated heist "
            "exercise. Crack the codes and get out before security resets the "
            "building."
        ),
        min_players=3,
        max_players=8,
        duration_minutes=75,
        difficulty="Hard",
        price_per_person=25.0,
    ),
    dict(
        name="The Last Transmission",
        theme="Sci-Fi / Space Station",
        description=(
            "A space station has lost contact with Earth. Restore the "
            "communication array before life support runs out."
        ),
        min_players=2,
        max_players=5,
        duration_minutes=60,
        difficulty="Easy",
        price_per_person=20.0,
    ),
]


def run():
    app = create_app()
    with app.app_context():
        if EscapeRoom.query.count() > 0:
            print("Database already has rooms - skipping seed.")
            return

        rooms = []
        for data in SAMPLE_ROOMS:
            room = EscapeRoom(**data)
            db.session.add(room)
            rooms.append(room)
        db.session.flush()  # assign ids

        base = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(
            days=1, hours=2
        )
        for room in rooms:
            for day_offset in range(3):
                for hour_offset in (0, 2, 4):
                    start = base + timedelta(days=day_offset, hours=hour_offset)
                    db.session.add(
                        GameSession(
                            room_id=room.id,
                            start_time=start,
                            capacity=room.max_players,
                        )
                    )

        db.session.commit()
        print(f"Seeded {len(rooms)} rooms with sessions.")


if __name__ == "__main__":
    run()
