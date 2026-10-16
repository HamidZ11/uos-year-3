# Advanced Web Development: Symfony workshops

Symfony 7.4 workshop app covering routing, Twig, debugging and Doctrine ORM.
Tested with PHP 8.5. PHP needs PDO SQLite; the workshop checks also use DOM.
Install dependencies with Composer.

## Run a fresh checkout

From this project's directory:

```bash
cp .env.example .env
php -r 'file_put_contents(".env.local", "APP_SECRET=".bin2hex(random_bytes(32)).PHP_EOL, FILE_APPEND);'
composer install
php bin/console doctrine:migrations:migrate --no-interaction
php -S 127.0.0.1:8000 -t public
```

The database is created locally at `var/app.db`. SQLite does not need a
separate database server or the `doctrine:database:create` command.
Environment files containing local settings and secrets, the database,
caches and installed dependencies are excluded from Git.

## Workshop 5: announcements

| URL | Behaviour |
| --- | --- |
| `/new_announcement/Hello` | Save a message with the current server timestamp; return its generated ID |
| `/announcement/1` | Show announcement 1, or HTTP 404 if absent |
| `/announcements` | Show all messages, newest first |

The creation URL uses GET to follow the workshop example. Each visit or
refresh creates another row; a production creation endpoint should use POST.

## Checks

```bash
php tests/workshop_doctrine.php
php bin/console doctrine:schema:validate
php bin/console lint:twig templates
php bin/console lint:container
```

The workshop script runs migrations and 40 checks against a temporary SQLite
database. It does not change the application's database.

## Debugging and notes

The repository excludes personal editor settings. To reuse the shared
VS Code PHP debugger configurations with the DEVSENSE PHP Tools extension:

```bash
mkdir -p .vscode
cp docs/vscode-launch.example.json .vscode/launch.json
```

The **Listen for Xdebug** configuration uses loopback port 9003 and permits
stepping into Symfony's vendor code. Start a PHP server and the listener,
then visit `/contacts?XDEBUG_TRIGGER=1` with a breakpoint in `contactsAction()`.

- [Workshop 4: routing and debugging](wkshp_PDFs/workshop4-checks.md)
- [Workshop 5: Doctrine persistence](wkshp_PDFs/workshop5-checks.md)
