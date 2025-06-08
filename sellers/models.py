from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse


# Create your models here.


class Seller(models.Model):
    name = models.CharField(max_length=50)
    # email = models.EmailField()
    # password = models.CharField(max_length=50)
    slug = models.SlugField(_("slug"),unique=True ,db_index=True)

    class Meta:
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")
    def __str__(self):
        return f"Seller's name:, {self.name}"

    def get_absolute_url(self):
        #return reverse("Seller_detail", kwargs={"pk": self.pk}) 
        return reverse("Seller_detail", kwargs={"slug": self.slug})