import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.models.models import Role, Permission, RolePermission, User, UserRole
from app.core.auth.security import hash_password


ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin123'

RBAC = {
    'admin': [
        'users:read',
        'users:update',
        'users:delete',

        'orders:read',
        'orders:create',
        'orders:update',
        'orders:delete',

        'products:read',
        'products:create',
        'products:update',
        'products:delete',

        'reports:read',
        'reports:create',
    ],

    'user': [
        'users:read',
        'users:update',

        'orders:read',

        'products:read',

        'reports:read',
    ],
}


async def seed_entity(
    session: AsyncSession,
    model: type[Role | Permission],
    name: str,
    description: str,
):
    query = (
        select(model)
        .where(model.name == name)
    )

    query_result = await session.execute(query)
    db_result = query_result.scalar_one_or_none()

    if not db_result:
        new_db_result = model(
            name=name,
            description=description,
        )
        session.add(new_db_result)


async def seed_role_permission(
    session: AsyncSession,
    role_name: str,
    permission_name: str,
):
    role = (await session.execute(
        select(Role)
        .where(Role.name == role_name)
    )).scalar_one_or_none()

    permission = (await session.execute(
        select(Permission)
        .where(Permission.name == permission_name)
    )).scalar_one_or_none()

    if not role or not permission:
        raise ValueError("Role or Permission not found")

    role_permission = (await session.execute(
        select(RolePermission)
        .where(RolePermission.role_id == role.id,
               RolePermission.permission_id == permission.id)
    )).scalar_one_or_none()

    if not role_permission:
        new_role_permission = RolePermission(
            role_id=role.id,
            permission_id=permission.id,
        )
        session.add(new_role_permission)


async def seed_admin_user(
    session: AsyncSession,
):
    admin_exists = (
        await session.execute(
            select(User)
            .where(User.email == ADMIN_EMAIL)
        )
    ).scalar_one_or_none()

    if admin_exists:
        return

    admin = User(
        name='admin',
        surname='admin',
        middle_name='admin',
        email=ADMIN_EMAIL,
        hashed_password=hash_password(ADMIN_PASSWORD),
        is_active=True,
    )

    session.add(admin)
    await session.flush()

    admin_role = (
        await session.execute(
            select(Role)
            .where(Role.name == 'admin')
        )
    ).scalar_one_or_none()

    if not admin_role:
        raise ValueError('Admin role not found')

    user_role = UserRole(
        user_id=admin.id,
        role_id=admin_role.id,
    )

    session.add(user_role)


async def seed_all():
    async with async_session_maker() as session:
        async with session.begin():
            # Admin Role
            await seed_entity(
                session=session, model=Role, name='admin', description='Admin role',
            )
            # User Role
            await seed_entity(
                session=session, model=Role, name='user', description='User role',
            )

            # Permissions
            for value in RBAC['admin']:
                await seed_entity(
                    session=session,
                    model=Permission,
                    name=value,
                    description=value,
                )

            await session.flush()

            await seed_admin_user(session=session)

            for role_name, permissions in RBAC.items():
                for permission in permissions:
                    await seed_role_permission(
                        session=session,
                        role_name=role_name,
                        permission_name=permission,
                    )


if __name__ == "__main__":
    asyncio.run(seed_all())
