import httpx
import json
from django.http import JsonResponse

# 서버는 도커 컨테이너 속 fastAPI로 띄워놓고 장고를 라우터처럼 씀(모델별 의존 패키지 요구 버전이 상이해서 일단 분리해놓음)
async def qwer(request):
    async with httpx.AsyncClient() as client:	# httpx 비동기 클라이언트(with 종료시 자동 연결 해제)
        data = json.loads(request.body)			# request의 body데이터는 {'base64img': 이미지문자열} 형태
        response = await client.post("http://192.168.0.91:5678/ktgmodel", content=data['base64img'], headers={"Content-Type": "text/plain"})
    return JsonResponse(response.json())		# {'emotion':감정, 'scores':수치 리스트} 형태 그대로 전달