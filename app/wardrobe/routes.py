import os
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.wardrobe import bp
from app.wardrobe.forms import ItemUploadForm, OutfitForm, EmptyForm
from app.models import WardrobeItem, Outfit
from app import db
from app.wardrobe.ml_utils import classify_image, generate_outfit_recommendation

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_item():
    form = ItemUploadForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(filepath)
            
            # Use ML to classify the image
            predicted_category, confidence = classify_image(filepath)
            
            item = WardrobeItem(
                name=form.name.data,
                category=form.category.data,
                color=form.color.data,
                occasion=form.occasion.data,
                image_path=filename,
                predicted_category=predicted_category,
                confidence_score=confidence,
                user_id=current_user.id
            )
            db.session.add(item)
            db.session.commit()
            flash('Item successfully uploaded!', 'success')
            return redirect(url_for('wardrobe.view_items'))
    return render_template('wardrobe/upload.html', title='Upload Item', form=form)

@bp.route('/items')
@login_required
def view_items():
    page = request.args.get('page', 1, type=int)
    items = WardrobeItem.query.filter_by(user_id=current_user.id)\
        .paginate(page=page, per_page=12)
    form = EmptyForm()  # For CSRF protection
    return render_template('wardrobe/items.html', title='My Wardrobe', items=items, form=form)

@bp.route('/item/<int:id>')
@login_required
def item_detail(id):
    item = WardrobeItem.query.get_or_404(id)
    if item.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('wardrobe.view_items'))
    return render_template('wardrobe/item_detail.html', title='Item Detail', item=item)

@bp.route('/item/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = WardrobeItem.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted.', 'success')
    return redirect(url_for('wardrobe.view_items'))

@bp.route('/create-outfit', methods=['GET', 'POST'])
@login_required
def create_outfit():
    form = OutfitForm()
    if form.validate_on_submit():
        outfit = Outfit(
            name=form.name.data,
            occasion=form.occasion.data,
            user_id=current_user.id
        )
        db.session.add(outfit)
        db.session.commit()
        flash('Outfit created successfully!', 'success')
        return redirect(url_for('wardrobe.view_outfits'))
    return render_template('wardrobe/create_outfit.html', title='Create Outfit', form=form)

@bp.route('/outfits')
@login_required
def view_outfits():
    page = request.args.get('page', 1, type=int)
    outfits = Outfit.query.filter_by(user_id=current_user.id)\
        .paginate(page=page, per_page=12)
    return render_template('wardrobe/outfits.html', title='My Outfits', outfits=outfits)

@bp.route('/recommend_outfit')
@login_required
def recommend_outfit():
    occasion = request.args.get('occasion', 'casual')
    items = WardrobeItem.query.filter_by(user_id=current_user.id, is_available=True).all()
    
    if not items:
        return jsonify({'error': 'No items available in wardrobe'}), 400
        
    recommended_items = generate_outfit_recommendation(items, occasion)
    return jsonify({
        'outfit': [item.to_dict() for item in recommended_items]
    })
