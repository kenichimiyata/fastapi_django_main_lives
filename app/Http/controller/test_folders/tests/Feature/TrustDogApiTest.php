<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Http\Controllers\TrustDogApiController;

class TrustDogApiTest extends TestCase
{
    /**
     * Test get data from TrustDog API.
     *
     * @return void
     */
    public function testGetDataFromTrustDogApi()
    {
        $response = $this->get('/trust-dog-api/data');

        $response->assertStatus(200);
    }
}