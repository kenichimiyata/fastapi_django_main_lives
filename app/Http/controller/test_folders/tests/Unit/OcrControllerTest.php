namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Http\Controllers\OcrController;
use App\Http\Requests\ImageUploadRequest;

class OcrControllerTest extends TestCase
{
    use RefreshDatabase;

    /**
     * @test
     */
    public function test_store()
    {
        $request = new ImageUploadRequest();
        $request->image = UploadedFile::fake()->image('test.jpg', 100, 100);
        $response = (new OcrController())->store($request);
        $this->assertEquals(201, $response->getStatusCode());
    }

    /**
     * @test
     */
    public function test_index()
    {
        factory(PhotoJudgement::class, 10)->create();
        $response = (new OcrController())->index();
        $this->assertEquals(200, $response->getStatusCode());
        $this->assertCount(10, $response->json());
    }
}