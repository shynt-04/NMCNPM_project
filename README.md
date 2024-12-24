# Bài tập lớn IT3180 - Quản lý thu phí chung cư
TODO!!

## Thành viên nhóm 3
| Thành viên                                        | MSSV     | Vai trò     | Nhiệm vụ                              |
| ------------------------------------------------- | -------- | ----------- | ------------------------------------- |
| [Nguyễn Đăng Phúc]  | 20220040 | Trưởng nhóm | Backend, Frontend (Lập trình)         |
| [Vũ Trường An]       | 20220058 | Phó nhóm    | Frontend (Thiết kế giao diện)         |
| [Nguyễn Ngọc Kiệt]   | 20220052 | Thành viên | Frontend (Lập trình), Kiểm thử (Test) |
| [Lê Danh Vinh] | 20220051 | Thành viên | Frontend (Lập trình)                  |
## Cài đặt (Install & Config)
1. Tạo môi trường ảo trên Windows
- Nhấn  <Win + R> gõ “cmd” để mở Command Prompt
- Di chuyển đến thư mục muốn tạo môi trường ảo thông qua lệnh “cd” . Ví dụ: cd D:/test
- Tạo môi trường ảo bằng lệnh sau: python -m venv venv
- Sử dụng lệnh venv\Scripts\activate để kích hoạt môi trường ảo

1. Tải repository
```
git clone https://github.com/shynt-04/NMCNPM_project.git
cd NMCNPM_project
```
2. Cài đặt thư viện Django
```
pip install -r requirements.txt
```
## Chạy phần mềm trên local (Local Deployment)
Sau khi tải các thư viện cần thiết, có thể chạy ứng dụng với lệnh sau:
```
python manage.py runserver
```
Ứng dụng sẽ được chạy local ở [http://localhost:8000](http://localhost:8000) (8000 là port mặc định của Django)


## Tạo tài khoản admin,
Để tạo tài khoản admin, trên giao diện CMD di chuyển đến thư mục cài đặt của phần mềm (Ví dụ:D:/test/NMCNPM_project.git) chạy lệnh sau:

```bash
python manage.py createsuperuser
```
Sau đó nhập thông tin cần thiết để tạo tài khoản admin.
Sau khi tạo tài khoản admin, bạn có thể dùng tài khoản này để đăng nhập vào trang quản trị của ứng dụng tại [http://localhost:8000/admin](http://localhost:8000/admin)


