<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Eoc;
use App\Models\ServiceUser;
use App\Models\TrustDogApi;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // Seed eoc table
        Eoc::factory()->count(10)->create();

        // Seed service_user table
        ServiceUser::factory()->count(10)->create();

        // Seed trust_dog_api table
        TrustDogApi::factory()->count(10)->create();
    }
}