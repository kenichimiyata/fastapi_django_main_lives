use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\AwsS3v3\AwsS3Adapter;

class LineController extends Controller
{
    public function doPost(Request $request)
    {
        $type = $request->input('type');

        if ($type === 'image') {
            $file = $request->file('file');
            $filename = $file->getClientOriginalName();
            $filePath = $file->getPathname();

            Storage::disk('local')->put($filename, file_get_contents($filePath);

            $adapter = new AwsS3Adapter(
                new \Aws\S3\S3Client([
                        'version' => 'latest',
                        'region' => 'your-region',
                        'credentials' => [
                            'key' => 'your-key',
                            'secret' => 'your-secret-key',
                        ],
                    ]),
                    'your-bucket-name',
                    'your-prefix'
                );

            $adapter->write($filename, file_get_contents($filePath));

            return response()->json(['message' => 'Image uploaded successfully']);
        }

        return response()->json(['message' => 'Invalid request']);
    }
}