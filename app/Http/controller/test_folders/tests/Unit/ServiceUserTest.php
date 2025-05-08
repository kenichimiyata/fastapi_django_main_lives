<?php

namespace Tests\Unit;

use Tests\TestCase;
use App\Models\ServiceUser;

class ServiceUserTest extends TestCase
{
    /**
     * Test service user model.
     *
     * @return void
     */
    public function testCreateServiceUser()
    {
        $serviceUser = new ServiceUser();
        $this->assertInstanceOf(ServiceUser::class, $serviceUser);
    }
}