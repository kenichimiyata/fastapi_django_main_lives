use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;

class CreatePhotoJudgementsTable extends Migration
{
    /**
     * @return void
     */
    public function up()
    {
        Schema::create('photo_judgements', function (Blueprint $table) {
            $table->id();
            $table->string('image_path');
            $table->text('ocr_text');
            $table->boolean('is_identified');
            $table->timestamps();
        });
    }

    /**
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('photo_judgements');
    }
}