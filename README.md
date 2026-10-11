# Escape-Room Creation and Management System

Course project for *Ingeniería del Software* (UPV, Campus d'Alcoi). The goal
of the system is to let an escape-room company manage its rooms, time slots
and reservations, and let customers browse rooms and book a session for
their team.

This repository follows the structure requested in the assignment brief:

```
doc/     design docs, SRS, Scrum documentation
src/     source code (the Flask application)
lib/     dependencies
```

## Team

> Fill in with your team's names and student IDs.

- Name Surname (PXXXXX)
- Name Surname (PXXXXX)

## Current scope (Sprint 1)

Sprint 1 covers the initial requirement analysis and a first working
prototype. What you can do with it today:

- Browse the list of escape rooms and see their details.
- See the upcoming available sessions (time slots) for a room.
- Book a session for a team, with a party size limited by the remaining
  capacity.
- Cancel a reservation.
- As an admin (no login yet, see `doc/SRS.md`): create new rooms and add
  sessions to them.

Things like puzzles/challenges, scoring, cancellation policies and
authentication are intentionally left for later sprints — see
`doc/SRS.md` for the full requirement list and what's in/out of scope.

## Running it locally

```bash
cd src
python -m venv ../venv
../venv/Scripts/activate        # on Windows
# source ../venv/bin/activate   # on macOS/Linux
pip install -r ../lib/requirements.txt

python seed.py      # creates the database and loads 3 sample rooms
python app.py        # starts the dev server on http://127.0.0.1:5000
```

Open http://127.0.0.1:5000 to see the room list, and
http://127.0.0.1:5000/admin to add rooms/sessions.

The database is a local SQLite file (`src/escape_room.db`), created
automatically — delete it and re-run `seed.py` any time you want to start
fresh.

## Project docs

- [`doc/SRS.md`](doc/SRS.md) — software requirements specification.
- [`doc/scrum/sprint1/backlog.md`](doc/scrum/sprint1/backlog.md) — Sprint 1
  backlog.
- [`doc/scrum/sprint1/`](doc/scrum/sprint1/) — meeting reports and sprint
  review (fill these in after your actual team meetings, the assignment
  requires at least 2 meeting reports per sprint).

## Putting this on GitHub

The assignment requires each team to have its own GitHub repository with
all members added as collaborators. To set that up:

1. On github.com, create a new **empty** repository (no README/license,
   this folder already has one).
2. In this folder, run:
   ```bash
   git init
   git add .
   git commit -m "Sprint 1: initial SRS and booking prototype"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. On GitHub, go to **Settings → Collaborators** and add every team member
   with full (admin) access, as the brief requires.
4. Use **Issues** on GitHub as your Scrum backlog (one issue per backlog
   item), and organize them into a Project board if you want a visual
   Sprint board.
