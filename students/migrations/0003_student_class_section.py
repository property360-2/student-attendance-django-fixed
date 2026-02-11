from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='class_section',
            field=models.CharField(
                max_length=50,
                blank=True,
                help_text='Class or section (e.g. BSIT 2A)',
            ),
        ),
    ]


