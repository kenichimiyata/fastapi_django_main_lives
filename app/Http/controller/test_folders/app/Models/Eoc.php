<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Eoc extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'eoc';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'data',
    ];
}