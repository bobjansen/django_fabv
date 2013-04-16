# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Experiment'
        db.create_table('django_fabv_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='result', null=True, to=orm['django_fabv.Test'])),
            ('goal', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_fabv.Goal'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('django_fabv', ['Experiment'])

        # Adding model 'Goal'
        db.create_table('django_fabv_goal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_fabv', ['Goal'])

        # Adding model 'Test'
        db.create_table('django_fabv_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_fabv.Experiment'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_fabv', ['Test'])

        # Adding model 'User'
        db.create_table('django_fabv_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('django_fabv', ['User'])

        # Adding model 'Hit'
        db.create_table('django_fabv_hit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_fabv.User'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('status_code', self.gf('django.db.models.fields.IntegerField')()),
            ('referer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('django_fabv', ['Hit'])

        # Adding model 'Choice'
        db.create_table('django_fabv_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_fabv.Experiment'])),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_fabv.Test'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_fabv.User'])),
        ))
        db.send_create_signal('django_fabv', ['Choice'])


    def backwards(self, orm):
        # Deleting model 'Experiment'
        db.delete_table('django_fabv_experiment')

        # Deleting model 'Goal'
        db.delete_table('django_fabv_goal')

        # Deleting model 'Test'
        db.delete_table('django_fabv_test')

        # Deleting model 'User'
        db.delete_table('django_fabv_user')

        # Deleting model 'Hit'
        db.delete_table('django_fabv_hit')

        # Deleting model 'Choice'
        db.delete_table('django_fabv_choice')


    models = {
        'django_fabv.choice': {
            'Meta': {'object_name': 'Choice'},
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_fabv.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_fabv.Test']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_fabv.User']"})
        },
        'django_fabv.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'goal': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_fabv.Goal']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'result'", 'null': 'True', 'to': "orm['django_fabv.Test']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'django_fabv.goal': {
            'Meta': {'object_name': 'Goal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'django_fabv.hit': {
            'Meta': {'object_name': 'Hit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_fabv.User']"}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'django_fabv.test': {
            'Meta': {'object_name': 'Test'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_fabv.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'django_fabv.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['django_fabv']