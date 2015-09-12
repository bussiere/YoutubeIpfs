from django.db import models
from datetime import datetime
# Create your models here.
class Youtube(models.Model):
    url = models.CharField(max_length=400,null=True, blank=True)
    date_sys_added = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self)  :
    	return self.url

class Ipfs(models.Model):
    hash_ipfs = models.CharField(max_length=800,null=True, blank=True)
    date_sys_added = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self)  :
    	return self.hash_ipfs

class YoutubeIpfs(models.Model):
    youtube = models.ForeignKey("Youtube",null=True, blank=True)
    ipfs = models.ForeignKey("Ipfs",null=True, blank=True)
    date_sys_added = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self)  :
    	return self.youtube.url

