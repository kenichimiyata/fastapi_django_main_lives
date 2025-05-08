<?php

namespace App\Traits;

trait TrustdogTrait
{
    /**
     * @return array
     */
    private function getServiceUserFromApi()
    {
        // Implement API call to get service user
        // For demonstration purposes, return a dummy array
        return [
            'id' => 1,
            'name' => 'John Doe',
            'email' => 'johndoe@example.com',
        ];
    }
}

**app/Events/TrustdogEvent.php**