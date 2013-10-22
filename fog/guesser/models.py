# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Feed(models.Model):
    url = models.URLField(unique=True)
    source = models.ForeignKey('Source', related_name='feeds')

    def __str__(self):
        return "{source} ({url})".format(
            source=self.source.name,
            url=self.url,
        )


@python_2_unicode_compatible
class Source(models.Model):
    name = models.CharField(max_length=50)
    code = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Headline(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1000, unique=True)
    feed = models.ForeignKey('Feed', related_name='headlines')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Voter(models.Model):
    token = models.CharField(max_length=100)

    def __str__(self):
        return "<Voter {}>".format(self.token)


@python_2_unicode_compatible
class Vote(models.Model):
    class Meta:
        unique_together = ('voter', 'headline')

    voter = models.ForeignKey('Voter')
    headline = models.ForeignKey('Headline')
    source = models.ForeignKey('Source')

    def __str__(self):
        return "<Vote for {} guess {}>".format(self.headline.title, self.source.name)


@python_2_unicode_compatible
class VoteStats(models.Model):
    headline = models.OneToOneField('Headline', related_name='stats')
    succeeded = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)

    def __str__(self):
        return "<Vote for {} +{} -{}>".format(self.headline.title, self.succeeded, self.failed)

    @staticmethod
    def re_calculate_stats_on_new_vote(instance, **kwargs):
        """
        Once a vote has been done, re-calculate the stats of this vote

        :type instance: Vote
        """
        stat = VoteStats.objects.get_or_create(headline=instance.headline, defaults={
            'succeeded': 0,
            'failed': 0,
        })[0]

        stat.succeeded = Vote.objects.filter(
            headline=instance.headline,
            source=instance.headline.feed.source
        ).count()

        stat.failed = Vote\
            .objects\
            .filter(headline=instance.headline)\
            .exclude(source=instance.headline.feed.source)\
            .count()

        stat.save()

    @staticmethod
    def create_stats_on_new_headline(instance, **kwargs):
        VoteStats.objects.create(headline=instance)

models.signals.post_save.connect(VoteStats.re_calculate_stats_on_new_vote, sender=Vote)
models.signals.post_save.connect(VoteStats.create_stats_on_new_headline, sender=Headline)
