"""
sentry_org_webhook.plugin
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2016 by Corey Donohoe, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

import operator
import six
import sentry
import sentry_org_webhook
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q

from sentry import http
from sentry.models import TagKey, TagValue
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri

class OrgWebhookPlugin(notify.NotificationPlugin):
    author = 'atmos'
    author_url = 'https://github.com/atmos'
    resource_links = (
        ('Bug Tracker', 'https://github.com/atmos/sentry-org-webhook/issues'),
        ('Source', 'https://github.com/atmos/sentry-org-webhook'),
    )

    title = 'Organization Webhook'
    slug = 'org_webhook'
    description = 'Post notifications to an HTTP endpoint.'
    timeout = getattr(settings, 'SENTRY_ORG_WEBHOOK_TIMEOUT', 3)
    conf_key = 'org_webhook'
    version = sentry_org_webhook.VERSION
    project_default_enabled = True


    def get_group_data(self, group, event):
        data = {
            'id': six.text_type(group.id),
            'project': group.project.slug,
            'project_name': group.project.name,
            'logger': event.get_tag('logger'),
            'level': event.get_tag('level'),
            'culprit': group.culprit,
            'message': event.get_legacy_message(),
            'url': group.get_absolute_url(),
        }
        data['event'] = dict(event.data or {})
        data['event']['tags'] = event.get_tags()
        return data

    def send_webhook(self, url, payload):
        return safe_urlopen(
            url=url,
            json=payload,
            timeout=self.timeout,
            verify_ssl=False,
        )

    def notify(self, notification):
        payload  = self.get_group_data(notification.event.group, notification.event)
        endpoint = getattr(settings, 'SENTRY_ORG_WEBHOOK_URI', 'http://example.com')
        safe_execute(self.send_webhook, endpoint, payload, _with_transaction=False)
