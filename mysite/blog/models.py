from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField

from modelcluster.models import ParentalKey

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


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ['date', 'intro', 'body', 'gallery_images']


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+',
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = ['image', 'caption']