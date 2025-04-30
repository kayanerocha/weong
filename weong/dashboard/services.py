from decouple import config
import requests

def get_ip_usuario(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_localizacao_ip(ip):
    try:
        response = requests.get(f'{config("URL_IPWHOIS_API")}{ip}')
        data = response.json()

        if data.get("success"):
            return {
                "country": data.get("country"),
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude")
            }
        else:
            return None
    except Exception as e:
        print("Erro ao obter a localização:", e)
        return None