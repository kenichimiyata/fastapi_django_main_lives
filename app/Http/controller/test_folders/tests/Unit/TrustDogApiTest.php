<?php

namespace Tests\Unit;

use Tests\TestCase;
use App\Models\TrustDogApi;

class TrustDogApiTest extends TestCase
{
    /**
     * Test trust dog api model.
     *
     * @return void
     */
    public function testCreateTrustDogApi()
    {
        $trustDogApi = new TrustDogApi();
        $this->assertInstanceOf(TrustDogApi::class, $trustDogApi);
    }
}