use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class LoginController extends Controller
{
    public function create()
    {
        return view('login');
    }

    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'email' => 'required|string|email|max:255',
            'password' => 'required|string|min:8',
        ]);

        if (!auth()->attempt($validatedData)) {
            return back()->withErrors(['email' => 'Invalid credentials']);
        }

        return redirect()->route('users.index');
    }
}