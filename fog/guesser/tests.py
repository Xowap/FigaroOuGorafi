"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from guesser.models import Headline, Voter, Source, Vote, VoteStats


class TestStatsCreation(TestCase):
    fixtures = ['initial_data.json', 'small_feed.json']

    def test_create_stats(self):
        headline = Headline.objects.get(id=1)
        source1 = Source.objects.get(id=1)
        source2 = Source.objects.get(id=2)

        voter1 = Voter(token='blah')
        voter1.save()

        voter2 = Voter(token='blih')
        voter2.save()

        vote = Vote(source=source1, headline=headline, voter=voter1)
        vote.save()
        stats = VoteStats.objects.get(headline=headline)
        self.assertEqual(0, stats.succeeded)
        self.assertEqual(1, stats.failed)

        vote = Vote(source=source2, headline=headline, voter=voter2)
        vote.save()
        stats = VoteStats.objects.get(headline=headline)
        self.assertEqual(1, stats.succeeded)
        self.assertEqual(1, stats.failed)

