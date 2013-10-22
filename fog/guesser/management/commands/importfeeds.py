# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from django.core.management.base import BaseCommand
from guesser.models import Feed, Headline
import feedparser


class Command(BaseCommand):
    help = 'Import feeds to the DB'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            p = feedparser.parse(feed.url)

            for entry in p.entries:
                headline, created = Headline.objects.get_or_create(
                    url=entry.link,
                    feed=feed,
                    defaults={
                        'title': entry.title
                    }
                )

                if created:
                    self.stdout.write('Created "{}" <{}>'.format(entry.title, entry.link))

                if not created and headline.title != entry.title:
                    headline.title = entry.title
                    headline.save()
                    self.stdout.write('Updated "{}" <{}>'.format(entry.title, entry.link))
