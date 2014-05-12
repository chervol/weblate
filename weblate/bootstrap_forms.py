# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2014 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.forms.forms import BoundField, Form
from django.forms.widgets import CheckboxInput
from django.forms.util import ErrorList
from django.utils.html import format_html_join
from django.utils.encoding import force_text


DIV_TEMPLATE = '''<div %(html_class_attr)s>%(label)s
%(field)s%(help_text)s%(errors)s</div>'''

SPAN_TEMPLATE = '''<span%(html_class_attr)s>%(field)s</span>'''

HELP_TEMPLATE = '<p class="help-block">%s</p>'


class BootstrapErrorList(ErrorList):
    def as_ul(self):
        if not self: return ''
        return format_html_join(
            '',
            u'<p class="text-danger">{0}</p>',
            ((force_text(e), ) for e in self)
        )


class BootstrapBoundField(BoundField):
    def css_classes(self, extra_classes=None):
        classes = super(BootstrapBoundField, self).css_classes(extra_classes)
        if classes:
            result = set(classes.split())
        else:
            result = set()
        print self.field.widget
        if isinstance(self.field.widget, CheckboxInput):
            result.add('checkbox')
        else:
            result.add('form-group')
        return ' '.join(result)


class BootstrapForm(Form):
    '''
    Adds HTML output in divs and spans.
    '''
    def as_div(self):
        return self._html_output(
            normal_row=DIV_TEMPLATE,
            error_row=u'%s',
            row_ender='</div>',
            help_text_html = HELP_TEMPLATE,
            errors_on_separate_row=False
        )

    def as_span(self):
        return self._html_output(
            normal_row=SPAN_TEMPLATE,
            error_row=u'%s',
            row_ender='</span>',
            help_text_html=u'',
            errors_on_separate_row=True
        )

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError('Key %r not found in Form' % name)
        return BootstrapBoundField(self, field, name)

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = BootstrapErrorList
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget
            if not isinstance(widget, CheckboxInput):
                widget.attrs['class'] = 'form-control'