from django.db import models

from django.utils import timezone

from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page

from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

# Create your models here.


class WarehousePage(Page):
    name = models.CharField(max_length=200, unique=True, null=False)
    location = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('location'),
    ]

    def __str__(self):
        return self.name


class ManufacturerPage(Page):
    name = models.CharField(max_length=200, unique=True, null=False)
    website = models.URLField(null=True)
    contact = models.CharField(max_length=200, null=True)
    phone_contact = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('contact'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('website'),
        FieldPanel('contact'),
        FieldPanel('phone_contact'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return self.name


class ProviderPage(Page):
    name = models.CharField(max_length=200, unique=True, null=False)
    website = models.URLField(null=True)
    address = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=200, null=True)
    phone_contact = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('contact'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('website'),
        FieldPanel('address'),
        FieldPanel('contact'),
        FieldPanel('phone_contact'),
    ]

    def __str__(self):
        return self.name


class ProductTypePage(Page):
    name = models.CharField(max_length=200, unique=True, null=False)
    features = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('features'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('features'),
    ]

    def __str__(self):
        return self.name


class ProductPage(Page):
    name = models.CharField(max_length=200, null=False)
    manufacturer = models.ForeignKey(
        'ManufacturerPage',
        on_delete=models.PROTECT,
    )
    provider = models.ForeignKey(
        'ProviderPage',
        on_delete=models.PROTECT,
    )
    product_type = models.ForeignKey(
        'ProductTypePage',
        on_delete=models.PROTECT,
    )
    picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    model = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(default=1, null=False)
    purchase_cost = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2
    )
    sale_cost = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2
    )
    friends_sale_cost = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    comments = models.TextField(max_length=400)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('manufacturer'),
        index.SearchField('product_type'),
        index.SearchField('model'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        ImageChooserPanel('picture'),
    ]

    def get_profit(self):
        return ((self.sale_cost / self.purchase_cost) - 1) * 100

    def get_friends_profit(self):
            return ((self.friends_sale_cost / self.purchase_cost) - 1) * 100

    def __str__(self):
        return self.name
