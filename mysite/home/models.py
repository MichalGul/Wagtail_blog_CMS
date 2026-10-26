from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

from wagtail.admin.panels import FieldPanel, MultiFieldPanel

class HomePage(Page):
    # add the Hero section

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )

    hero_text = models.CharField(max_length=255, blank=True, help_text='Homepage hero text')

    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text='Homepage hero call to action text'
    )

    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Hero CTA link",
        related_name='+', #you create a connection between models without creating a reverse relation. In other words, you’re instructing Django to create a way to access wagtailimages.Image from your Homepage but not a way to access HomePage from wagtailimages.Image.
        help_text='Homepage hero call to action link'
    )



    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
            MultiFieldPanel(
                [
                    FieldPanel("image"),
                    FieldPanel("hero_text"),
                    FieldPanel("hero_cta"),
                    FieldPanel("hero_cta_link"),
                ],
                heading="Hero section",
            ),
            FieldPanel("body"),
        ]