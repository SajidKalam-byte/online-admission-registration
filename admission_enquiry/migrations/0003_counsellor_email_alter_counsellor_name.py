from django.db import migrations, models

def assign_unique_emails(apps, schema_editor):
    Counsellor = apps.get_model('admission_enquiry', 'Counsellor')
    for index, counsellor in enumerate(Counsellor.objects.all()):
        counsellor.email = f"counsellor{index+1}@example.com"
        counsellor.save()

class Migration(migrations.Migration):

    dependencies = [
        ('admission_enquiry', '0002_alter_counsellor_name'),
    ]

    operations = [
        # Step 1: Add email field with null=True temporarily
        migrations.AddField(
            model_name='counsellor',
            name='email',
            field=models.EmailField(max_length=254, unique=True, null=True),
        ),
        # Step 2: Assign unique email addresses to existing records
        migrations.RunPython(assign_unique_emails),
        # Step 3: Alter email field to make it non-nullable
        migrations.AlterField(
            model_name='counsellor',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
