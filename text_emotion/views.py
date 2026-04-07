from django.shortcuts import render

## Django modules
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
import os, json

#Django 라고 생각하고 views.py 에다가 들어갈 내용
import tensorflow as tf
import sentencepiece as spm
from tensorflow.keras.preprocessing.sequence import pad_sequences
# Create your views here.

max_len=100
@csrf_exempt
def Board_emotion(request):
    try:
        #param처리(POST가 아니면 오류 응답 json으로 처리)
        model = tf.keras.models.load_model("/home/ict/backend_ai/models/best_Text_emotion_model.keras")
        sp = spm.SentencePieceProcessor()
        sp.load("/home/ict/backend_ai/models/best_Text_emotion_model.model")
        if request.method != "POST":
            return JsonResponse({'error':"POST 방식만 허용하겠습니다"},status=405)
        body = json.loads(request.body.decode('utf-8'))
        sample_texts = [body.get('content',None)]
        sample_seq = [sp.encode_as_ids(text) for text in sample_texts]
        sample_pad = pad_sequences(sample_seq,maxlen=max_len)
        predicted = model.predict(sample_pad)
        print(predicted[0][0],type(predicted[0][0]))
        return JsonResponse({
            'input':sample_texts[0],
            "positive":float(f"{predicted[0][0]:.4f}"),
            "negative":float(f"{1 - predicted[0][0]:.4f}")
        },json_dumps_params={'ensure_ascii': False},status=200)
    
    except ValueError as e:
        return JsonResponse({"error":str(e)},status=400)
    except Exception as e:
        return JsonResponse({"error":f"Exception 이다 : {str(e)}"},status=500)