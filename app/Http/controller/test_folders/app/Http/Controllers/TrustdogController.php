<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ServiceUser;
use App\Traits\TrustdogTrait;

class TrustdogController extends Controller
{
    /**
     * @param Request $request
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        // Get service user from Trustdog API
        $serviceUser = $this->getServiceUserFromApi();

        // Register service user in database
        $serviceUserModel = new ServiceUser();
        $serviceUserModel->fill($serviceUser);
        $serviceUserModel->save();

        // Return response
        return response()->json(['message' => 'Service user registered successfully']);
    }

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
            'email' => 'johndoe@example.com'
        ];
    }
}

**app/Http/Webhooks/TrustdogWebhookController.php**