# Software Requirements Specification

**Project:** Escape-Room Creation and Management System
**Course:** Ingeniería del Software — UPV, Campus d'Alcoi
**Version:** 1.0 (Sprint 1)

This document will be revised at the end of every sprint as the product
backlog evolves, in line with the Scrum methodology followed in this
course. This first version covers what was analyzed and built during
Sprint 1.

## 1. Introduction

### 1.1 Purpose

The purpose of this system is to help an escape-room company manage its
rooms, time slots and reservations, while giving customers a simple way to
browse the available escape rooms and book a session for their group.

### 1.2 Scope

For Sprint 1 we chose to build a **general booking system for an
escape-room company that operates several physical rooms**, rather than a
single themed room or a fully virtual/online puzzle experience. This was
the natural starting point because booking and availability management are
needed regardless of which room or theme is involved, and every later
feature (puzzles, scoring, team management, etc.) builds on top of having
rooms, sessions and reservations in place.

### 1.3 Intended audience

This document is aimed at the development team, the course instructor
acting as stakeholder, and anyone who wants to understand what the system
does and why, at this stage of the project.

## 2. Overall description

### 2.1 Actors

- **Player / Customer** — browses rooms, checks availability and books a
  session for their team. No account is required yet in Sprint 1; the
  person booking identifies themselves with their name and email as the
  team leader.
- **Admin** — manages the catalog of escape rooms and opens new sessions
  (time slots) for customers to book.

### 2.2 Product perspective

This is a new, standalone web application. It is not replacing an existing
system. It is built with Python (Flask) and a local SQLite database, kept
deliberately simple so the whole team can read, run and extend it without
a steep learning curve.

### 2.3 Assumptions and dependencies

- A session (time slot) belongs to exactly one room.
- A reservation always belongs to exactly one session and one team.
- Payments are out of scope for the whole project; the brief does not ask
  for them and the company is assumed to handle payment on-site.

## 3. Functional requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR1 | Admin can create a new escape room (name, theme, description, min/max players, duration, difficulty, price). | Done |
| FR2 | Admin can open a new session (date/time + capacity) for a room. | Done |
| FR3 | Customer can see the list of all escape rooms. | Done |
| FR4 | Customer can see the details of a room and its upcoming available sessions. | Done |
| FR5 | Customer can book a session for a team, giving a team name, leader name/email/phone and party size. | Done |
| FR6 | The system must not allow a booking that exceeds the remaining capacity of a session. | Done |
| FR7 | A session is automatically marked "full" once its capacity is reached, and reopens if a reservation on it is cancelled. | Done |
| FR8 | Customer (or admin) can cancel an existing reservation. | Done |
| FR9 | Customer accounts / authentication (players and admin log in). | Planned — later sprint |
| FR10 | Puzzles/challenges content and in-game progress tracking. | Planned — later sprint |
| FR11 | Scores and results per team/session. | Planned — later sprint |
| FR12 | Resource management (props/equipment per room). | Planned — later sprint |
| FR13 | Cancellation policies (e.g. deadlines, refund rules). | Planned — later sprint |

Requirements FR9–FR13 come directly from the full feature list in the
assignment brief (customers, rooms, sessions, reservations, teams,
puzzles, resources, availability, cancellations, scores). We deliberately
scoped Sprint 1 to FR1–FR8, since they form the minimum booking flow that
everything else depends on.

## 4. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR1 | **Usability** — a new visitor should be able to go from the room list to a confirmed reservation in under a minute, without instructions. |
| NFR2 | **Portability** — the system must run on any machine with Python 3 installed (Windows, macOS, Linux), with no external services required for Sprint 1. |
| NFR3 | **Maintainability** — code is organized by responsibility (`models.py` for data, `app.py` for routes, `templates/` for views) so any team member can find and change a feature without reading the whole codebase. |
| NFR4 | **Data integrity** — the database must never show negative availability or let two reservations silently overbook the same session. |
| NFR5 | **Performance** — typical pages (room list, room detail, booking form) should load in well under a second on a local/dev setup, since Sprint 1 targets a single-machine prototype, not production load. |
| NFR6 | **Security** — out of scope for Sprint 1 (no accounts exist yet), but planned once authentication (FR9) is introduced: passwords must be hashed, and the admin area must not be publicly reachable. |

## 5. Data model (Sprint 1)

- **EscapeRoom** — name, theme, description, min/max players, duration,
  difficulty, price per person.
- **GameSession** — belongs to a room; date/time, capacity, status
  (available / full / cancelled).
- **Team** — name, leader name, leader email, leader phone.
- **Reservation** — links a team to a session; party size, status
  (confirmed / cancelled), creation timestamp.

This model will grow in later sprints — for example `Puzzle` and `Score`
entities are expected once FR10/FR11 are tackled.

## 6. Out of scope for Sprint 1

- Login / accounts for players and admin.
- Puzzles, hints, and in-game content.
- Scoring and leaderboards.
- Payment processing.
- Email/SMS notifications for bookings.

These are not forgotten — they are simply scheduled for Sprints 2–5, as
the course brief expects each sprint to add new requirements on top of a
working product.
