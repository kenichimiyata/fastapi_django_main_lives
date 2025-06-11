<?php

namespace App\Listeners;

use App\Events\TrustdogEvent;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;

class TrustdogListener
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     *
     * @param  TrustdogEvent  $event
     * @return void
     */
    public function handle(TrustdogEvent $event)
    {
        // Implement logic to process service user data
        // For demonstration purposes, log a message
        \Log::info('Service user data processed successfully');
    }
}

**routes/web.php**