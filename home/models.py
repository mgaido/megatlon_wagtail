from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager



class HomePage(Page):
    template = "home/home_page.html"

    body = RichTextField(features=["bold", "italic"])
    date = models.DateField("Post date", null=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('date'),
        FieldPanel('feed_image'),
    ]



class Pepe(Page):
    template = "home/home_page.html"

    body = RichTextField(features=["bold", "italic"])
    date = models.DateField("Post date", null=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('date'),
        FieldPanel('feed_image'),
    ]


