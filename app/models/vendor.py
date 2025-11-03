"""Vendor model module."""
from .base import BaseModel, db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func

class VendorCategory(BaseModel):
    """Vendor category model."""
    
    __tablename__ = 'vendor_categories'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    vendors = db.relationship('Vendor', back_populates='category')

class VendorContact(BaseModel):
    """Vendor contact model for multiple contacts per vendor."""
    
    __tablename__ = 'vendor_contacts'

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    is_primary = db.Column(db.Boolean, default=False)

    vendor = db.relationship('Vendor', back_populates='contacts')

class Vendor(BaseModel):
    """Vendor model."""
    
    __tablename__ = 'vendors'

    name = db.Column(db.String(255), nullable=False)
    legal_name = db.Column(db.String(255))
    tax_id = db.Column(db.String(50))
    website = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')
    category_id = db.Column(db.Integer, db.ForeignKey('vendor_categories.id'))
    
    # Address fields
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))

    # Banking information
    bank_name = db.Column(db.String(255))
    bank_account_name = db.Column(db.String(255))
    bank_account_number = db.Column(db.String(50))
    bank_routing_number = db.Column(db.String(50))

    # Relationships
    category = db.relationship('VendorCategory', back_populates='vendors')
    contacts = db.relationship('VendorContact', back_populates='vendor',
                             cascade='all, delete-orphan')
    documents = db.relationship('VendorDocument', back_populates='vendor',
                              cascade='all, delete-orphan')
    
    @hybrid_property
    def primary_contact(self):
        """Get the primary contact for the vendor."""
        return next((contact for contact in self.contacts if contact.is_primary), None)

    @hybrid_property
    def full_address(self):
        """Get the full address as a formatted string."""
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.extend([self.city, self.state, self.postal_code])
        if self.country:
            parts.append(self.country)
        return ', '.join(filter(None, parts))

    @classmethod
    def search(cls, query):
        """Search vendors by name, legal name, or tax ID."""
        return cls.query.filter(
            db.or_(
                cls.name.ilike(f'%{query}%'),
                cls.legal_name.ilike(f'%{query}%'),
                cls.tax_id.ilike(f'%{query}%')
            )
        )

class VendorDocument(BaseModel):
    """Vendor document model for storing document metadata."""
    
    __tablename__ = 'vendor_documents'

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    mime_type = db.Column(db.String(100))
    size = db.Column(db.Integer)  # in bytes
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    expiry_date = db.Column(db.Date)

    vendor = db.relationship('Vendor', back_populates='documents')
    uploader = db.relationship('User')