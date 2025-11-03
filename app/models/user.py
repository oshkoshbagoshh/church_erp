"""User and role models for authentication and authorization."""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .base import BaseModel, db

# Association table for user roles
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Permission:
    """Permission flags for role-based access control."""
    VIEW = 1
    CREATE = 2
    EDIT = 4
    DELETE = 8
    ADMIN = 16

class Role(BaseModel):
    """Role model for RBAC."""
    
    __tablename__ = 'roles'

    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permissions = db.Column(db.Integer, default=Permission.VIEW)
    is_default = db.Column(db.Boolean, default=False, index=True)

    users = db.relationship('User', secondary=user_roles, back_populates='roles')

    @staticmethod
    def insert_default_roles():
        """Insert default roles into the database."""
        roles = {
            'User': [Permission.VIEW],
            'Staff': [Permission.VIEW, Permission.CREATE, Permission.EDIT],
            'Admin': [Permission.VIEW, Permission.CREATE, Permission.EDIT, 
                     Permission.DELETE, Permission.ADMIN]
        }

        default_role = 'User'

        for role_name, permissions in roles.items():
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
            role.permissions = sum(permissions)
            role.is_default = (role_name == default_role)
            db.session.add(role)
        db.session.commit()

class User(UserMixin, BaseModel):
    """User model with role-based access control."""
    
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)

    roles = db.relationship('Role', secondary=user_roles, back_populates='users')

    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password to a hashed password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        """Check if user has a specific permission."""
        return any(role.permissions & permission for role in self.roles)

    def has_role(self, role_name):
        """Check if user has a specific role."""
        return any(role.name == role_name for role in self.roles)

    @property
    def is_admin(self):
        """Check if user is an admin."""
        return self.has_role('Admin')

    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username