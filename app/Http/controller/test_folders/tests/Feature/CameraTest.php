<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Http\Controllers\CameraController;

class CameraTest extends TestCase
{
    /**
     * Test launch camera app.
     *
     * @return void
     */
    public function testLaunchCameraApp()
    {
        $response = $this->post('/camera/launch');

        $response->assertStatus(200);
    }
}