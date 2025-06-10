from django.core.management.base import BaseCommand
from community.models import StudyGroup

class Command(BaseCommand):
    help = 'Fix study groups with empty slugs'

    def handle(self, *args, **kwargs):
        # Get all groups with empty slugs
        groups = StudyGroup.objects.filter(slug='')
        count = 0
        
        for group in groups:
            original_slug = group.slug
            # Force slug generation by saving
            group.save()
            
            if group.slug and group.slug != original_slug:
                count += 1
                self.stdout.write(f'Fixed slug for group: {group.name} -> {group.slug}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully fixed {count} groups'))
