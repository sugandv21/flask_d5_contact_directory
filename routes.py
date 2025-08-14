from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import Contact
from extensions import db
from forms import ContactForm

main = Blueprint("main", __name__)

@main.route("/")
def index():
    contacts = Contact.query.all()
    return render_template("index.html", contacts=contacts)

@main.route("/add", methods=["GET", "POST"])
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(contact)
        db.session.commit()
        flash("Contact added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("contact_form.html", form=form, title="Add Contact")

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        form.populate_obj(contact)
        db.session.commit()
        flash("Contact updated successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("contact_form.html", form=form, title="Edit Contact")

@main.route("/delete/<int:id>")
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted successfully!", "success")
    return redirect(url_for("main.index"))

@main.route("/api/contacts", methods=["GET"])
def api_get_contacts():
    contacts = Contact.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "phone": c.phone,
        "email": c.email,
        "address": c.address
    } for c in contacts])

@main.route("/api/contacts", methods=["POST"])
def api_add_contact():
    data = request.get_json()
    contact = Contact(
        name=data["name"],
        phone=data["phone"],
        email=data["email"],
        address=data.get("address", "")
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({
        "id": contact.id,
        "name": contact.name,
        "phone": contact.phone,
        "email": contact.email,
        "address": contact.address
    }), 201

@main.route("/api/contacts/<int:id>", methods=["PUT"])
def api_update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    if "name" in data:
        contact.name = data["name"]
    if "phone" in data:
        contact.phone = data["phone"]
    if "email" in data:
        contact.email = data["email"]
    if "address" in data:
        contact.address = data["address"]
    db.session.commit()
    return jsonify({
        "id": contact.id,
        "name": contact.name,
        "phone": contact.phone,
        "email": contact.email,
        "address": contact.address
    })

@main.route("/api/contacts/<int:id>", methods=["DELETE"])
def api_delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": f"Contact {id} deleted successfully."})
