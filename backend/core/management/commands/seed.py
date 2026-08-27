from django.core.management.base import BaseCommand
from core.models import Category, Food, User


class Command(BaseCommand):
    help = 'Seed initial data for ClockTower'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', password='clocktower2026',
                first_name='Admin', email='admin@clocktower.tz',
                role='admin', phone='0700000000'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created (admin / clocktower2026)'))

        # Create categories
        cats = {
            'breakfast': {'name': 'Breakfast', 'name_sw': 'Kifungua Kinywa', 'emoji': '🍳', 'color': '#ffb84d'},
            'lunch': {'name': 'Lunch', 'name_sw': 'Chakula cha Mchana', 'emoji': '🍛', 'color': '#34d399'},
            'dinner': {'name': 'Dinner', 'name_sw': 'Chakula cha Jioni', 'emoji': '🍽️', 'color': '#a78bfa'},
            'drinks': {'name': 'Drinks', 'name_sw': 'Vinywaji', 'emoji': '🥤', 'color': '#38bdf8'},
        }
        for slug, data in cats.items():
            Category.objects.get_or_create(slug=slug, defaults={**data})
        self.stdout.write(self.style.SUCCESS('Categories created'))

        # Create foods
        foods_data = [
            {'name': 'Chapati', 'name_sw': 'Chapati', 'cat': 'breakfast', 'price': 2000, 'icon': '🫓',
             'img': 'https://images.unsplash.com/photo-1600935926387-12d9b03066f0?auto=format&fit=crop&w=600&q=70',
             'rating': 4.8, 'popular': True, 'desc': 'Soft, layered flatbread grilled to a golden finish.',
             'desc_sw': 'Chapati laini linalopakwa hadi kuwa la rangi ya dhahabu.'},
            {'name': 'Mandazi', 'name_sw': 'Mandazi', 'cat': 'breakfast', 'price': 1000, 'icon': '🍩',
             'img': 'https://images.unsplash.com/photo-1509365465985-25d11c17e812?auto=format&fit=crop&w=600&q=70',
             'rating': 4.6, 'popular': True, 'desc': 'Light, fluffy fried dough.',
             'desc_sw': 'Mandazi laini yenye hewa.'},
            {'name': 'Tea', 'name_sw': 'Chai', 'cat': 'breakfast', 'price': 1500, 'icon': '🍵',
             'img': 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=70',
             'rating': 4.7, 'popular': False, 'desc': 'Hot, sweet and milky tea.',
             'desc_sw': 'Chai moto, tamu na ya maziwa.'},
            {'name': 'Coffee', 'name_sw': 'Kahawa', 'cat': 'breakfast', 'price': 2500, 'icon': '☕',
             'img': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=600&q=70',
             'rating': 4.5, 'popular': False, 'desc': 'Freshly brewed coffee.',
             'desc_sw': 'Kahawa iliyotengenezwa upya.'},
            {'name': 'Eggs', 'name_sw': 'Mayai', 'cat': 'breakfast', 'price': 3000, 'icon': '🍳',
             'img': 'https://images.unsplash.com/photo-1518476381266-33596bddffc0?auto=format&fit=crop&w=600&q=70',
             'rating': 4.6, 'popular': False, 'desc': 'Farm-fresh eggs cooked to your liking.',
             'desc_sw': 'Mayai safi yakapikwa kulingana na utakavyo.'},
            {'name': 'Chicken & Chips', 'name_sw': 'Kuku na Chips', 'cat': 'lunch', 'price': 12000, 'icon': '🍗',
             'img': 'https://images.unsplash.com/photo-1562967914-608f82629710?auto=format&fit=crop&w=600&q=70',
             'rating': 4.9, 'popular': True, 'desc': 'Crispy grilled chicken with golden chips.',
             'desc_sw': 'Kuku aliyechomwa na chips za dhahabu.'},
            {'name': 'Rice & Chicken', 'name_sw': 'Wali na Kuku', 'cat': 'lunch', 'price': 10000, 'icon': '🍛',
             'img': 'https://images.unsplash.com/photo-1603496987674-79600a000f55?auto=format&fit=crop&w=600&q=70',
             'rating': 4.8, 'popular': True, 'desc': 'Steamed rice with tender chicken.',
             'desc_sw': 'Wali wa mvuke na kuku laini.'},
            {'name': 'Pilau', 'name_sw': 'Pilau', 'cat': 'lunch', 'price': 8000, 'icon': '🍚',
             'img': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=600&q=70',
             'rating': 4.9, 'popular': True, 'desc': 'Fragrant spiced rice with tender meat.',
             'desc_sw': 'Pilau yenye harufu nzuri ya viungo.'},
            {'name': 'Chips Mayai', 'name_sw': 'Chips Mayai', 'cat': 'lunch', 'price': 7000, 'icon': '🍟',
             'img': 'https://images.unsplash.com/photo-1518013431117-eb1465fa5752?auto=format&fit=crop&w=600&q=70',
             'rating': 4.8, 'popular': True, 'desc': 'Golden chips in egg omelette.',
             'desc_sw': 'Chips za dhahabu kwenye omeleti ya mayai.'},
            {'name': 'Grilled Chicken', 'name_sw': 'Kuku Mchoma', 'cat': 'dinner', 'price': 15000, 'icon': '🍗',
             'img': 'https://images.unsplash.com/photo-1712579733874-c3a79f0f9d12?auto=format&fit=crop&w=600&q=70',
             'rating': 4.9, 'popular': True, 'desc': 'Whole grilled chicken, smoky and juicy.',
             'desc_sw': 'Kuku mzima aliyechomwa, wenye moshi na juisi.'},
            {'name': 'Beef Steak', 'name_sw': 'Steki ya Nyama', 'cat': 'dinner', 'price': 14000, 'icon': '🥩',
             'img': 'https://images.unsplash.com/photo-1546964124-0cce460f38ef?auto=format&fit=crop&w=600&q=70',
             'rating': 4.8, 'popular': True, 'desc': 'Juicy steak grilled to perfection.',
             'desc_sw': 'Steki ya juisi iliyochomwa kikamilifu.'},
            {'name': 'Fish & Chips', 'name_sw': 'Samaki na Chips', 'cat': 'dinner', 'price': 12000, 'icon': '🐟',
             'img': 'https://images.unsplash.com/photo-1697748836791-9ddf7e616ece?auto=format&fit=crop&w=600&q=70',
             'rating': 4.6, 'popular': False, 'desc': 'Crispy fish fillet with golden chips.',
             'desc_sw': 'Samaki aliyekaanga na chips za dhahabu.'},
            {'name': 'Soda', 'name_sw': 'Soda', 'cat': 'drinks', 'price': 2500, 'icon': '🥤',
             'img': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=600&q=70',
             'rating': 4.5, 'popular': True, 'desc': 'Ice-cold soda.',
             'desc_sw': 'Soda ya barafu.'},
            {'name': 'Fruit Juice', 'name_sw': 'Juisi ya Matunda', 'cat': 'drinks', 'price': 4000, 'icon': '🧃',
             'img': 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=600&q=70',
             'rating': 4.7, 'popular': True, 'desc': 'Freshly squeezed seasonal fruit juice.',
             'desc_sw': 'Juisi mpya ya matunda ya msimu.'},
            {'name': 'Passion Juice', 'name_sw': 'Juisi ya Passion', 'cat': 'drinks', 'price': 4000, 'icon': '🍹',
             'img': 'https://images.unsplash.com/photo-1600718374662-0483d2b9da44?auto=format&fit=crop&w=600&q=70',
             'rating': 4.8, 'popular': True, 'desc': 'Sweet passion fruit juice.',
             'desc_sw': 'Juisi ya passion tamu.'},
            {'name': 'Mango Smoothie', 'name_sw': 'Smoothie ya Embe', 'cat': 'drinks', 'price': 5000, 'icon': '🥭',
             'img': 'https://images.unsplash.com/photo-1577805947697-89e18249d767?auto=format&fit=crop&w=600&q=70',
             'rating': 4.9, 'popular': False, 'desc': 'Creamy, thick mango smoothie.',
             'desc_sw': 'Smoothie laini ya embe.'},
        ]

        breakfast = Category.objects.get(slug='breakfast')
        lunch = Category.objects.get(slug='lunch')
        dinner = Category.objects.get(slug='dinner')
        drinks = Category.objects.get(slug='drinks')
        cat_map = {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner, 'drinks': drinks}

        created = 0
        for fd in foods_data:
            cat = cat_map[fd['cat']]
            food, is_new = Food.objects.get_or_create(
                name=fd['name'],
                defaults={
                    'name_sw': fd['name_sw'], 'category': cat, 'price': fd['price'],
                    'icon': fd['icon'], 'image_url': fd['img'], 'rating': fd['rating'],
                    'popular': fd['popular'], 'description': fd['desc'], 'description_sw': fd['desc_sw'],
                }
            )
            if is_new:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'{created} foods created'))
        self.stdout.write(self.style.SUCCESS('Seed complete!'))
