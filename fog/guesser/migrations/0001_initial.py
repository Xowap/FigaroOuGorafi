# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('guesser_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feeds', to=orm['guesser.Source'])),
        ))
        db.send_create_signal('guesser', ['Feed'])

        # Adding model 'Source'
        db.create_table('guesser_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('guesser', ['Source'])

        # Adding model 'Headline'
        db.create_table('guesser_headline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='headlines', to=orm['guesser.Feed'])),
        ))
        db.send_create_signal('guesser', ['Headline'])

        # Adding model 'Voter'
        db.create_table('guesser_voter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('guesser', ['Voter'])

        # Adding model 'Vote'
        db.create_table('guesser_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guesser.Voter'])),
            ('headline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guesser.Headline'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guesser.Source'])),
        ))
        db.send_create_signal('guesser', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['voter', 'headline']
        db.create_unique('guesser_vote', ['voter_id', 'headline_id'])

        # Adding model 'VoteStats'
        db.create_table('guesser_votestats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.related.OneToOneField')(related_name='stats', unique=True, to=orm['guesser.Headline'])),
            ('succeeded', self.gf('django.db.models.fields.IntegerField')()),
            ('failed', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('guesser', ['VoteStats'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['voter', 'headline']
        db.delete_unique('guesser_vote', ['voter_id', 'headline_id'])

        # Deleting model 'Feed'
        db.delete_table('guesser_feed')

        # Deleting model 'Source'
        db.delete_table('guesser_source')

        # Deleting model 'Headline'
        db.delete_table('guesser_headline')

        # Deleting model 'Voter'
        db.delete_table('guesser_voter')

        # Deleting model 'Vote'
        db.delete_table('guesser_vote')

        # Deleting model 'VoteStats'
        db.delete_table('guesser_votestats')


    models = {
        'guesser.feed': {
            'Meta': {'object_name': 'Feed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feeds'", 'to': "orm['guesser.Source']"}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'guesser.headline': {
            'Meta': {'object_name': 'Headline'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'headlines'", 'to': "orm['guesser.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        },
        'guesser.source': {
            'Meta': {'object_name': 'Source'},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'guesser.vote': {
            'Meta': {'unique_together': "(('voter', 'headline'),)", 'object_name': 'Vote'},
            'headline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guesser.Headline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guesser.Source']"}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['guesser.Voter']"})
        },
        'guesser.voter': {
            'Meta': {'object_name': 'Voter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'guesser.votestats': {
            'Meta': {'object_name': 'VoteStats'},
            'failed': ('django.db.models.fields.IntegerField', [], {}),
            'headline': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stats'", 'unique': 'True', 'to': "orm['guesser.Headline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'succeeded': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['guesser']