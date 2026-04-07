import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

MODEL_PATH = os.path.join('/home/ict/backend_ai/models/skin_model_final.keras')
model = load_model(MODEL_PATH)

CLASSES = ['건선', '아토피', '여드름', '염증성']


@csrf_exempt
def predict_skin(request):
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']

        img = Image.open(uploaded_file).convert('RGB')
        img = img.resize((256, 256))

        img_array = np.array(img, dtype='float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # (1, 256, 256, 3)

        predictions = model.predict(img_array)[0]
        predicted_idx = int(np.argmax(predictions))

        return JsonResponse({
            'success': True,
            'predicted_class': CLASSES[predicted_idx],
            'confidence': round(float(predictions[predicted_idx]) * 100, 1),
            'scores': {
                cls: round(float(prob) * 100, 1)
                for cls, prob in zip(CLASSES, predictions)
            }
        })

    return JsonResponse({'success': False, 'message': 'POST 방식으로 이미지를 전송해주세요'})
