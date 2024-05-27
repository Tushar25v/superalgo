from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
import urllib.parse
import uuid
import requests


def index(request):
    return render(request, 'index.html')


def login(request):
    base_url = "https://api.upstox.com/v2/login/authorization/dialog"
    client_id = settings.UPSTOX_CLIENT_ID
    redirect_uri = settings.UPSTOX_REDIRECT_URI
    state = str(uuid.uuid1())
    response_type = "code"
    
    # Construct the full URL with parameters
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "response_type": response_type
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    # Redirect the user to the Upstox login page
    return redirect(url)


def upstox_callback(request):
    # Extract the authorization code and state from the URL parameters
    authorization_code = request.GET.get('code')
    state = request.GET.get('state')
    
    if not authorization_code:
        return HttpResponse("Authorization failed or denied.", status=400)

    # Exchange the authorization code for an access token
    token_url = "https://api.upstox.com/v2/login/authorization/token"
    data = {
        "code": authorization_code,
        "client_id": settings.UPSTOX_CLIENT_ID,
        "client_secret": settings.UPSTOX_CLIENT_SECRET,
        "redirect_uri": settings.UPSTOX_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code != 200:
        return HttpResponse("Failed to obtain access token.", status=400)

    token_response = response.json()
    access_token = token_response.get('access_token')
    
    if not access_token:
        return HttpResponse("No access token received.", status=400)

    # At this point, you have the access token. You can save it to the database or session.
    # For demonstration purposes, we'll just render it.
    return render(request, 'access_token.html', {'access_token': access_token, 'state': state})
