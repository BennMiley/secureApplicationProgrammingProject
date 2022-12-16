from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Item
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        item = request.form.get('item')

        if len(item) < 1:
            flash('Please enter an item!', category='error')
        else:
            new_item = Item(data=item, user_id=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            flash('Item Added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    itemId = item['itemId']
    item = Item.query.get(itemId)
    if item:
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()

    return jsonify({})