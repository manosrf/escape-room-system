# Sprint 1 Backlog

**Sprint dates:** 30/09/2026 – 14/10/2026 (due 13/10/2026)
**Sprint goal:** Analyze requirements and deliver an initial working
prototype of the booking flow, as the basis for the rest of the project.

Copy each item below into a GitHub Issue in the team repo (the brief asks
for the backlog to live there, with issues assigned to team members).

| # | Item | Type | Notes |
|---|------|------|-------|
| 1 | Define system scope and actors (Admin, Player) | Analysis | Covered in `doc/SRS.md` §2.1 |
| 2 | Write initial SRS (functional + non-functional requirements) | Analysis | `doc/SRS.md` |
| 3 | Design data model (rooms, sessions, teams, reservations) | Design | `doc/SRS.md` §5, `src/models.py` |
| 4 | Set up Flask project skeleton | Dev | `src/app.py` |
| 5 | Room list page | Dev | `GET /` |
| 6 | Room detail page with available sessions | Dev | `GET /rooms/<id>` |
| 7 | Reservation form with capacity check | Dev | `GET/POST /sessions/<id>/reserve` |
| 8 | Reservation confirmation + cancellation | Dev | `GET /reservations/<id>`, cancel |
| 9 | Admin: create room | Dev | `GET/POST /admin/rooms/new` |
| 10 | Admin: open a session for a room | Dev | `GET/POST /admin/rooms/<id>/sessions/new` |
| 11 | Seed script with sample data for demos | Dev | `src/seed.py` |
| 12 | Record 2 meeting reports | Scrum | `meeting1.md`, `meeting2.md` |
| 13 | Write sprint review report | Scrum | `review.md` |
| 14 | Prepare 5' presentation / demo | Scrum | show the product working live |

Assign owners and move items across your GitHub Project board (To do /
In progress / Done) as your team works through them.
