<?php

use Illuminate\Support\Facades\Route;

Route::post('/camera/launch', 'CameraController@launchCameraApp');
Route::get('/trust-dog-api/data', 'TrustDogApiController@getDataFromTrustDogApi');
Route::post('/webhook', 'WebhookController@handleWebhookRequest');