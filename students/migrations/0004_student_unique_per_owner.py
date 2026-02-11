from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_class_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.UniqueConstraint(
                fields=('owner', 'student_id'),
                name='unique_student_id_per_owner',
            ),
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.UniqueConstraint(
                fields=('owner', 'email'),
                name='unique_email_per_owner',
            ),
        ),
    ]


