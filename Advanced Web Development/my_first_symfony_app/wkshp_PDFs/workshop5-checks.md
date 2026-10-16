# Workshop 5: Doctrine persistence

Completed on 16 October 2026 using SQLite with Symfony 7.4.

## Completed exercises

- Installed Doctrine ORM, Doctrine migrations and MakerBundle.
- Configured SQLite through `DATABASE_URL` in `.env.local`.
- Created `Announcement` with an automatically generated ID, required text
  `message` and required `DateTimeImmutable` `timestamp`.
- Created the initial table through a migration.
- Added `#[ORM\Table(name: 'announcements')]` and applied a second migration.
  The migration renames the existing table instead of dropping its data;
  its rollback renames the table back.
- Added creation through `/new_announcement/{message}` with the server's
  current date and time, `persist()` and `flush()`.
- Added a repository-backed page for a single announcement and a Twig table
  showing all announcements, newest first.
- Handled blank messages, unknown/invalid IDs and an empty announcement list.

## Routes

| Method | URL | Behaviour |
| --- | --- | --- |
| GET | `/new_announcement/Hello` | Save a new announcement; return HTTP 201 and its generated ID |
| GET | `/announcement/1` | Display announcement 1, or HTTP 404 if absent |
| GET | `/announcements` | Display every announcement |

Creation uses GET to match the workshop's demonstration URL. Each visit or
refresh creates another row. A production creation endpoint should use POST.
The pages escape announcement text through Twig's normal HTML escaping.

## SQLite setup difference

The installed DBAL 4 version does not support `doctrine:database:create` for
SQLite. Opening a connection creates its database file automatically:

```bash
php bin/console dbal:run-sql "SELECT 1 AS connection_ok"
```

The database is stored in `var/app.db`. Inspect its table structure with:

```bash
php bin/console dbal:run-sql "SELECT name, type, [notnull] AS required, pk AS primary_key FROM pragma_table_info('announcements')"
```

## Verification

Run the workshop checks with:

```bash
php tests/workshop_doctrine.php
```

The script uses a temporary SQLite database and runs the actual migrations.
It checks creation, generated IDs, automatic timestamps, persisted text,
retrieval, newest-first ordering, empty results, invalid IDs, rejected inputs,
HTML escaping and existing routes. All 40 checks passed.
The script does not change the project's database.

PHP, Twig and service-container linting passed. The project's applied
migrations and Doctrine schema were checked against the entity mapping.

## Files

- `src/Entity/Announcement.php`: entity and database mapping.
- `src/Repository/AnnouncementRepository.php`: Doctrine repository.
- `src/Controller/DefaultController.php`: creation and retrieval actions.
- `templates/default/announcement.html.twig`: individual announcement.
- `templates/default/announcements.html.twig`: announcement table.
- `migrations/`: initial table creation and table rename.

Reference: [Symfony's Doctrine documentation](https://symfony.com/doc/7.4/doctrine.html).
