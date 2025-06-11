namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ImageUploadRequest extends FormRequest
{
    public function rules()
    {
        return [
            'image' => 'required|image|mimes:jpg,jpeg,png|max:2048',
        ];
    }
}