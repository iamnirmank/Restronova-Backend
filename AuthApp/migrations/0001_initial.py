# Generated by Django 4.2.6 on 2024-02-21 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Outlet",
            fields=[
                (
                    "outlet_code",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("addresss", models.CharField(blank=True, max_length=255, null=True)),
                ("contact_no", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "restaurant_code",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                ("contact_no", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "subscription_token",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("contact_no", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("role", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "verification_code",
                    models.CharField(blank=True, max_length=6, null=True),
                ),
                ("is_verified", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "password_reset_token",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                (
                    "password_reset_token_created_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_users",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "outlet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="outlet",
                        to="AuthApp.outlet",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_users",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="outlet",
            name="restaurant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurant",
                to="AuthApp.restaurant",
            ),
        ),
    ]
