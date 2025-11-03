"""Vendor management blueprint."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ...models import Vendor, VendorCategory, VendorContact, Permission
from ...utils.decorators import permission_required

bp = Blueprint('vendor', __name__, url_prefix='/vendors')

@bp.route('/')
@login_required
@permission_required(Permission.VIEW)
def index():
    """List all vendors."""
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    category_id = request.args.get('category', type=int)
    status = request.args.get('status')

    vendors_query = Vendor.query
    if query:
        vendors_query = Vendor.search(query)
    if category_id:
        vendors_query = vendors_query.filter_by(category_id=category_id)
    if status:
        vendors_query = vendors_query.filter_by(status=status)

    pagination = vendors_query.order_by(Vendor.name).paginate(
        page=page, per_page=12, error_out=False)
    
    categories = VendorCategory.query.order_by(VendorCategory.name).all()
    
    return render_template('vendor/index.html',
                         vendors=pagination.items,
                         pagination=pagination,
                         categories=categories)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.CREATE)
def add():
    """Add a new vendor."""
    if request.method == 'POST':
        vendor = Vendor(
            name=request.form['name'],
            legal_name=request.form.get('legal_name'),
            tax_id=request.form.get('tax_id'),
            website=request.form.get('website'),
            status=request.form.get('status', 'active'),
            category_id=request.form.get('category_id', type=int),
            address_line1=request.form.get('address_line1'),
            address_line2=request.form.get('address_line2'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            postal_code=request.form.get('postal_code'),
            country=request.form.get('country')
        )

        # Add primary contact
        if request.form.get('contact_name'):
            contact = VendorContact(
                name=request.form['contact_name'],
                title=request.form.get('contact_title'),
                email=request.form.get('contact_email'),
                phone=request.form.get('contact_phone'),
                is_primary=True
            )
            vendor.contacts.append(contact)

        try:
            vendor.save()
            flash('Vendor added successfully!', 'success')
            return redirect(url_for('vendor.index'))
        except Exception as e:
            flash(f'Error adding vendor: {str(e)}', 'danger')

    categories = VendorCategory.query.order_by(VendorCategory.name).all()
    return render_template('vendor/form.html', vendor=None, categories=categories)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def edit(id):
    """Edit a vendor."""
    vendor = Vendor.get_by_id(id)
    if vendor is None:
        flash('Vendor not found.', 'danger')
        return redirect(url_for('vendor.index'))

    if request.method == 'POST':
        vendor.name = request.form['name']
        vendor.legal_name = request.form.get('legal_name')
        vendor.tax_id = request.form.get('tax_id')
        vendor.website = request.form.get('website')
        vendor.status = request.form.get('status')
        vendor.category_id = request.form.get('category_id', type=int)
        vendor.address_line1 = request.form.get('address_line1')
        vendor.address_line2 = request.form.get('address_line2')
        vendor.city = request.form.get('city')
        vendor.state = request.form.get('state')
        vendor.postal_code = request.form.get('postal_code')
        vendor.country = request.form.get('country')

        # Update primary contact
        primary_contact = vendor.primary_contact
        if primary_contact:
            primary_contact.name = request.form.get('contact_name')
            primary_contact.title = request.form.get('contact_title')
            primary_contact.email = request.form.get('contact_email')
            primary_contact.phone = request.form.get('contact_phone')
        elif request.form.get('contact_name'):
            contact = VendorContact(
                name=request.form['contact_name'],
                title=request.form.get('contact_title'),
                email=request.form.get('contact_email'),
                phone=request.form.get('contact_phone'),
                is_primary=True
            )
            vendor.contacts.append(contact)

        try:
            vendor.save()
            flash('Vendor updated successfully!', 'success')
            return redirect(url_for('vendor.index'))
        except Exception as e:
            flash(f'Error updating vendor: {str(e)}', 'danger')

    categories = VendorCategory.query.order_by(VendorCategory.name).all()
    return render_template('vendor/form.html', vendor=vendor, categories=categories)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@permission_required(Permission.DELETE)
def delete(id):
    """Delete a vendor."""
    vendor = Vendor.get_by_id(id)
    if vendor is None:
        flash('Vendor not found.', 'danger')
    else:
        try:
            vendor.delete()
            flash('Vendor deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting vendor: {str(e)}', 'danger')
    return redirect(url_for('vendor.index'))