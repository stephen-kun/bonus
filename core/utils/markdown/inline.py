# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import copy

from django.conf import settings
from django.contrib.auth import get_user_model

import mistune

from core.utils.markdown.utils.weibo import weibos
from .utils.emoji import emojis

User = get_user_model()
_linebreak = re.compile(r'^ *\n(?!\s*$)')
_text = re.compile(
    r'^[\s\S]+?(?=[\\<!\[_*`:@~]|https?://| *\n|$)'
)


class InlineGrammar(mistune.InlineGrammar):

    # todo: match unicode emojis
    emoji = re.compile(
        r'^:(?P<emoji>[A-Za-z0-9_\-\+]+?):'
    )

    weibo = re.compile(
        r'^\[(?P<weibo>[\u4E00-\u9FA5]+?)\]'
    )

    weibo3 = re.compile(
        r'^\[(?P<weibo>NO|good|ok)\]'
    )

    mention = re.compile(
        r'^@(?P<username>[\w.@+-]+)',
        flags=re.UNICODE
    )

    # Override
    def hard_wrap(self):
        # Adds ":" and "@" as an invalid text character, so we can match emojis and mentions.
        self.linebreak = _linebreak
        self.text = _text


class InlineLexer(mistune.InlineLexer):

    default_rules = copy.copy(mistune.InlineLexer.default_rules)
    default_rules.insert(2, 'emoji')
    default_rules.insert(2, 'mention')
    default_rules.insert(2, 'weibo')
    default_rules.insert(2,'weibo3')

    def __init__(self, renderer, rules=None, **kwargs):
        rules = InlineGrammar()
        rules.hard_wrap()

        super(InlineLexer, self).__init__(renderer, rules, **kwargs)

        self.mentions = {}
        self._mention_count = 0

    def output_weibo(self,m):
        weibo = m.group('weibo')
        if weibo not in weibos.keys():
            return m.group(0)

        title = weibo
        name_raw = weibos[title]

        return self.renderer.weibo(title,name_raw)


    def output_weibo3(self,m):
        weibo = m.group('weibo')
        if weibo not in weibos.keys():
            return m.group(0)

        title = weibo
        name_raw = weibos[title]

        return self.renderer.weibo(title,name_raw)


    def output_emoji(self, m):
        emoji = m.group('emoji')

        if emoji not in emojis:
            return m.group(0)

        name_raw = emoji
        name_class = emoji.replace('_', '-').replace('+', 'plus')
        return self.renderer.emoji(name_class=name_class, name_raw=name_raw)

    def output_mention(self, m):
        username = m.group('username')

        # Already mentioned?
        if username in self.mentions:
            user = self.mentions[username]
            return self.renderer.mention(username, user.jf.get_absolute_url())

        # Mentions limiter
        if self._mention_count >= settings.MENTIONS_PER_COMMENT:
            return m.group(0)

        # We increase this before doing the query to avoid abuses
        self._mention_count += 1

        # New mention
        try:
            user = User.objects\
                .select_related('jf')\
                .get(username=username)
        except User.DoesNotExist:
            return m.group(0)

        self.mentions[username] = user
        return self.renderer.mention(username, user.jf.get_absolute_url())
