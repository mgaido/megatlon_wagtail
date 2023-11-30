from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


# Add these:
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    # add the get_context method:
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        print("A: ", request.user)
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        tenant_filtered_blogpages = [
            page for page in blogpages if page.specific.tenant == request.user.tenant
        ]
        context['blogpages'] = tenant_filtered_blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    #@login_required
    def serve(self, request):
        print("A: ", request.user)
        if request.user.is_authenticated:
            print("A: ", request.user)
            return super().serve(request)
        else:
            return render(request, 'users/login.html', {'page': self})
    

# add this:
from wagtail.search import index


# Keep the definition of BlogIndexPage model, and add the BlogPage model:

# New imports added for ParentalKey, Orderable, InlinePanel

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# ... Keep the definition of BlogIndexPage, update the content_panels of BlogPage, and add a new BlogPageGalleryImage model:

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)    
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    class Tenant(models.TextChoices):
        OPEN = "Accenture", "Accenture"
        TAKEN = "Vergeben", "Vergeben"
        WORK_IN_PROGRESS = "In Arbeit", "In Arbeit"
        COMPLETED = "Komplett", "Komplett"
        ABORTED = "Abgebrochen", "Abgebrochen"

    tenant = models.CharField(
        max_length=15,
        choices=Tenant.choices,
        default=Tenant.OPEN,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('tenant'),
        FieldPanel('tags'),

        # Add this:
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    #@login_required
    def serve(self, request):
        if not request.user.is_authenticated:
            return render(request, 'users/login.html', {'page': self})
        
        print(self.tenant)
        if request.user.tenant != self.tenant:
            return render(request, 'users/fail.html', {'page': self})

        return super().serve(request)
            


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]