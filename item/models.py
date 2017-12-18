from django.contrib.auth.models import Permission, User
from django.db import models
from datetime import date


class RFId(models.Model):
    MANUFACTURE = 'MFR'
    OUT = 'OUT'
    IN = 'IN'
    WASTE = 'WST'

    rf_id_state_CHOICES = (
        (MANUFACTURE, '제품입고'),
        (OUT, '납품'),
        (IN, '수리입고'),
        (WASTE, '폐기'),
    )

    rf_id = models.CharField(primary_key=True, max_length=10)
    mfr_date = models.DateField(db_index=True, default=date.today)
    mfr_firm = models.CharField(max_length=50, blank=True)      #제조 회사
    expire_yn = models.BooleanField(default=False)
    expire_date = models.DateField(null=True, blank=True)
    out_firm = models.CharField(max_length=50, blank=True, null=True)      #납품회사
    out_date = models.DateField(null=True, blank=True)              #납품일자
    in_date = models.DateField(null=True, blank=True)  # 입고일자(for 수리)

    rf_id_state = models.CharField(max_length=3, choices=rf_id_state_CHOICES, default='MFR')
    #rfid상태코드 : MFR[제조입고], OUT[납품],IN[수리입고],FIX[수리완료], WASTE[폐기]

    def __str__(self):
        return self.rf_id + ' - ' + self.mfr_firm

class RFIdDet(models.Model):

    RFId = models.ForeignKey(RFId, on_delete=models.CASCADE)
    out_date = models.DateField(default=date.today)              #납품일자
    in_date = models.DateField(null=True, blank=True)           #수리입고일자
    message = models.CharField(max_length=300, blank=True, null=True)          #수리의견

    def __str__(self):
        return self.RFId + ' - ' + self.out_date


class Item(models.Model):

    PRODUCT = 'PRO'
    MATERIAL = 'MAT'
    CONSUMABLE = 'CON'
    ITEM_TYPE_CHOICES = (
        (PRODUCT, '제품'),
        (MATERIAL, '자재'),
        (CONSUMABLE, '소모품'),
    )

    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.CharField(max_length=20, blank=True, null=True, help_text="Item Name")
    item_type = models.CharField(max_length=3, choices=ITEM_TYPE_CHOICES, default='PRO')

    def __str__(self):
        return self.item_name


class ItemOut(models.Model):
    Item = models.ForeignKey(Item)
    out_date = models.DateField(default=date.today)
    out_firm = models.CharField(max_length=50, blank=True)
    out_qty = models.PositiveIntegerField(default=0)
    # message = models.TextField(null=True)
    message = models.CharField(max_length=300, blank=True, null=True)  # 수리의견


class ItemIn(models.Model):
    Item = models.ForeignKey(Item)
    in_date = models.DateField(default=date.today, help_text="입고일자")
    in_firm = models.CharField(max_length=50, blank=True)
    in_qty = models.PositiveIntegerField(default=0)
    # message = models.TextField(null=True)
    message = models.CharField(max_length=300, blank=True, null=True)  # 수리의견


class Stock(models.Model):
    Item = models.ForeignKey(Item)
    in_qty = models.PositiveIntegerField(default=0)
    out_qty = models.PositiveIntegerField(default=0)


class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title


