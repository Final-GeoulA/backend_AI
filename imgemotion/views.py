from django.http import JsonResponse
import urllib.request # 이건 모델 불러올 때(fer = HSEmotionRecognizer(model_name='enet_b0_8_best_afew')) 내부에서 쓰임
from hsemotion_onnx.facial_emotions import HSEmotionRecognizer
import base64
import numpy as np
import cv2
from django.views.decorators.csrf import csrf_exempt

face_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fer = HSEmotionRecognizer(model_name='enet_b0_8_best_afew')

@csrf_exempt
def predict_emotion(request):
	if request.method == 'POST' and 'image' in request.FILES:
		uploaded_file = request.FILES['image']

		np_arr = np.frombuffer(uploaded_file.read(), np.uint8)
		img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5)

		if len(faces) == 0:
			return JsonResponse({'success': False,'message': '얼굴 못찾음'})
		x, y, w, h = faces[0]
		face_img = img_rgb[y:y+h, x:x+w]
		emotion, scores = fer.predict_emotions(face_img, logits=False)
		return JsonResponse({'success': True, 'emotion': emotion, 'scores': scores.tolist()})
	return JsonResponse({'success': False, 'message': 'POST 방식으로 이미지를 전송해주세요'})