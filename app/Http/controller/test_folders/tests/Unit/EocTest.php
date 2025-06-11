<?php

namespace Tests\Unit;

use Tests\TestCase;
use App\Models\Eoc;

class EocTest extends TestCase
{
    /**
     * Test eoc model.
     *
     * @return void
     */
    public function testCreateEoc()
    {
        $eoc = new Eoc();
        $this->assertInstanceOf(Eoc::class, $eoc);
    }
}