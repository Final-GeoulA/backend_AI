from PIL import Image
import numpy as np
import cv2
import os
from insightface.app import FaceAnalysis
from tensorflow.keras.models import load_model

# Django module
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile

app = FaceAnalysis(allowed_modules=['detection','recognition'],providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0,det_thresh=0.5,det_size=(640,640))

MASK_MODEL_PATH = os.path.join('/home/ict/backend_ai/recogface/models/MaskModel.keras')
mask_model = load_model(MASK_MODEL_PATH)

ref_img1 = cv2.imread('/home/ict/backend_ai/recogface/images/admin1.jpg')
ref_img2 = cv2.imread('/home/ict/backend_ai/recogface/images/admin2.jpg')
ref_img3 = cv2.imread('/home/ict/backend_ai/recogface/images/admin3.png')
ref_faces1 = app.get(ref_img1)
ref_faces2 = app.get(ref_img2)

ref_faces3 = app.get(ref_img3)
ref_face1 = ref_faces1[0] if ref_faces1 else None
ref_face2 = ref_faces2[0] if ref_faces2 else None
ref_face3 = ref_faces3[0] if ref_faces3 else None
admin_faces = [ref_face1,ref_face2,ref_face3]
admin_faces = [{'name':'admin1','img':ref_face1},
               {'name':'admin2','img':ref_face2},
               {'name':'admin3','img':ref_face3}]

def check_mask(img):
    """
    이미지를 받아 마스크 착용 여부를 반환하는 별도 메서드.
    True: 마스크 착용 (또는 착용 확률이 높음)
    False: 마스크 미착용
    """
    try:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized_img = cv2.resize(rgb_img, (224, 224))
        # 모델 입력 사이즈에 맞게 리사이즈 (예: 224x224) 
        # ※ 주의: 학습하신 MaskModel.keras의 input shape에 맞춰 수정해야 합니다!
        
        # 정규화 및 차원 추가 (Keras 모델 예측용)
        img_array = np.expand_dims(resized_img, axis=0)
        img_array = img_array.astype('float32') / 255.0
        
        # 예측 (이진 분류라고 가정: 0.5 이상이면 마스크, 미만이면 노마스크 등)
        prediction = mask_model.predict(img_array)[0][0]
        
        # 기준값(Threshold)에 따라 판별 (학습 방식에 따라 0과 1의 의미가 다를 수 있으니 확인 필요)
        is_masked = prediction < 0.5
        print(prediction)
        print(is_masked)
        return is_masked
    except Exception as e:
        print(f"Mask check error: {e}")
        return False # 에러 시 기본값 처리

# Django와 React간의 파일 업로드 *****
@csrf_exempt
def compare_face(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # 업로드된 파일을 읽기
        uploaded_file:InMemoryUploadedFile = request.FILES['image']
        # 바이트로 읽어들인 값을 numpy Array변환
        file_bytes = np.array(bytearray(uploaded_file.read()),dtype=np.uint8)
        img = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
        
        if check_mask(img):
            return JsonResponse({
                'success': False, 
                'message': '마스크가 감지되었습니다. 마스크를 벗고 다시 시도해주세요.'
            })
        
        # FaceAnalysis 에 등록
        faces = app.get(img)
        if not faces:
            return JsonResponse({'success':False,'message':'얼굴을 감지하지 못했습니다.'})

        face = faces[0]
        similarities = []
        for i in range(len(admin_faces)):
            similarities.append(float(np.dot(admin_faces[i]['img'].normed_embedding, face.normed_embedding)))
        similarity = max(similarities)
        adminarg = np.argmax(np.array(similarities))
        result_text = "ok" if similarity > 0.6 else "fail"

        return JsonResponse({
            'success':True,
            'similarity':round(similarity,4),
            'result':result_text,
            'admin_name':admin_faces[adminarg]['name'],
            'bbox':face.bbox.astype(int).tolist()
        })

    return JsonResponse({'success':False,'message':'POST 방식으로 이미지 파일을 전송해주세요'})