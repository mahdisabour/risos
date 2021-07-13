from django.db import models

# Create your models here.
from treebeard.mp_tree import MP_Node
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save


class SmileCategory(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Smile Category: %s' % self.name

    def __str__(self):
        return self.name


class SmileColor(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Smile Color: %s' % self.name

    def __str__(self):
        return self.name


class SmileType(models.Model):
    name = models.CharField(max_length=20)
    related_smile_category = models.ForeignKey(
        SmileCategory, on_delete=models.CASCADE)
    related_smile_color = models.ForeignKey(
        SmileColor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)



class Teeth(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    teeth_image = models.ImageField(upload_to='Teeth/', blank=True, null=True)
    related_smile_color = models.ForeignKey(SmileColor, on_delete=models.CASCADE)
    related_smile_category = models.ForeignKey(SmileCategory, on_delete=models.CASCADE)


class Tooth(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    tooth_image = models.ImageField(upload_to='Teeth/', blank=True, null=True)
    related_teeth = models.ForeignKey(Teeth, on_delete=models.CASCADE, related_name="Tooths")

    

class SmileDesignService(models.Model):
    smile_image = models.ImageField(blank=True, null=True)
    full_smile_image = models.ImageField(blank=True, null=True)
    side_image = models.ImageField(blank=True, null=True)
    optional_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_type = models.ForeignKey(
        SmileType, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)


# there is bug in one to one field (related_smile_design)
class SmilePlot(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_design = models.ForeignKey(
        SmileDesignService, on_delete=models.CASCADE, related_name="smile_plot"
    )
    UNITS = {
        ("px", "Pixel"),
        ("cm", "Centi Meter")
    }
    unit = models.CharField(max_length=50, choices=UNITS, default="px")


class RectAngle(models.Model):
    x1 = models.FloatField(default=0)
    y1 = models.FloatField(default=0)
    x2 = models.FloatField(default=0)
    y2 = models.FloatField(default=0)


class OutRectangle(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_plot = models.ForeignKey(
        SmilePlot, on_delete=models.CASCADE, related_name="out_rectangle")
    rect_angle = models.OneToOneField(RectAngle, on_delete=models.CASCADE)


class TeethCoordinate(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    sequence = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    related_smile_plot = models.ForeignKey(
        SmilePlot, on_delete=models.CASCADE, related_name="teeth_coordinates")
    rect_angle = models.OneToOneField(RectAngle, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sequence', 'related_smile_plot', )


@receiver(post_save, sender=SmileDesignService)
def create_smile_plot(sender, instance, created, **kwargs):
    if created:
        SmilePlot(related_smile_design=instance).save()


@receiver(post_save, sender=SmilePlot)
def create_out_rectangle(sender, instance, created, **kwargs):
    if created:
        rect_angle = RectAngle()
        rect_angle.save()
        OutRectangle(related_smile_plot=instance, rect_angle=rect_angle).save()

        for i in range(6):
            rect_angle = RectAngle()
            rect_angle.save()
            TeethCoordinate(related_smile_plot=instance,
                            sequence=i, rect_angle=rect_angle).save()
        
