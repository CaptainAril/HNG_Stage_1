from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from ipware import get_client_ip
import requests
import os


class status(View):
    def get(self, request):
        return JsonResponse(data={"status":"OK", "code":200})

class hello(View):
    w_key = os.getenv('w_key')
    def get(self, request):
        # name = request.GET['visitor_name']
        name = request.GET.get('visitor_name')
        name = f', {name}' if name else ''
        temperature = '100'
        ip = '41.58.229.34'
        # ip, is_routable = get_client_ip(request)
        location, temperature = self.get_weather(ip)
        # location = 'Junsu' 
        # request.
        res = {
            "client_ip": ip,
            "location": location,
            "greeting": f"Hello{name}!, the temperature is {temperature} degrees Celcius in {location}"
            }
        return JsonResponse(res, status=200)
    
    def get_weather(self, ip_address: str):
        # q=41.58.229.34&key=c217450162e94226aa633351240207
        # https://api.weatherapi.com/v1/current.json?q=41.58.229.34&key=c217450162e94226aa633351240207

        params = {'key':self.w_key, 'q':ip_address}
        r = requests.get('https://api.weatherapi.com/v1/current.json', params=params)
        print(r.json())
        res = r.json()
        region = res.get('location').get('region')
        temperature = res.get('current').get('temp_c')
        return region, temperature




@requires_csrf_token
def custom_404(request, exception=None):
    return JsonResponse({"error": "Invalid Enpoint!", "msg":"Correct usage: <example.com>/api/hello?visitor_name=<name>"}, status=404)

@requires_csrf_token
def custom_405(request, exception=None):
    return JsonResponse({"error":"Method not allowed for endpoint!"}, status=405)



# {
#   "client_ip": "127.0.0.1", // The IP address of the requester
#   "location": "New York" // The city of the requester
#   "greeting": "Hello, Mark!, the temperature is 11 degrees Celcius in New York"
# }