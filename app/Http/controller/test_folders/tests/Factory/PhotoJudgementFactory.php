namespace Tests\Factory;

use App\Models\PhotoJudgement;
use Illuminate\Database\Eloquent\Factories\Factory;

class PhotoJudgementFactory extends Factory
{
    protected $model = PhotoJudgement::class;

    public function definition()
    {
        return [
            'image_path' => 'test.jpg',
            'ocr_text' => 'This is a test',
            'is_identified' => true
        ];
    }
}