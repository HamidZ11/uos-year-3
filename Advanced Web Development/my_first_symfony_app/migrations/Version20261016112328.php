<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20261016112328 extends AbstractMigration
{
    public function getDescription(): string
    {
        return 'Rename announcement to announcements while preserving existing data';
    }

    public function up(Schema $schema): void
    {
        $this->addSql('ALTER TABLE announcement RENAME TO announcements');
    }

    public function down(Schema $schema): void
    {
        $this->addSql('ALTER TABLE announcements RENAME TO announcement');
    }
}
