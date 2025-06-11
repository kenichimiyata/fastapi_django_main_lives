<?php

namespace Tests\Unit;

use Tests\TestCase;
use App\Http\Controllers\WebhookController;

class WebhookTest extends TestCase
{
    /**
     * Test webhook controller.
     *
     * @return void
     */
    public function testWebhookController()
    {
        $webhookController = new WebhookController();
        $this->assertInstanceOf(WebhookController::class, $webhookController);
    }
}