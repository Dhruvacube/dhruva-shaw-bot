from django.contrib import messages
import requests

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from discord_auth_data.models import *
from django.conf import settings
import discord
from discord import Webhook, RequestsWebhookAdapter


from .models import *
from django.conf import settings

# Create your views here.
@login_required
def home(request):
    return render(request,'home.html',{
        'server_name': 'Announcement Portal',
        'weebhook': Webhooks.objects.all(),
        'docs':settings.DOCS,
        'website':settings.WEBSITE
    })


def sendmessages(request):
    if request.method == 'POST':
        weebhook = request.POST.get('weebhook')
        announcement = request.POST.get('announcement')
        wbhk_obj = Webhooks.objects.filter(name=weebhook).all()[0]

        webhook = Webhook.partial(wbhk_obj.weebhook_id, wbhk_obj.webhook_token, adapter=RequestsWebhookAdapter())
        e = discord.Embed(title='A message from my developer',description=announcement)
        webhook.send(embed=e)
        messages.success(request,f'Announcement Sent to {weebhook} !')
    return redirect(reverse('Home'))


def keep_alive(request):
    api_key = settings.STATUSPAGE_API
    page_id = settings.PAGE_ID
    metric_id = settings.METRIC_ID
    api_base = 'api.statuspage.io'

    import time, random
    headers = {"Content-Type": "application/json", "Authorization": "OAuth " + api_key}
    ts = int(time.time()) - (random.randint(0,50) * 5 * 60)
    value = 5
    a=requests.post(
            'https://'+api_base+"/v1/pages/" + page_id + "/metrics/" + metric_id + "/data", 
            headers=headers, 
            json={'data':{'timestamp': ts, 'value': value}}
    ) 
    if (a.status_code >= 500):
        genericError = "Error encountered. Please ensure that your page code and authorization key are correct."
        print(genericError)
    if request.META.get('HTTP_AUTHORIZATION') == settings.AUTH_PASS:
        return render(
            request, 
            'keep_alive.html',
            {
                'server_name': 'Keeping Alive The Bot',
                'docs':settings.DOCS,
                'website':settings.WEBSITE,
                'statuspagecode': a.status_code
            }
        )
    else:
        return redirect(reverse('Home'))

def invite_bot(request):
    return redirect('https://discord.com/oauth2/authorize?client_id=779559821162315787&permissions=2147483656&scope=bot')


def return_available_anime(request, name):
    name_id = AnimeName.objects.filter(anime_name__in=name).all()
    anime = [i.anime_name for i in AnimeName.objects.iterator()]

    #return JsonResponse(anime, safe=False)
