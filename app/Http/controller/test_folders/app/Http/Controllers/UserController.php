use App\Http\Controllers\Controller;
use App\Models\Team;
use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        $users = User::latest()->get();

        return view('users', compact('users'));
    }

    public function show(User $user)
    {
        return view('users.show', compact('user'));
    }

    public function update(Request $request, User $user)
    {
        $validatedData = $request->validate([
            'team_id' => 'required',
            'profile' => 'required|string',
            'tags' => 'required|array',
        ]);

        $user->update($validatedData);

        return redirect()->route('users.index');
    }
}