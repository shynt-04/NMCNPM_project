from django.apps import AppConfig
from django.db.models.signals import post_migrate


class NmcnpmappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nmcnpmapp'

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nmcnpmapp'

    def ready(self):
        from .models import apartment
        from django.db import connections

        def populate_apartments(sender, **kwargs):
            # Kiểm tra chỉ khởi tạo khi bảng chưa có dữ liệu
            if not apartment.objects.exists():
                apartments = []
                for floor in range(1, 21):  # Tầng từ 1 đến 20
                    for room in range(1, 15):  # Mỗi tầng có 14 phòng
                        room_id = int(f"{floor}{room:02d}")
                        area = 40 if room <= 9 else 60 if 9 < room <= 12 else 80
                        apartments.append(apartment(room_id=room_id, area=area))

                apartment.objects.bulk_create(apartments)
                print(f"Created {len(apartments)} apartments.")

        post_migrate.connect(populate_apartments, sender=self)