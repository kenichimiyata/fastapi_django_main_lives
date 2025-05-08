<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Http\Controllers\WebhookController;

class WebhookTest extends TestCase
{
    /**
     * Test handle webhook request.
     *
     * @return void
     */
    public function testHandleWebhookRequest()
    {
        $response = $this->post('/webhook', [
            'id' => 'some_id',
            'data' => 'some_data',
        ]);

        $response->assertStatus(200);**
    }
}