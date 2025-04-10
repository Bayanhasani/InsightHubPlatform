# Generated by Django 5.1.7 on 2025-04-10 22:36

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('graduate', 'Graduate'), ('student', 'Student'), ('company', 'Company')], max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('verification_token', models.CharField(blank=True, max_length=100, null=True)),
                ('token_expiry', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pics/default_profile.jpg', null=True, upload_to='profile_pics/')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter your phone number', max_length=128, region=None)),
                ('location', models.CharField(blank=True, choices=[('Amman', 'Amman'), ('karak', 'AlKarak'), ('Zarqa', 'Zarqa'), ('Irbid', 'Irbid'), ('Aqaba', 'Aqaba'), ('Mafraq', 'Mafraq'), ('Madaba', 'Madaba'), ('Al-Balqa', 'Al-Balqa'), ('Jerash', 'Jerash'), ("Ma'an", "Ma'an"), ('Ajloun', 'Ajloun'), ('Tafilah', 'Tafilah')], max_length=100)),
                ('github', models.URLField(blank=True)),
                ('student_id', models.CharField(blank=True, max_length=20, null=True)),
                ('current_job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('current_company', models.CharField(blank=True, max_length=100, null=True)),
                ('work_experience', models.TextField(blank=True, null=True)),
                ('major', models.CharField(blank=True, choices=[('cis', 'CIS'), ('AI', 'AI'), ('software engineering', 'software engineering'), ('Cyber Security', 'Cyber Security')], max_length=100, null=True)),
                ('graduation_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1995), django.core.validators.MaxValueValidator(2030)])),
                ('skills', models.TextField(blank=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_description', models.TextField(blank=True, null=True)),
                ('company_size', models.CharField(blank=True, max_length=50, null=True)),
                ('industry', models.CharField(blank=True, max_length=100, null=True)),
                ('founded_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2025)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_type', models.CharField(choices=[('graduate', 'Graduate'), ('student', 'Student'), ('company', 'Company')], max_length=10)),
                ('university_id', models.CharField(blank=True, max_length=20, null=True)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('request_message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
