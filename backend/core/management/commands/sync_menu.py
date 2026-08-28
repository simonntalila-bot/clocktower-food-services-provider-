import json
import os
from django.core.management.base import BaseCommand
from core.models import Category, Food


class Command(BaseCommand):
    help = 'Sync the Django Food database to match the Vue app menu (173 items)'

    def handle(self, *args, **options):
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'data', 'foods.json')
        json_path = os.path.abspath(json_path)

        with open(json_path, encoding='utf-8') as fh:
            foods = json.load(fh)

        # Ensure category "kisnia" -> "visinia" so it matches the Vue app
        if Category.objects.filter(slug='kisnia').exists():
            kisnia = Category.objects.get(slug='kisnia')
            visinia, _ = Category.objects.get_or_create(
                slug='visinia',
                defaults={'name': 'Visinia', 'name_sw': 'Visinia', 'emoji': '🍽️', 'color': '#a78bfa'},
            )
            kisnia.foods.update(category=visinia)
            kisnia.delete()

        # Ensure all base categories exist
        cat_defaults = {
            'breakfast': {'name': 'Breakfast', 'name_sw': 'Kifungua Kinywa', 'emoji': '🍳', 'color': '#ffb84d'},
            'lunch': {'name': 'Lunch', 'name_sw': 'Chakula cha Mchana', 'emoji': '🍛', 'color': '#34d399'},
            'dinner': {'name': 'Dinner', 'name_sw': 'Chakula cha Jioni', 'emoji': '🍽️', 'color': '#a78bfa'},
            'drinks': {'name': 'Drinks', 'name_sw': 'Vinywaji', 'emoji': '🥤', 'color': '#38bdf8'},
            'visinia': {'name': 'Visinia', 'name_sw': 'Visinia', 'emoji': '🍽️', 'color': '#a78bfa'},
        }
        for slug, data in cat_defaults.items():
            Category.objects.get_or_create(slug=slug, defaults=data)

        cat_map = {c.slug: c for c in Category.objects.all()}

        # Remove old foods that are not part of the Vue menu
        vue_ids = {f['id'] for f in foods if f['category'] in cat_map}
        Food.objects.exclude(v_id__in=vue_ids).delete()

        created = updated = 0
        for fd in foods:
            slug = fd['category']
            if slug not in cat_map:
                continue
            rating = float(fd.get('rating') or 4.5)
            food, was_created = Food.objects.update_or_create(
                v_id=fd['id'],
                defaults={
                    'name': fd['name'],
                    'name_sw': fd.get('nameSw') or '',
                    'category': cat_map[slug],
                    'price': int(fd.get('price') or 0),
                    'icon': fd.get('icon') or '🍽️',
                    'image_url': fd.get('img') or '',
                    'rating': rating,
                    'popular': bool(fd.get('popular')),
                },
            )
            food.description = fd.get('desc') or ''
            food.description_sw = fd.get('descSw') or ''
            food.save()
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Menu sync complete: {created} created, {updated} updated, total={Food.objects.count()}'
        ))
