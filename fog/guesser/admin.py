# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from django.contrib import admin
from guesser.models import Feed, Source, Headline


admin.site.register(Feed)
admin.site.register(Source)
admin.site.register(Headline)