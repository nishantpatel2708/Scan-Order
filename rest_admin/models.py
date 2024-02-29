from django.db import models
from accounts.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.validators import RegexValidator

# Create your models here.


class Table(models.Model):
    table_no = models.CharField(max_length=120)
    rest = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    qr = models.ImageField(upload_to='qr_code', null=True, blank=False)

    def __str__(self):
        return f"{self.table_no} of {self.rest.restaurant_name}"

    def save(self, *args, **kwargs):
        logo = Image.open('rest_admin/python.png')
        img = Image.open('rest_admin/QR_ Flyer.jpg')

        basewidth = 75
        basewidth = basewidth
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        qr_big = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=11,
        )
        qr_big.add_data(
            f'http://127.0.0.1:8000/restaurant/menu/{self.rest.id}/{self.table_no}/'
        )
        qr_big.make()

        qrcode_img = qr_big.make_image(fill_color='black',
                                       back_color='white').convert('RGB')

        # pos = ((qrcode_img.size[0] - logo.size[0]) // 2, (qrcode_img.size[1] - logo.size[1]) // 2)
        # qrcode_img.paste(logo, pos)

        canvas = img.copy()

        canvas.paste(qrcode_img, (681, 1350))
        fname = f'qr_code-{self.table_no}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class Categories(models.Model):
    rest = models.ForeignKey(User, on_delete=models.CASCADE)
    Category_Name = models.CharField(max_length=50)
    Category_Image = models.ImageField(upload_to='category_images')
    Description = models.CharField(max_length=100)

    def __str__(self):
        return self.Category_Name


class MenuTable(models.Model):
    res = models.ForeignKey(User, on_delete=models.CASCADE)
    Dish_image = models.ImageField(upload_to='dish_images/',
                                   null=True,
                                   blank=True)
    Dish_Name = models.CharField(max_length=50)
    Dish_Description = models.CharField(max_length=80)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    Price = models.PositiveIntegerField()
    pices = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=20)
    speciality = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Dish_Name} of {self.res.restaurant_name}"


class Expenses(models.Model):
    res = models.ForeignKey(User, on_delete=models.CASCADE)
    Day_Expense = models.PositiveIntegerField()
    Date = models.DateTimeField()
    Others = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.res.restaurant_name


class PerMonthExpenses(models.Model):
    res = models.ForeignKey(User, on_delete=models.CASCADE)
    Rent = models.PositiveIntegerField(null=True, blank=True)
    Light_Bill = models.PositiveIntegerField(null=True, blank=True)
    Others = models.PositiveIntegerField(null=True, blank=True)
    Date = models.DateTimeField()

    def __str__(self):
        return self.res.restaurant_name


class Assests(models.Model):
    res = models.ForeignKey(User, on_delete=models.CASCADE)
    Furnishing = models.PositiveIntegerField(null=True, blank=True)
    Kitchen_equipements = models.PositiveIntegerField(null=True, blank=True)
    Others = models.PositiveIntegerField(null=True, blank=True)
    Date = models.DateTimeField()


class Unit(models.Model):
    rest = models.ForeignKey(User, on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=50)

    def __str__(self):
        return self.unit_name


class Inventory(models.Model):
    rest = models.ForeignKey(User, on_delete=models.CASCADE)
    Item_Name = models.CharField(max_length=50)
    Item_Price = models.PositiveBigIntegerField()
    Item_Amount = models.CharField(max_length=50)
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Item_Name