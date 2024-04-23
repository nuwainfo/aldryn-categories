# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext

from parler.admin import TranslatableAdmin

from treebeard.admin import TreeAdmin

from .forms import CategoryAdminForm
from .models import Category

try:
    from awesome_slugify import Slugify
except ModuleNotFoundError:
    from slugify import Slugify
unicodeSlugify = Slugify(translate=None)


class CategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = CategoryAdminForm

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
            )
        }),
        (' ', {
            'fields': (
                '_position',
                '_ref_node_id',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        FormClass = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        # Workaround for missing translations on treebeard
        FormClass.base_fields['_position'].label = ugettext('Position')
        FormClass.base_fields['_ref_node_id'].label = ugettext('Relative to')
        return FormClass

    def response_add(self, request, obj, post_url_continue=None):
        slug = request.POST.get('slug')
        if slug:
            obj.slug = unicodeSlugify(slug)
        else:
            obj.slug = unicodeSlugify(obj.name)
        obj.save()
        return super(CategoryAdmin, self).response_add(request, obj, post_url_continue=None)

    def response_change(self, request, obj):
        slug = request.POST.get('slug')
        if slug:
            obj.slug = unicodeSlugify(slug)
        else:
            obj.slug = unicodeSlugify(obj.name)
        obj.save()
        return super(CategoryAdmin, self).response_change(request, obj)


admin.site.register(Category, CategoryAdmin)
