#!/bin/bash

# Install dependencies
php composer.phar install

# Run the Laravel application
php artisan serve
