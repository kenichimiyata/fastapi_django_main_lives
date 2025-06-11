<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Eoc;
use App\Models\ServiceUser;

class WebhookController extends Controller
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
     * Handle webhook request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function handleWebhookRequest(Request $request)
    {
        // Get data from webhook request
        $data = $request->all();

        // Register data to eoc table
        $eoc = new Eoc();
        $eoc->data = $data;
        $eoc->save();

        // Get service user data
        $serviceUser = ServiceUser::where('id', $data['id'])->first();

        // Update service user data
        $serviceUser->data = $data;
        $serviceUser->save();

        return response()->json(['message' => 'Webhook request handled successfully']);
    }
}