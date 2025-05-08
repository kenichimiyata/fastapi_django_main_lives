<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\TrustDogApi;

class TrustDogApiController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * Get data from TrustDog API.
     *
     * @return \Illuminate\Http\Response
     */
    public function getDataFromTrustDogApi()
    {
        // Get data from TrustDog API
        $data = 'some_data';

        // Register data to service_user table
        $serviceUser = new ServiceUser();
        $serviceUser->data = $data;
        $serviceUser->save();

        return response()->json(['message' => 'Data retrieved successfully']);
    }
}