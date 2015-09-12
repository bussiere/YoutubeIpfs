from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import subprocess

from django.contrib.auth.decorators import login_required

from threading import Thread
from Engine.models import Youtube,Ipfs,YoutubeIpfs

class GetUrlThread(Thread):
    def __init__(self, url):
        self.url = url 
        super(GetUrlThread, self).__init__()

    def run(self):
        url = self.url
        y =  Youtube.objects.all().filter(url=url)
        if len(y) ==  0 :
            y = Youtube(url=url)
            y.save()
        else :
            y = Youtube.objects.get(url=url)
        f = ""
        result = subprocess.check_output("""youtube-dl  -o "%(autonumber)s.mp4" """+""" "%s" """%url,shell=True)
        #print(result)
        #print(result)
        result = str(result)
        result = result.split("Destination:")[1]
        result = result.split(".mp4")[0]
        result = "%s.mp4"%result.strip()
        #print(result)
        result2 = subprocess.check_output("ipfs add %s"%result,shell=True)
        result2 = str(result2)
        hashipfs = result2.split(" ")[1]
        #print(result2.split(" ")[1])
        subprocess.check_output("rm %s"%result,shell=True)
        try :
            Ipfs.objects.get(hash_ipfs=hashipfs)
        except :
            ipfs =  Ipfs(hash_ipfs=hashipfs)
            ipfs.save()
        try :
            YoutubeIpfs.objects.get(youtube=y,ipfs=ipfs)
        except :
            yipfs = YoutubeIpfs(youtube=y,ipfs=ipfs)
            yipfs.save()
        


def index(request):
    context = {}
    list_marketdata = ""
    liste = {"liste" :YoutubeIpfs.objects.all().filter().order_by('-date_sys_added')[:25]}
    #print(liste)
    context.update(liste)
    if request.method == 'POST':
        retour = ""
        #print(request.POST)

        url = request.POST['url']
        url= url.strip()
        if "&" or "|" not in url :
            try :
                y =  Youtube.objects.get(url=url)
                yi = YoutubeIpfs.objects.get(youtube=y)
                retour = { 'retour' : """Url deja presente : %s <a href="http://gateway.ipfs.io/ipfs/%s"> http://gateway.ipfs.io/ipfs/%s</a> <a href="http://37.187.127.74:8080/ipfs/%s"> http://37.187.127.74:8080/ipfs/%s</a>"""%(yi.youtube,yi.ipfs,yi.ipfs,yi.ipfs,yi.ipfs) }
            except Exception as e :
                print(e)    
                t = GetUrlThread(url)
                t.start()
            

    else :
        retour = ""
    context.update(retour)
    return render(request, 'Index.html', context)    
