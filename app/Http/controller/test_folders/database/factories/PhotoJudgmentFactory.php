namespace Database\Factories;

use App\Models\PhotoJudgment;
use Illuminate\Database\Eloquent\Factories\Factory;

class PhotoJudgmentFactory extends Factory
{
    protected $model = PhotoJudgment::class;

    public function definition()
    {
        return [
            'image_path' => 'storage/photos/test.jpg',
            'ocr_text' => 'This is a test text',
            'is_identified' => true
        ];
    }
}