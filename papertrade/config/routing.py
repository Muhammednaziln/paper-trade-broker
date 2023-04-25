# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
from papertrade.config.base_dir import BASE_DIR

ROOT_URLCONF = 'papertrade.urls'

STATIC_URL = 'assets/'
MEDIA_URL = 'src/'


MEDIA_ROOT = BASE_DIR / "public" / "src"            # keeping same end-name as MEDIA_URL for gateway server compatabilty
STATIC_ROOT = BASE_DIR / "public" / "assets"        # keeping same end-name as STATIC_URL for gateway server compatabilty
STATICFILES_DIRS = [BASE_DIR / "public" / "static"]



