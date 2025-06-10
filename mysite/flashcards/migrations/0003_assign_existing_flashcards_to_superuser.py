from django.db import migrations

def assign_flashcards_to_superuser(apps, schema_editor):
    Flashcard = apps.get_model('flashcards', 'Flashcard')
    User = apps.get_model('auth', 'User')
    
    # Get the first superuser
    superuser = User.objects.filter(is_superuser=True).first()
    
    if superuser:
        # Update all flashcards without a user to belong to the superuser
        Flashcard.objects.filter(user__isnull=True).update(user=superuser)

def reverse_migrate(apps, schema_editor):
    Flashcard = apps.get_model('flashcards', 'Flashcard')
    # Set user to null for all flashcards owned by superusers
    Flashcard.objects.filter(user__is_superuser=True).update(user=None)

class Migration(migrations.Migration):
    dependencies = [
        ("flashcards", "0002_alter_flashcard_options_flashcard_user"),
    ]

    operations = [
        migrations.RunPython(assign_flashcards_to_superuser, reverse_migrate),
    ]
