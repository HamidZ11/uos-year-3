# Workshop 4: routing and debugging

Checked on 16 October 2026 with Symfony 7.4, PHP 8.5 and Xdebug 3.

## Routes

| URL | Expected output |
| --- | --- |
| `/hello/world` | Welcome to AWD. |
| `/hello/Sam` | Hello Sam |
| `/hi/John` | hi John |
| `/welcome/Jane` | welcome Jane |
| `/increment/0` | 1 |
| `/increment/9` | 10 |
| `/contacts` | Table with the three workshop contacts |

The static attribute routes load first. In `config/routes.yaml`,
`hello_name` precedes `greeting` so its controller action remains reachable.
The greeting pattern still accepts only `hello`, `hi` or `welcome`;
`hello` URLs are handled by the earlier, more specific route.

All ten single digits were checked. Multiple digits, negative numbers,
letters, decimals, unsupported salutations and extra path segments were rejected.

## Profiler and logging

- WebProfilerBundle is enabled only in development and test environments.
- `/contacts` calls `dump($contacts)` before rendering a complete HTML page.
- A real HTTP request produced the toolbar and a working Profiler dump panel
  containing all three contacts.
- Monolog is installed and configured by its standard Symfony recipe.
  Development requests write to `var/log/dev.log`.
- `php bin/console server:dump` is available as an alternative dump viewer.
- Production routes were checked: no Profiler routes were registered.

## Xdebug

The project uses the existing DEVSENSE PHP Tools extension in VS Code.
The debug configurations explicitly listen on loopback port `9003` and allow
stepping into vendor code, including Symfony's `render()` method.

For the existing Symfony development server:

1. Set a breakpoint on the `return $this->render(...)` line in `contactsAction()`.
2. Select **Listen for Xdebug** in VS Code's Run and Debug panel, then start it.
3. Visit `http://localhost:8000/contacts?XDEBUG_TRIGGER=1`.
4. Inspect `$contacts`, then use **Step Into** to enter `render()`.

The URL parameter triggers Xdebug directly, so a browser helper is not needed
for this workflow. The handout's older `xdebug.remote_*` settings are for
Xdebug 2; this installation uses Xdebug 3's `xdebug.client_*` settings.

A direct DBGp verification against a real HTTP request successfully hit the
controller breakpoint, inspected the three-element contacts array and call
stack, stepped into `render()` and resumed the request to an HTTP 200 response.
This verified the debugging engine independently of the editor UI. A graphical
VS Code/PhpStorm session and browser helper installation were not verified.

The answer to exercise 7 is:
`Symfony\Bundle\FrameworkBundle\Controller\AbstractController`.

## Configuration checks

Passed YAML linting, Twig linting, service-container linting and
`composer validate --no-check-publish`. Composer reported no known security
advisories when installing the logging bundle.

Reference documentation:
[Symfony routing](https://symfony.com/doc/7.4/routing.html),
[Symfony logging](https://symfony.com/doc/7.4/logging.html),
[PHP Tools launch profiles](https://docs.devsense.com/vscode/debug/launch-json/),
[Xdebug step debugging](https://xdebug.org/docs/step_debug).
