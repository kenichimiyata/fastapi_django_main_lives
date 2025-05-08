use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Storage;

class User extends Model
{
    protected $fillable = [
        'name',
        'email',
        'team_id',
        'profile',
        'tags',
    ];

    public function team()
    {
        return $this->belongsTo(Team::class);
    }
}