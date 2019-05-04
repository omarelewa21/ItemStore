import os
import sys
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from database import Accessory, AccessorySection, SectionItem, User
from database import db, app
import psycopg2
# Imports for security features
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = app


@app.route('/mobily/categories/json')
def categoriesJson():
    # Jsonify all the category sections in database
    category = AccessorySection.query.all()
    return jsonify(categories=[i.serialize for i in category])


@app.route('/mobily/<int:category_id>/items/json')
def itemJson(category_id):
    # Jsonify all the items in a category sections
    item = SectionItem.query.filter_by(store_id=category_id).all()
    return jsonify(items=[i.serialize for i in item])


@app.route('/mobily/<int:item_id>/itemdetail/json')
def itemdetailjson(item_id):
    # Jsonify the details specfic for one item
    item = SectionItem.query.filter_by(id=item_id).one()
    return jsonify(item_details=item.serialize)


@app.route('/')
@app.route('/mobily')
def mobilystore():
    # Main page for the Mobily Store
    mobile_items = AccessorySection.query.filter(
        AccessorySection.store_id == 1).all()
    PC_items = AccessorySection.query.filter(
        AccessorySection.store_id == 2).all()
    # Storing each cateogry items in a variable
    # In order to render an item from each category on the page
    all_cables = SectionItem.query.filter(
        SectionItem.store_id == 1).all()
    all_chargers = SectionItem.query.filter(
        SectionItem.store_id == 2).all()
    all_headsets = SectionItem.query.filter(
        SectionItem.store_id == 3).all()
    all_mouses = SectionItem.query.filter(
        SectionItem.store_id == 4). all()
    all_keyboards = SectionItem.query.filter(
        SectionItem.store_id == 5).all()
    all_drivers = SectionItem.query.filter(
        SectionItem.store_id == 6).all()

    return render_template(
        'mainpage_notLoggedin.html', mobile_items=mobile_items,
        PC_items=PC_items, all_cables=all_cables,
        all_chargers=all_chargers, all_headsets=all_headsets,
        all_mouses=all_mouses, all_keyboards=all_keyboards,
        all_drivers=all_drivers)


@app.route('/mobily/category/<int:category_id>')
def category_store(category_id):
    # Display a navigation bar as the same of the main page
    # Dispaly all items specific to one category
    mobile_items = AccessorySection.query.filter(
        AccessorySection.store_id == 1).all()
    PC_items = AccessorySection.query.filter(
        AccessorySection.store_id == 2).all()
    # Refer to Cateogry ID by store_id to obtain all items for that category
    category_items = SectionItem.query.filter_by(
        store_id=category_id)

    return render_template(
        'category.html', category_items=category_items,
        mobile_items=mobile_items, PC_items=PC_items,
        store__id=category_id)


@app.route('/mobily/item/<int:item_id>')
def itemdetail(item_id):
    # Display item information
    item = SectionItem.query.filter_by(id=item_id).one()
    return render_template('itemdetail.html', item=item)


if __name__ == "__main__":
    app.run()
