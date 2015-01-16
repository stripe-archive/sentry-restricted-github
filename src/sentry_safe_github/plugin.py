import logging
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from sentry.plugins import Plugin
from sentry.utils.http import absolute_uri
from sentry.utils.safe import safe_execute

import sentry_safe_github


logger = logging.getLogger('sentry.plugin.' + __name__)


class Form(forms.Form):
    # TODO: validate repo
    proj_url = forms.CharField(
        label=_('Project URL'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. github.com/stripe/sentry-safe-github'}),
        help_text=_('Enter your project url.'))


class SafeGithubPlugin(Plugin):
    title = _('Safe Github')
    slug = 'safe_github'
    description = "Tag sentry groups with the git blame for the code that threw the exception."
    version = sentry_safe_github.VERSION

    author = 'Stripe'
    author_url = 'https://github.com/stripe/sentry-safe-github'

    conf_title = title
    conf_key = 'safe_github'
    project_conf_form = Form

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('proj_url', project))

    def widget(self, request, group, **kwargs):
        event = group.get_latest_event()
        return self.render('sentry_safe_github/widget.html', {
            'is_configured': self.is_configured(group.project),
            'proj_url': self._get_github_url(group),
            'title': self._get_group_title(request, group, event),
            'desc': self._get_group_description(request, group, event),
        })

    def _get_group_body(self, request, group, event, **kwargs):
        interface = (event.interfaces.get('exception') or
                     event.interfaces.get('sentry.interfaces.Exception'))
        if interface:
            return safe_execute(interface.to_string, event)
        return

    def _get_group_description(self, request, group, event):
        output = [
            absolute_uri(group.get_absolute_url()),
        ]
        body = self._get_group_body(request, group, event)
        if body:
            output.extend([
                '',
                '```',
                body,
                '```',
            ])
        return '\n'.join(output)

    def _get_group_title(self, request, group, event):
        return event.error()

    def _get_github_url(self, group):
        url = self.get_option('proj_url', group.project)
        if url is None:
            return None
        match = re.match('github.com[/:]([-\w]+/[-\w]+)', url)
        if match:
            return 'https://github.com/%s' % match.groups()[0]
        else:
            return None
