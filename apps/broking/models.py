from django.db import models


class Symbol(models.Model):
    symbol = models.CharField(max_length=40, primary_key=True, unique=True, db_index=True)
    display_name = models.CharField(max_length=120, null=True, blank=True)
    industry_name = models.CharField(max_length=120, null=True, blank=True)
    parent_company = models.CharField(max_length=120, null=True, blank=True)
    nse_script_code = models.CharField(max_length=40, null=True, blank=True)
    is_nse_tradeable = models.BooleanField(default=True)
    bse_script_code = models.CharField(max_length=40, null=True, blank=True)
    is_bse_tradable = models.BooleanField(default=True)
    logo_url = models.ImageField(upload_to='symbol-logos',null=True, blank=True)

    def __str__(self):
        return self.symbol


