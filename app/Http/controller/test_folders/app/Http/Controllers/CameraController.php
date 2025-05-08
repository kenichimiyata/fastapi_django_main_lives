<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ServiceUser;

class CameraController extends Controller
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
     * Launch camera app and get ID.
     *
     * @return \Illuminate\Http\Response
     */
    public function launchCameraApp()
    {
        // Launch camera app and get ID
        $id = 'some_id';

        // Register ID to service_user table
        $serviceUser = new ServiceUser();
        $serviceUser->id = $id;
        $serviceUser->save();

        return response()->json(['message' => 'Camera app launched successfully']);
    }
}