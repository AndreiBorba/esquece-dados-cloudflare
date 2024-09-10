from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

headers_yc_core_dcg = {
    'Host': 'youcom.layer.core.dcg.com.br',
    'Content-Type': 'application/json',
    'User-Agent': 'YouCom/1 CFNetwork/1121.2.1 Darwin/19.2.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-us',
    'Authorization': str(os.getenv('URL_AUTHORIZATION')),
    'Cookie': str(os.getenv('URL_COOKIE'))
}

@csrf_exempt
def consultar_cliente(request):
    if request.method == 'POST':
        document_number = request.POST.get('document_number')
        url = str(os.getenv('URL_SEARCH_CUSTOMER'))
        headers = headers_yc_core_dcg
        body = {
            "Page": {
                "PageIndex": 0,
                "PageSize": 0
            },
            "Where": f'DocumentNumber = "{document_number}"'
        }
        response = requests.post(url=url, json=body, headers=headers)
        result = response.json()
        return JsonResponse(result)

@csrf_exempt
def esquecer_cliente(request):
    customer_id = request.POST.get('globalCustomerId')
    url = str(os.getenv('URL_ANONYMIZE_CUSTOMER'))
    headers = headers_yc_core_dcg
    body = customer_id
    response = requests.post(url=url, json=body, headers=headers)
    result = {}
    if response.status_code == 200:
        result = response.json()
        if not result['Errors'] and result['IsValid']:
            return JsonResponse(result)
        else:
            print(
                f"|e|anonymanizeCustomer|erro ao anonimizar cliente {body}: {result['Errors'][0]['ErrorMessage']}")
            result = {}
            return JsonResponse(result)
    else:
        print(f"|e|anonymanizeCustomer|endpoint indisponivel|codigo de erro [{response.status_code}]: {response}")
        return JsonResponse(result)

def index(request):
    return render(request, 'inicio/index.html')
