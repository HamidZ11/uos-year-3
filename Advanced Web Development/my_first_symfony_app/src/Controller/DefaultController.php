<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Attribute\Route;

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
