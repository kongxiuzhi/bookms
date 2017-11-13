from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime


# Create your models here.

today_str 	= "({} {})".format(_(".etc"),datetime.datetime.now().strftime("%Y-%m-%d"))

class Category(models.Model):
	name = models.CharField(_('Category'),max_length=64)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Category')

class Location(models.Model):
	zone  = models.CharField(_('Zone'),max_length=128,help_text=_("The name of zone"))
	shelf = models.PositiveSmallIntegerField(_('Shelf'),help_text=_("The number of shelf"))
	row = models.PositiveSmallIntegerField(_('Row'))
	col	= models.PositiveSmallIntegerField(_('Col'))

	class Meta:
		verbose_name = _('Location')
		verbose_name_plural = verbose_name
		

class BookEditValidator():

	@staticmethod
	def isbn13(value):
		if not value.isdigit():
			raise ValidationError(_('%s not a digit') % value)
		elif len(value)!=13:
			raise ValidationError(_('%s --the number is not 13 digits') % value)
		pass
	@staticmethod
	def isbn10(value):
		if not value.isdigit():
			raise ValidationError(_('%s not a digit') % value)
		elif len(value)!=10:
			raise ValidationError(_('%s --the number is not 10 digits') % value)
		pass



class Book(models.Model):

	isbn10		= models.CharField(_('ISBN10'),default="",max_length=10,blank=True)
	isbn13		= models.CharField(_('ISBN13'),max_length=13,validators=[BookEditValidator.isbn13])
	face_l		= models.URLField(_('Face_L'),max_length=255,default="",blank=True)
	face_m		= models.URLField(_('Face_M'),max_length=255,default="",blank=True)
	face_s		= models.URLField(_('Face_S'),max_length=255,default="",blank=True)
	title		= models.CharField(_('Title'),max_length=128)
	subtitle 	= models.CharField(_('Subtitle'),max_length=128,default="",blank=True)
	pages		= models.PositiveSmallIntegerField(_('Pages'),default=0,blank=0,null=0)
	author		= models.CharField(_('Author'),max_length=256,default="",blank=True)
	translator	= models.CharField(_('Translator'),max_length=256,default="",blank=True)
	publisher	= models.CharField(_('Publisher'),max_length=256,default="",blank=True)
	price		= models.DecimalField(_('Price'),max_digits=5,decimal_places=2,default=0,blank=True,null=True)
	#boughtPrice	= models.DecimalField(_('Price Bought'),max_digits=5,decimal_places=2,default=0,blank=True,null=True)
	binding		= models.CharField(_('Binding'),max_length=128,default="",blank=True)
	pubdate		= models.DateField(_('Date Published'),blank=True,null=True,help_text=today_str)
	#boughtDate 	= models.DateField(_('Date Bought'),blank=True,null=True,help_text=today_str)
	authorDesc	= models.TextField(_('Author Desc'),blank=True,default="")
	summary		= models.TextField(_('Summary'),blank=True,default="")
	rating		= models.DecimalField(_('Rating'),max_digits=5,decimal_places=2,default=0,blank=True,null=True)
	#readPages	= models.PositiveSmallIntegerField(_('Read Pages'),default=0,blank=0,null=0,help_text="(%s)" %(_("Pages Be Read")))
	#readStart	= models.DateField(_('Reading Start'),blank=True,null=True,help_text=today_str)
	#readEnd		= models.DateField(_('Reading Finished'),blank=True,null=True,help_text=today_str)
	#readTags	= models.TextField(_('Reading Tags'),default="",blank=True)
	#readNote	= models.TextField(_('Reading Note'),default="",blank=True)
	category	= models.ForeignKey(Category,default="",blank=True,null=True,verbose_name=_('Category'))
	location	= models.ForeignKey(Location,default="",blank=True,null=True,verbose_name=_('Location')) 

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = _("Book")
		verbose_name_plural =verbose_name

class Reader(models.Model):
	name = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="read",verbose_name=_("Name of Reader"))
	book = models.ForeignKey(Book,related_name="reader",verbose_name=_("Book"))
	readPages	= models.PositiveSmallIntegerField(_('Read Pages'),default=0,blank=0,null=0,help_text="(%s)" %(_("Pages Be Read")))
	readStart	= models.DateField(_('Reading Start'),blank=True,null=True,help_text=today_str)
	readEnd		= models.DateField(_('Reading Finished'),blank=True,null=True,help_text=today_str)
	readTags	= models.TextField(_('Reading Tags'),default="",blank=True)
	readNote	= models.TextField(_('Reading Note'),default="",blank=True)
	boughtDate 	= models.DateField(_('Date Bought'),blank=True,null=True,help_text=today_str)
	boughtPrice	= models.DecimalField(_('Price Bought'),max_digits=5,decimal_places=2,default=0,blank=True,null=True)

	def __str__(self):
		return "{} is reading {}".format(name,book)

	class Meta:
		verbose_name = _("Reader")
		verbose_name_plural = verbose_name
