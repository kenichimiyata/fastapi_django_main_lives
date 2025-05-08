<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TrustDogApi extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'trust_dog_api';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'data',
    ];
}