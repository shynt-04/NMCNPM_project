# Description: Script để tạo dữ liệu mẫu trong database

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from nmcnpmapp.models import apartment
# Tạo dữ liệu mẫu cho bảng apartment
def populate_apartments():
    apartments = []
    for floor in range(1, 21):  # Tầng từ 1 đến 10
        for room in range(1, 15):  # Mỗi tầng có 12 phòng
            room_id = int(f"{floor}{room:02d}")
            area = 40 if room <= 9 else 60 if 9 < room <= 12 else 80
            apartments.append(apartment(room_id=room_id, area=area))

    apartment.objects.bulk_create(apartments, ignore_conflicts=True)
    print(f"Created {len(apartments)} apartments!")

if __name__ == "__main__":
    populate_apartments()
