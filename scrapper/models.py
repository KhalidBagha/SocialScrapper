from django.db import models

# Create your models here.



class Facebook_Pages(models.Model):

    title = models.CharField(max_length=250)
    link = models.CharField(max_length=250, unique=True)
    about = models.TextField(null=True)
    audience = models.CharField(max_length=250,null=True)
    rating = models.CharField(max_length=250,null=True)
    category = models.CharField(max_length=250,null=True)
    keyword = models.CharField(max_length=250,null=True)
    location = models.CharField(max_length=250,null=True)
    email = models.EmailField(max_length=250,null=True)
    phone = models.CharField(max_length=250,null=True)
    website = models.URLField(max_length=250,null=True)
    
    def __str__(self):
        return self.title +" "+ self.link
    

class Linkedin_Pages(models.Model): ## companies
    title = models.CharField(max_length=250)
    website = models.URLField(max_length=250,null=True)
    about = models.TextField(null=True)
    link = models.CharField(max_length=250, unique=True)
    audience = models.CharField(max_length=250,null=True)
    keyword = models.CharField(max_length=250,null=True)
    category = models.CharField(max_length=250,null=True)
    location = models.CharField(max_length=250,null=True)
    email = models.EmailField(max_length=250,null=True)
    phone = models.CharField(max_length=250,null=True)
    csize = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.title


class Linkedin_Emp(models.Model):
    company = models.ForeignKey(Linkedin_Pages,on_delete=models.CASCADE)
    link = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    tag = models.CharField(max_length=250)
    timePeriod = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    jobType = models.CharField(max_length=250)
    location = models.CharField(max_length=250,null=True)
    keyword = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.name + " " + self.company.title 