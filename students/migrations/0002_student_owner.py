from django.db import migrations, models
from django.conf import settings


def assign_owner_to_existing_students(apps, schema_editor):
    Student = apps.get_model('students', 'Student')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])

    first_user = User.objects.order_by('id').first()
    if not first_user:
        return

    Student.objects.filter(owner__isnull=True).update(owner=first_user)


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='owner',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='students',
                null=True,
                blank=True,
            ),
        ),
        migrations.RunPython(assign_owner_to_existing_students, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='student',
            name='owner',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='students',
            ),
        ),
    ]


