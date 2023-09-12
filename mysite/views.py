from django.views import View
import json
from django.http import JsonResponse
from .services.validate_client_response_service import Response
from .models import ClientResponse
from django.views.decorators.csrf import csrf_exempt
from .services.sms_service import SMS
from .services.slang_service import Slang
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
from .utils import covert_to_json_serializable


def find_slang(request):
    if request.method == 'GET':
        word = request.GET.get('word')
        lang = request.GET.get('lang')

        if not word or not lang:
            return JsonResponse({'error': 'Both word and lang are required.'}, status=400)

        try:
            slang = Slang.get_slang(word, lang)
            return JsonResponse({'slang': slang})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)


@csrf_exempt
def validate_and_create_response(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        name = request_body.get("name")
        monthly_income = request_body.get("monthly_income")
        monthly_savings = request_body.get("monthly_savings")
        phone_no = request_body.get("phone_no")
        email = request_body.get("email")
        country_code = request_body.get("country_code")

        try:
            result = Response.validate_response(name, monthly_income, monthly_savings, phone_no, email)
            if not result:
                ClientResponse.objects.create(name=name, monthly_income=monthly_income,
                                              monthly_savings=monthly_savings,
                                              phone_no=phone_no, email=email)
                SMS.send_sms(phone_no, country_code, request_body)
                return JsonResponse({'message': 'client response saved successfully'}, status=200)
            return JsonResponse({'error': result}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


def get_create_google_sheet_data(request):
    # Define the scope and credentials for Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'mysite/atlanbackendchallenge-398717-4e496bfb54ed.json', scope)

    # Authenticate with Google Sheets API
    gc = gspread.authorize(credentials)
    spreadsheet = gc.create('MyData Export')
    worksheet = spreadsheet.get_worksheet(0)

    # Fetch data from the database
    data = ClientResponse.objects.all()

    # Write data to the Google Sheet
    for i, obj in enumerate(data):
        worksheet.update_cell(i + 1, 1, obj.name)
        worksheet.update_cell(i + 1, 2, covert_to_json_serializable(obj.monthly_income))
        worksheet.update_cell(i + 1, 3, covert_to_json_serializable(obj.monthly_savings))
        worksheet.update_cell(i + 1, 4, obj.phone_no)
        worksheet.update_cell(i + 1, 5, obj.email)
    return JsonResponse({'google_sheets_url': spreadsheet.url})

