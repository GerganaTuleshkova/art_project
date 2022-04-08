from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from multiselectfield import MultiSelectField

UserModel = get_user_model()


class Style(models.Model):
    style_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.style_name

    class Meta:
        ordering = ['style_name']


class Technique(models.Model):
    technique_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.technique_name

    class Meta:
        ordering = ['technique_name']


class Gallery(models.Model):
    name = models.CharField(
        max_length=50,
    )

    address = models.CharField(
        max_length=150
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Galleries'


class Painting(models.Model):
    MIN_DIMENSIONS_VALUE_IN_CM = 2
    MAX_DIMENSIONS_VALUE_IN_CM = 400
    DEFAULT_PAINTING_NAME = 'Unnamed'
    PRICE_MIN_VALUE = 0.01

    # 11 main colors
    BLACK = 'black'
    BLUE = 'blue'
    BROWN = 'brown'
    GRAY = 'gray'
    GREEN = 'green'
    ORANGE = 'orange'
    PINK = 'pink'
    PURPLE = 'purple'
    RED = 'red'
    WHITE = 'white'
    YELLOW = 'yellow'
    ALL = 'all'
    COLOR_CHOICES = (
        (1, BLACK),
        (2, BLUE),
        (3, BROWN),
        (4, GRAY),
        (5, GREEN),
        (6, ORANGE),
        (7, PINK),
        (8, PURPLE),
        (9, RED),
        (10, WHITE),
        (11, YELLOW),
        (12, ALL),
    )

    # 5 base materials
    CANVAS = 'Canvas'
    PAPER = 'Paper'
    WOOD = 'Wood'
    GLASS = 'Glass'
    METAL = 'Metal'
    BASE_MATERIAL_CHOICES = [(x, x) for x in (CANVAS, PAPER, WOOD, GLASS, METAL)]

    title = models.CharField(
        max_length=50,
        default=DEFAULT_PAINTING_NAME,
        blank=True,
        null=True,
    )

    artist = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    width = models.IntegerField(
        validators=[
            MinValueValidator(MIN_DIMENSIONS_VALUE_IN_CM),
            MaxValueValidator(MAX_DIMENSIONS_VALUE_IN_CM),
        ]
    )

    height = models.IntegerField(
        validators=[
            MinValueValidator(MIN_DIMENSIONS_VALUE_IN_CM),
            MaxValueValidator(MAX_DIMENSIONS_VALUE_IN_CM),
        ]
    )

    base_material = models.CharField(
        max_length=max([len(p) for n, p in BASE_MATERIAL_CHOICES]),
        choices=BASE_MATERIAL_CHOICES,
        default=CANVAS,
    )

    style = models.ForeignKey(Style, on_delete=models.RESTRICT)
    techniques = models.ForeignKey(Technique, on_delete=models.RESTRICT)
    photo = models.ImageField(
        upload_to='paintings_photos',
    )

    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
    )
    price = models.FloatField(
        validators=[
            MinValueValidator(PRICE_MIN_VALUE),
        ]
    )

    main_colors = MultiSelectField(choices=COLOR_CHOICES, default=ALL)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'"{self.title}" by {self.artist}'
