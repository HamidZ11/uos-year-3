<?php

declare(strict_types=1);

use App\Entity\Announcement;
use App\Kernel;
use Doctrine\DBAL\Connection;
use Symfony\Bundle\FrameworkBundle\Console\Application;
use Symfony\Component\Console\Input\ArrayInput;
use Symfony\Component\Console\Output\BufferedOutput;
use Symfony\Component\Dotenv\Dotenv;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

require dirname(__DIR__).'/vendor/autoload.php';

(new Dotenv())->bootEnv(dirname(__DIR__).'/.env');
$databaseFile = tempnam(sys_get_temp_dir(), 'awd-doctrine-test-');

if ($databaseFile === false) {
    throw new RuntimeException('Could not create a temporary database.');
}

$databaseUrl = 'sqlite:///'.$databaseFile;
$_SERVER['DATABASE_URL'] = $_ENV['DATABASE_URL'] = $databaseUrl;
putenv('DATABASE_URL='.$databaseUrl);

$kernel = new Kernel('test', true);
$connection = null;
$pdo = null;
$checks = 0;

$check = static function (bool $condition, string $message) use (&$checks): void {
    if (!$condition) {
        throw new RuntimeException($message);
    }

    ++$checks;
};

$request = static function (string $path, string $method = 'GET') use ($kernel): Response {
    $request = Request::create('http://localhost'.$path, $method);
    $response = $kernel->handle($request);
    $kernel->terminate($request, $response);

    return $response;
};

$document = static function (Response $response): DOMDocument {
    $document = new DOMDocument();
    @$document->loadHTML('<?xml encoding="UTF-8">'.$response->getContent());

    return $document;
};

try {
    $kernel->boot();
    $manager = $kernel->getContainer()->get('doctrine')->getManager();
    $connection = $manager->getConnection();

    if (realpath($connection->getParams()['path'] ?? '') !== realpath($databaseFile)) {
        throw new RuntimeException('Refusing to run tests against a non-temporary database.');
    }

    $connection->getNativeConnection()->setAttribute(PDO::ATTR_TIMEOUT, 2);
    $application = new Application($kernel);
    $application->setAutoExit(false);
    $output = new BufferedOutput();
    $exitCode = $application->run(new ArrayInput([
        'command' => 'doctrine:migrations:migrate',
        '--no-interaction' => true,
    ]), $output);
    $check($exitCode === 0, 'Migrations failed: '.$output->fetch());
    $pdo = new PDO('sqlite:'.$databaseFile, null, null, [PDO::ATTR_TIMEOUT => 2]);

    $response = $request('/announcements');
    $check($response->getStatusCode() === 200, 'Empty announcement list must return HTTP 200.');
    $check(str_contains($response->getContent(), 'No announcements yet.'), 'Empty list message is missing.');
    $check($request('/announcement/1')->getStatusCode() === 404, 'An absent announcement must return HTTP 404.');

    $message = "  Workshop café's <img src=x onerror=alert(1)>  ";
    $earliest = time();
    $response = $request('/new_announcement/'.rawurlencode($message));
    $check($response->getStatusCode() === 201, 'Creation must return HTTP 201.');
    $check(str_starts_with($response->headers->get('Content-Type', ''), 'text/plain'), 'Creation response must be plain text.');
    $check(preg_match('/^Saved announcement ID: (\d+)$/', $response->getContent(), $matches) === 1, 'Creation response must contain the generated ID.');
    $id = (int) $matches[1];
    $statement = $pdo->prepare('SELECT * FROM announcements WHERE id = ?');
    $statement->execute([$id]);
    $row = $statement->fetch(PDO::FETCH_ASSOC);
    $statement->closeCursor();
    $check($row !== false && $row['message'] === trim($message), 'The database must preserve the message text.');
    $timestamp = new DateTimeImmutable($row['timestamp']);
    $check($timestamp->getTimestamp() >= $earliest && $timestamp->getTimestamp() <= time(), 'Timestamp must be set automatically to the current server time.');

    $response = $request('/announcement/'.$id);
    $check($response->getStatusCode() === 200, 'Existing announcement must return HTTP 200.');
    $html = $document($response);
    $check($html->getElementsByTagName('p')->item(0)?->textContent === trim($message), 'Detail page must show the saved message.');
    $check($html->getElementsByTagName('img')->length === 0, 'Detail page must escape message HTML.');
    $check($html->getElementsByTagName('time')->item(0)?->textContent === $row['timestamp'], 'Detail page must show the saved timestamp.');
    $check(str_contains($response->getContent(), 'href="/announcements"'), 'Detail page needs a link back to the list.');

    $check($request('/new_announcement/%20%20%20')->getStatusCode() === 400, 'Blank message must return HTTP 400.');
    $check($request('/new_announcement/')->getStatusCode() === 404, 'Missing message must return HTTP 404.');
    $check($request('/new_announcement/Unexpected', 'POST')->getStatusCode() === 405, 'Unsupported creation method must return HTTP 405.');
    $check((int) $pdo->query('SELECT COUNT(*) FROM announcements')->fetchColumn() === 1, 'Rejected requests must not create rows.');

    foreach (['0', '-1', 'abc', '1.5', '999999999999999999999999', '999999'] as $invalidId) {
        $check($request('/announcement/'.$invalidId)->getStatusCode() === 404, 'Invalid or absent ID must return HTTP 404: '.$invalidId);
    }

    $response = $request('/new_announcement/Second');
    $check($response->getStatusCode() === 201, 'A second announcement must be saved.');
    $check(preg_match('/^Saved announcement ID: (\d+)$/', $response->getContent(), $matches) === 1 && (int) $matches[1] > $id, 'Each announcement needs a new generated ID.');
    $secondId = (int) $matches[1];
    $check((int) $pdo->query('SELECT COUNT(*) FROM announcements')->fetchColumn() === 2, 'Exactly two announcements should have been saved.');

    $response = $request('/announcements');
    $check($response->getStatusCode() === 200, 'Populated list must return HTTP 200.');
    $html = $document($response);
    $xpath = new DOMXPath($html);
    $rows = $xpath->query('//tbody/tr');
    $check($rows->length === 2, 'List must display every announcement.');
    $check(trim($rows->item(0)->getElementsByTagName('td')->item(0)->textContent) === (string) $secondId, 'List must show newest announcements first.');
    $check(trim($rows->item(1)->getElementsByTagName('td')->item(1)->textContent) === trim($message), 'List must preserve message text.');
    $check($html->getElementsByTagName('img')->length === 0, 'List must escape message HTML.');
    $check(str_contains($response->getContent(), 'href="/announcement/'.$id.'"'), 'List must link to individual announcements.');
    $check(!str_contains($response->getContent(), 'No announcements yet.'), 'Populated list must not show its empty state.');
    $check($request('/announcements', 'POST')->getStatusCode() === 405, 'List must reject unsupported methods.');
    $check($request('/announcement/'.$id, 'POST')->getStatusCode() === 405, 'Detail page must reject unsupported methods.');

    $manager = $kernel->getContainer()->get('doctrine')->getManager();
    $manager->clear();
    $announcement = $manager->find(Announcement::class, $id);
    $check($announcement instanceof Announcement && $announcement->getTimestamp() instanceof DateTimeImmutable, 'Doctrine must reload the saved object with an immutable timestamp.');
    $router = $kernel->getContainer()->get('router');
    $check($router->match('/contacts')['_controller'] === 'App\\Controller\\DefaultController::contactsAction', 'Existing contacts route must keep its controller.');
    $check($request('/hello/world')->getStatusCode() === 200, 'Existing static route must still work.');
    $check(str_contains($request('/increment/9')->getContent(), '<h1>10</h1>'), 'Existing increment route must still work.');

    echo "PASS: {$checks} checks covering migrations, persistence, retrieval, validation, escaping and existing routes.\n";
    echo "All test data was stored in a temporary database; the project database was unchanged.\n";
} finally {
    $kernel->shutdown();

    if ($connection instanceof Connection) {
        $connection->close();
    }

    $pdo = null;
    unlink($databaseFile);
}
