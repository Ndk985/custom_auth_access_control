"""
Management command для создания тестовых данных.

Создает:
- Роли: admin, manager, user, guest
- Бизнес-элементы: users, products, orders, shops, access_rules
- Правила доступа для каждой роли
- Тестовых пользователей с разными ролями
"""
from django.core.management.base import BaseCommand
from access.models import Role, BusinessElement, AccessRule
from users.models import User


class Command(BaseCommand):
    help = 'Создает тестовые данные: роли, элементы, правила доступа и пользователей'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        # Создание ролей
        self.stdout.write('\n1. Создание ролей...')
        roles = self._create_roles()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Создано {len(roles)} ролей')
        )

        # Создание бизнес-элементов
        self.stdout.write('\n2. Создание бизнес-элементов...')
        elements = self._create_business_elements()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Создано {len(elements)} элементов')
        )

        # Создание правил доступа
        self.stdout.write('\n3. Создание правил доступа...')
        rules_count = self._create_access_rules(roles, elements)
        self.stdout.write(
            self.style.SUCCESS(f'✓ Создано {rules_count} правил доступа')
        )

        # Создание тестовых пользователей
        self.stdout.write('\n4. Создание тестовых пользователей...')
        users_count = self._create_test_users(roles)
        self.stdout.write(
            self.style.SUCCESS(f'✓ Создано {users_count} пользователей')
        )
        self.stdout.write(
            self.style.SUCCESS('  ✓ Создан суперпользователь для админки')
        )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Все тестовые данные успешно созданы!')
        )

    def _create_roles(self):
        """Создает предустановленные роли."""
        roles_data = [
            {
                'name': 'admin',
                'description': 'Администратор системы с полным доступом ко всем ресурсам'
            },
            {
                'name': 'manager',
                'description': 'Менеджер с расширенными правами доступа'
            },
            {
                'name': 'user',
                'description': 'Обычный пользователь с базовыми правами'
            },
            {
                'name': 'guest',
                'description': 'Гость с минимальными правами доступа'
            },
        ]

        roles = []
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            roles.append(role)
            if created:
                self.stdout.write(f'  - Создана роль: {role.name}')
            else:
                self.stdout.write(f'  - Роль уже существует: {role.name}')

        return roles

    def _create_business_elements(self):
        """Создает предустановленные бизнес-элементы."""
        elements_data = [
            {
                'name': 'users',
                'description': 'Управление пользователями'
            },
            {
                'name': 'products',
                'description': 'Управление товарами'
            },
            {
                'name': 'orders',
                'description': 'Управление заказами'
            },
            {
                'name': 'shops',
                'description': 'Управление магазинами'
            },
            {
                'name': 'access_rules',
                'description': 'Управление правилами доступа'
            },
        ]

        elements = []
        for element_data in elements_data:
            element, created = BusinessElement.objects.get_or_create(
                name=element_data['name'],
                defaults={'description': element_data['description']}
            )
            elements.append(element)
            if created:
                self.stdout.write(f'  - Создан элемент: {element.name}')
            else:
                self.stdout.write(f'  - Элемент уже существует: {element.name}')

        return elements

    def _create_access_rules(self, roles, elements):
        """Создает правила доступа для ролей."""
        # Получаем роли и элементы по именам
        admin_role = next(r for r in roles if r.name == 'admin')
        manager_role = next(r for r in roles if r.name == 'manager')
        user_role = next(r for r in roles if r.name == 'user')
        guest_role = next(r for r in roles if r.name == 'guest')

        users_element = next(e for e in elements if e.name == 'users')
        products_element = next(e for e in elements if e.name == 'products')
        orders_element = next(e for e in elements if e.name == 'orders')
        shops_element = next(e for e in elements if e.name == 'shops')
        access_rules_element = next(
            e for e in elements if e.name == 'access_rules'
        )

        rules_data = [
            # Admin - полный доступ ко всему
            {
                'role': admin_role,
                'element': users_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': True,
                    'delete_permission': True,
                    'delete_all_permission': True,
                }
            },
            {
                'role': admin_role,
                'element': products_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': True,
                    'delete_permission': True,
                    'delete_all_permission': True,
                }
            },
            {
                'role': admin_role,
                'element': orders_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': True,
                    'delete_permission': True,
                    'delete_all_permission': True,
                }
            },
            {
                'role': admin_role,
                'element': shops_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': True,
                    'delete_permission': True,
                    'delete_all_permission': True,
                }
            },
            {
                'role': admin_role,
                'element': access_rules_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': True,
                    'delete_permission': True,
                    'delete_all_permission': True,
                }
            },
            # Manager - расширенные права
            {
                'role': manager_role,
                'element': products_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': False,
                    'update_all_permission': False,
                    'delete_permission': False,
                    'delete_all_permission': False,
                }
            },
            {
                'role': manager_role,
                'element': orders_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': False,
                    'update_all_permission': False,
                    'delete_permission': False,
                    'delete_all_permission': False,
                }
            },
            {
                'role': manager_role,
                'element': shops_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_permission': False,
                    'update_all_permission': False,
                    'delete_permission': False,
                    'delete_all_permission': False,
                }
            },
            # User - базовые права (только свои ресурсы)
            {
                'role': user_role,
                'element': products_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': False,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': False,
                    'delete_permission': True,
                    'delete_all_permission': False,
                }
            },
            {
                'role': user_role,
                'element': orders_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': False,
                    'create_permission': True,
                    'update_permission': True,
                    'update_all_permission': False,
                    'delete_permission': True,
                    'delete_all_permission': False,
                }
            },
            # Guest - минимальные права (только чтение своих)
            {
                'role': guest_role,
                'element': products_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': False,
                    'create_permission': False,
                    'update_permission': False,
                    'update_all_permission': False,
                    'delete_permission': False,
                    'delete_all_permission': False,
                }
            },
            {
                'role': guest_role,
                'element': orders_element,
                'permissions': {
                    'read_permission': True,
                    'read_all_permission': False,
                    'create_permission': False,
                    'update_permission': False,
                    'update_all_permission': False,
                    'delete_permission': False,
                    'delete_all_permission': False,
                }
            },
        ]

        created_count = 0
        for rule_data in rules_data:
            rule, created = AccessRule.objects.get_or_create(
                role=rule_data['role'],
                element=rule_data['element'],
                defaults=rule_data['permissions']
            )
            if created:
                created_count += 1
                self.stdout.write(
                    f'  - Создано правило: {rule.role.name} → {rule.element.name}'
                )
            else:
                # Обновляем существующее правило
                for key, value in rule_data['permissions'].items():
                    setattr(rule, key, value)
                rule.save()
                self.stdout.write(
                    f'  - Обновлено правило: {rule.role.name} → {rule.element.name}'
                )

        return created_count

    def _create_test_users(self, roles):
        """Создает тестовых пользователей."""
        admin_role = next(r for r in roles if r.name == 'admin')
        manager_role = next(r for r in roles if r.name == 'manager')
        user_role = next(r for r in roles if r.name == 'user')
        guest_role = next(r for r in roles if r.name == 'guest')

        users_data = [
            {
                'email': 'admin@example.com',
                'first_name': 'Админ',
                'last_name': 'Админов',
                'middle_name': 'Админович',
                'password': 'admin123',
                'role': admin_role,
            },
            {
                'email': 'manager@example.com',
                'first_name': 'Менеджер',
                'last_name': 'Менеджеров',
                'middle_name': 'Менеджерович',
                'password': 'manager123',
                'role': manager_role,
            },
            {
                'email': 'user@example.com',
                'first_name': 'Пользователь',
                'last_name': 'Пользователев',
                'middle_name': 'Пользователевич',
                'password': 'user123',
                'role': user_role,
            },
            {
                'email': 'guest@example.com',
                'first_name': 'Гость',
                'last_name': 'Гостев',
                'middle_name': 'Гостевич',
                'password': 'guest123',
                'role': guest_role,
            },
        ]

        created_count = 0
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'middle_name': user_data['middle_name'],
                    'role': user_data['role'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                created_count += 1
                self.stdout.write(
                    f'  - Создан пользователь: {user.email} (пароль: {user_data["password"]})'
                )
            else:
                # Обновляем пароль, если пользователь уже существует
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    f'  - Пользователь уже существует: {user.email} (пароль обновлен)'
                )

        # Создание суперпользователя для доступа в админку
        self.stdout.write('\n5. Создание суперпользователя...')
        superuser, created = User.objects.get_or_create(
            email='admin@admin.com',
            defaults={
                'first_name': 'Super',
                'last_name': 'Admin',
                'middle_name': '',
                'role': admin_role,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            superuser.set_password('admin')
            superuser.save()
            self.stdout.write(
                self.style.SUCCESS(
                    '  ✓ Создан суперпользователь: admin@admin.com (пароль: admin)'
                )
            )
        else:
            superuser.set_password('admin')
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()
            self.stdout.write(
                '  - Суперпользователь уже существует: admin@admin.com (обновлен)'
            )

        return created_count

