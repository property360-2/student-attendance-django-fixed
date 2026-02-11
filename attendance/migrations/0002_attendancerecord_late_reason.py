from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='late_reason',
            field=models.CharField(
                max_length=255,
                blank=True,
                help_text='Optional reason if the student is late.',
            ),
        ),
    ]


