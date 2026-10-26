from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from django import forms
from modelcluster.models import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.snippets.models import register_snippet # standard django model that is not a Page but can be reusable

# Create your models here.

class BlogIndexPage(Page):

    intro = RichTextField(blank=True)

    # modyfikacja podstawowego zwracanego query setu
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chronological
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blog_pages'] = blogpages
        return context

    content_panels = Page.content_panels + ["intro"] # pozwala na edycje w interface admina

# tagging system
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )



class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    authors = ParentalManyToManyField("blog.Author", blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                "date",
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                "tags",
            ],
            heading="Blog information",
        ),
        "intro",
        "body",
        "gallery_images",
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+',
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = ['image', 'caption']

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"

class BlogTagIndexPage(Page):
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context