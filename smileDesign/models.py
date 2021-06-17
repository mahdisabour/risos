from django.db import models

# Create your models here.
from treebeard.mp_tree import MP_Node
from django.core.validators import MinValueValidator, MaxValueValidator


class SmileCategory(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Smile Category: %s' % self.name

    def __str__(self):
        return self.name


class SmileColor(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Smile Color: %s' % self.name

    def __str__(self):
        return self.name


class SmileType(models.Model):
    name = models.CharField(max_length=20)
    related_smile_category = models.ForeignKey(SmileCategory, on_delete=models.CASCADE)
    related_smile_color = models.ForeignKey(SmileColor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SmileDesignService(models.Model):
    smile_image = models.ImageField(blank=True, null=True)
    full_smile_image = models.ImageField(blank=True, null=True)
    side_image = models.ImageField(blank=True, null=True)
    optional_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_type = models.ForeignKey(SmileType, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.id


# class SmilePlot(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
#     updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
#     related_smile_design = models.OneToOneField(SmileDesignService, on_delete=models.CASCADE, related_name="smile_plot")
#     UNITS = {
#         ("px","Pixel"),
#         ("cm", "Centi Meter")
#     }
#     unit = models.CharField(max_length=50, choices=UNITS,default="px")
    

# class RectAngle(models.Model):
#     x1 = models.FloatField()
#     y1 = models.FloatField()
#     x2 = models.FloatField()
#     y2 = models.FloatField()


# class OutRectangle(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
#     updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
#     related_smile_plot = models.OneToOneField(SmilePlot, on_delete=models.CASCADE, related_name="out_rectangle")
#     rect_angle = models.OneToOneField(RectAngle, on_delete=models.CASCADE)


# class TeethCoordinate(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
#     updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
#     teeth_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
#     related_smile_plot = models.ForeignKey(OutRectangle, on_delete=models.CASCADE, related_name="teeth_cordinates")
#     rect_angle = models.OneToOneField(RectAngle, on_delete=models.CASCADE)
#     class Meta:
#         unique_together = ('teeth_number', 'related_smile_plot', )


