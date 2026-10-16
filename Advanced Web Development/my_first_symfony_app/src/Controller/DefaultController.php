<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Attribute\Route;
use App\Entity\Announcement;
use App\Repository\AnnouncementRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpFoundation\Response;

class DefaultController extends AbstractController
{
    public function about()
    {
        return $this->render('default/about.html.twig');
    }

    #[Route('/hello/world')]

    public function helloAction()
    {
        return $this->render('default/hello.html.twig');
    }

    public function helloNameAction(string $name)
    {
        return $this->render('default/hello_name.html.twig', ['name' => $name]);
        
    }
    
    public function incrementAction(int $digit)
    {
        $result = $digit + 1;

        return $this->render('default/increment.html.twig', ['result' => $result]);
    }

    public function greetingAction(string $salutation, string $name)
    {
        return $this->render('default/greeting.html.twig', ['salutation' => $salutation, 'name' => $name]);
    }

    // GET follows the workshop example; a production creation endpoint should use POST.
    #[Route('/new_announcement/{message}', name: 'new_announcement', methods: ['GET'])]
    public function newAnnouncementAction(
        string $message,
        EntityManagerInterface $entityManager
    ): Response {
        $message = trim($message);

        if ($message === '') {
            return new Response('Message must not be blank.', Response::HTTP_BAD_REQUEST, [
                'Content-Type' => 'text/plain; charset=UTF-8',
            ]);
        }

        $announcement = new Announcement();
        $announcement->setMessage($message);
        $announcement->setTimestamp(new \DateTimeImmutable());

        $entityManager->persist($announcement);
        $entityManager->flush();

        return new Response('Saved announcement ID: '.$announcement->getId(), Response::HTTP_CREATED, [
            'Content-Type' => 'text/plain; charset=UTF-8',
        ]);
    }

    #[Route('/announcements', name: 'announcements', methods: ['GET'])]
    public function announcementsAction(AnnouncementRepository $repository): Response
    {
        return $this->render('default/announcements.html.twig', [
            'announcements' => $repository->findBy([], ['timestamp' => 'DESC', 'id' => 'DESC']),
        ]);
    }

    #[Route('/announcement/{id}', name: 'announcement_show', requirements: ['id' => '\d+'], methods: ['GET'])]
    public function announcementAction(string $id, AnnouncementRepository $repository): Response
    {
        $announcementId = filter_var($id, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);

        if ($announcementId === false) {
            throw $this->createNotFoundException('Announcement not found.');
        }

        $announcement = $repository->find($announcementId);

        if ($announcement === null) {
            throw $this->createNotFoundException('Announcement not found.');
        }

        return $this->render('default/announcement.html.twig', [
            'announcement' => $announcement,
        ]);
    }

    #[Route('/contacts')]
    public function contactsAction()
    {
        $contacts = [
    ['name' => 'Jane Smith', 'email' => 'jane@smith.com'],
    ['name' => 'John Smith', 'email' => 'john@smith.com'],
    ['name' => 'Bill Gates', 'email' => 'bill@microsoft.com'],
        ];


        dump($contacts);

        return $this->render('default/contacts.html.twig', ['contacts' => $contacts]);
    }
}
