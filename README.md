# Auth System

## About Project

Auth System is a REST API service built with FastAPI that implements authentication, authorization, and Role-Based Access Control (RBAC).

The project provides user registration, login, JWT authentication, profile management, role management, permission management, and protected endpoints with role-based access control.

The application is fully containerized with Docker and supports automatic database migrations and data seeding during startup.

## Features

### Authentication

* User registration
* User login
* JWT access tokens
* Current user retrieval
* Logout with token blacklist

### User Management

* Get current profile
* Update profile
* Soft delete account

### Authorization (RBAC)

* Roles
* Permissions
* User roles
* Role permissions
* Permission-based endpoint protection

### Admin Management

* Assign role to user
* Remove role from user
* Get user roles
* Get user permissions

### Infrastructure

* PostgreSQL database
* Alembic migrations
* Docker & Docker Compose
* Automatic database migrations
* Automatic data seeding
* PostgreSQL health checks

## Tech Stack

* Python 3.14
* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic
* JWT (PyJWT)
* Passlib / Bcrypt
* Docker
* Docker Compose

## Quick Start

### Run with Docker

Clone the repository:

```bash
git clone https://github.com/IsmailBinnatov/auth_system_tz.git
cd auth_system_tz
```

Build and start the application:

```bash
docker compose up --build
```

The application automatically:

* Starts PostgreSQL
* Waits until the database is ready
* Applies Alembic migrations
* Seeds initial data
* Starts the FastAPI application

### API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI schema:

```text
http://localhost:8000/openapi.json
```

## Default Admin Account

The application automatically creates a default administrator account during database seeding.

```text
Email: admin@example.com
Password: admin123
```

## Environment Configuration

The repository contains a ready-to-use `.env.example` file with demonstration configuration values for local testing.

For production environments, sensitive data should be stored securely and must not be committed to version control.

## RBAC Access Control Design

The project uses a Role-Based Access Control (RBAC) model.

Instead of assigning permissions directly to users, permissions are assigned to roles, and roles are assigned to users.

### Access Control Structure

```text
User
  │
  ▼
UserRole
  │
  ▼
Role
  │
  ▼
RolePermission
  │
  ▼
Permission
```

### Database Tables

#### users

Stores user accounts and profile information.

#### roles

Stores available system roles.

Examples:

* admin
* user

#### permissions

Stores fine-grained access rules.

Permissions follow the format:

```
resource:action

```

Examples:

```
users:read
users:update
users:delete

orders:read
orders:create
orders:update
orders:delete

products:read
products:create
products:update
products:delete

reports:read
reports:create
```

Where:

* `resource` identifies the protected resource
* `action` identifies the operation allowed on that resource

For example:

`orders:create` allows a user to create new orders.

`orders:delete` allows a user to delete existing orders.

#### user_roles

Associates users with roles.

A user can have one or more roles.

#### role_permissions

Associates roles with permissions.

A role can contain multiple permissions.

### Permission Resolution

When a protected endpoint is accessed:

1. The JWT access token is validated.
2. The current user is identified.
3. All user roles are loaded.
4. All permissions associated with those roles are collected.
5. The requested permission is checked.
6. Access is granted or denied.

### HTTP Status Codes

#### 401 Unauthorized

Returned when:

* Access token is missing
* Access token is invalid
* User does not exist
* User is inactive
* Token is blacklisted

#### 403 Forbidden

Returned when:

* The user is authenticated
* The user does not have the required permission

### Permission Checker

Protected endpoints use a reusable permission dependency.

Example:

```python
PermissionChecker("orders:create")
```

The endpoint is accessible only if the current user has the required permission.

## Administrative API

The system provides administrative endpoints for managing user access.

Only users with the appropriate permissions can access these endpoints.

### Assign Role

Assign a role to a user.

```http
POST /admin/users/{user_id}/roles/{role_name}
```

### Remove Role

Remove a role from a user.

```http
DELETE /admin/users/{user_id}/roles/{role_name}
```

### Get User Roles

Retrieve all roles assigned to a user.

```http
GET /admin/users/{user_id}/roles
```

### Get User Permissions

Retrieve all permissions available to a user.

```http
GET /admin/users/{user_id}/permissions
```

## Mock Business Resources

To demonstrate the RBAC system, the project includes protected mock resources.

### Orders

```http
GET    /orders
POST   /orders
PATCH  /orders/{order_id}
DELETE /orders/{order_id}
```

### Products

```http
GET    /products
POST   /products
PATCH  /products/{product_id}
DELETE /products/{product_id}
```

### Reports

```http
GET    /reports
POST   /reports
```

These endpoints do not persist data and are intended only to demonstrate authentication and authorization behavior.
