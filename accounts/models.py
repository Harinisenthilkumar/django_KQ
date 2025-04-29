from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    USER_ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('sme', 'SME'),
        ('examiner', 'Examiner'),
        ('admin', 'Admin'),
    ]
    userRole = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, verbose_name='User Role')

    username = models.CharField(max_length=255, verbose_name='User Name', null=True, blank=True,unique=True)

    employeeId = models.CharField(max_length=100, verbose_name='Employee ID', default='')

    DEPARTMENT_CHOICES = [
        ('tech', 'Tech'),
        ('quality_check', 'Quality Check'),
        ('media', 'Media'),
        ('business_development', 'Business Development'),
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, verbose_name='Department')

    DESIGNATION_CHOICES = [
        ('developer', 'Developer'),
        ('qc_analysis', 'QC Analysis'),
        ('business_development_executive', 'Business Development Executive'),
    ]
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES, verbose_name='Designation')

    emailId = models.EmailField(verbose_name='Email ID', unique=True)

    mobileNumber = models.CharField(max_length=20, verbose_name='Mobile Number')

    isActive = models.BooleanField(default=True, verbose_name='Is Active')
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')

    isAccountLocked = models.BooleanField(default=False, verbose_name='Is Account Locked')

    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    


#Login Model

class LoginCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='login_credentials')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 

    class Meta:
        db_table = 'login_credentials'

    def __str__(self):
        return self.email
