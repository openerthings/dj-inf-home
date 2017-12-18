from django.contrib import admin
from .models import Album, Song
from .models import Item, ItemOut, ItemIn
# from .models import RFId, RFIdDet
# admin.site.register(Album)
# admin.site.register(Song)
admin.site.register(Item)
admin.site.register(ItemOut)
admin.site.register(ItemIn)

# admin.site.register(RFId)
# admin.site.register(RFIdDet)