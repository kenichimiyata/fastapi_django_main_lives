namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Requests\ImageUploadRequest;
use thiagoalessio\TesseractOCR\TesseractOCR;

class OcrController extends Controller
{
        /**
         * @param ImageUploadRequest $request
         * @return \Illuminate\Http\JsonResponse
         */
        public function store(ImageUploadRequest $request)
        {
            $image = $request->file('image');
            $filePath = $image->store('photos');
            $text = (new TesseractOCR(storage_path('app/' . $filePath)))->run();
            $judgement = $this->judge($text);
            $photoJudgement = new PhotoJudgement();
            $photoJudgement->image_path = $filePath;
            $photoJudgement->ocr_text = $text;
            $photoJudgement->is_identified = $judgement;
            $photoJudgement->save();
            return response()->json([
                'result' => $judgement ? '身分証' : 'Unknown',
                'text' => $text,
                'file_path' => $filePath
            ]);
        }

        /**
         * @return \Illuminate\Http\JsonResponse
        */
        public function index()
        {
            $photoJudgements = PhotoJudgement::all();
            return response()->json($photoJudgements);
        }

        /**
         * @param string $text
         * @return bool
         */
        private function judge($text)
        {
            $keywords = [
                '運転免許証',
                '健康保険証',
                'マイナンバー',
                '個人番号',
                '有効期限',
                '氏名',
                '生年月日'
            ];
            foreach ($keywords as $keyword) {
                if (strpos($text, $keyword) !== false) {
                    return true;
                }
            }
            return false;
        }
    }