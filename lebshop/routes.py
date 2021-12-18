from lebshop.db_models import Fruit, User, ShoppingCart, FruitCartAss, CheckOutSessionData
from lebshop import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import json, render_template, url_for, redirect, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from lebshop.forms import SigninForm, SignupForm
from datetime import datetime
import stripe


db.create_all()


@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/get_item_count")
def get_items_count():
    cart = ShoppingCart.query.filter_by(
        owner_id=current_user.id).first()
    cart_length = len(cart.items)
    return jsonify(cart_length)


@app.route("/checkout/success")
@login_required
def successful_checkout():
    session_id = request.args.get("session_id")
    session_details = stripe.checkout.Session.retrieve(session_id)
    cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
    del_ass = FruitCartAss.query.filter_by(cart_id=cart.id).all()
    cosd = CheckOutSessionData(
        user_id=current_user.id,
        total_amount=f"{session_details['amount_total'] / 100 }",
        currency=session_details.get("currency"),
        session_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        items_count=len(cart.items),
        payment_method="card"
    )
    db.session.add(cosd)
    db.session.commit()
    for ass in del_ass:
        db.session.delete(ass)
    cart.items = []
    db.session.commit()
    return "<h1> hOOray </h1>"\
        "<br />"\
        "<br />"\
        f"<a href={url_for('leb_shop', category='all')}> BACK TO SHOP </a>"


@app.route("/checkout/canceled")
@login_required
def canceled_checkout():
    return "<h1> OOps </h1>"


@app.route("/shop/<category>")
def leb_shop(category):
    if category == "all":
        fruits_data = Fruit.query.all()
    else:
        fruits_data = Fruit.query.join(
            Fruit.categories, aliased=True).filter_by(name=category).all()
    return render_template("shop.html", fruits_data=fruits_data, keyword=f"category: {category}")


@ app.route("/shop/search/", methods=["GET"])
def leb_shop_search():
    search_value = request.args["q"]
    fruits_data = Fruit.query.filter(
        Fruit.name.like(f"%{search_value}%")).all()
    return render_template("shop.html", fruits_data=fruits_data, keyword=f"q: {search_value}")


@app.route("/shop/product/<product_id>")
def product_view(product_id):
    selected_fruit = Fruit.query.get(product_id)
    cart_length = 0
    if current_user.is_authenticated:
        cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
        cart_length = len(cart.items)
    return render_template("product_view.html", product=selected_fruit, cart_items_count=cart_length)


@app.route("/add-item-to-cart", methods=["POST"])
@login_required
def add_item():
    new_item = Fruit.query.get(request.form["itemId"])
    item_amount = float(request.form["quantity"])
    cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
    check_ass = FruitCartAss.query.filter_by(
        cart_id=cart.id, fruit_id=new_item.id).first()
    if check_ass:
        check_ass.fruit_amount += item_amount
        db.session.commit()
        return jsonify("increment")
    a = FruitCartAss(
        cart_id=cart.id,
        fruit_amount=item_amount
    )
    a.fruit_obj = new_item
    db.session.commit()
    if current_user.is_authenticated:
        return ""


@app.route("/cart-edit-amount", methods=["POST"])
@login_required
def edit_amount():
    cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
    edited_fruit = Fruit.query.filter_by(
        name=request.form["fruitName"]).first()
    for ass_obj in cart.items:
        if ass_obj.fruit_obj == edited_fruit:
            ass_obj.fruit_amount = request.form["fruitAmount"]
            db.session.commit()
            break
    return ""


@app.route("/cart-remove-item", methods=["POST"])
@login_required
def remove_cart_item():
    cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
    fruit_to_remove = Fruit.query.filter_by(
        name=request.form["fruitName"]).first()
    for ass_obj in cart.items:
        if ass_obj.fruit_obj == fruit_to_remove:
            db.session.delete(ass_obj)
            db.session.commit()
            break
    return ""


@app.route("/shop/cart")
@login_required
def cart():
    cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
    total = 0
    for item in cart.items:
        total += (item.fruit_amount * item.fruit_obj.price)
    return render_template("cart.html", cart=cart.items, total=total)


@app.route('/shop/create-checkout-session', methods=["POST"])
@login_required
def create_checkout_session():
    price_id_data = []
    with open(r"lebshop\json\id_price.json") as f:
        price_id_data = json.load(f)[0]
    line_items = []
    cart = ShoppingCart.query.filter_by(owner_id=current_user.id).first()
    for cart_item in cart.items:
        item = {
            "price": price_id_data[cart_item.fruit_obj.name],
            "quantity": int(cart_item.fruit_amount)
        }
        line_items.append(item)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode='payment',
        success_url=url_for("successful_checkout", _external=True) +
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for("canceled_checkout", _external=True)
    )
    return redirect(session.url, code=303)


@app.route("/user-profile")
def user_profile():
    user_sessions = CheckOutSessionData.query.filter_by(
        user_id=current_user.id).all()
    user_sessions = user_sessions[::-1]
    date_diffs = {}
    for session in user_sessions:
        d1 = datetime.strptime(session.session_date, "%m/%d/%Y, %H:%M:%S")
        d2 = datetime.strptime(datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S"), "%m/%d/%Y, %H:%M:%S")
        time_diff = abs((d2 - d1).days)
        if time_diff <= 1:
            time_uom = "day"
        else:
            time_uom = "days"
        if time_diff < 1:
            time_diff = int(abs((d2 - d1).seconds / (60 * 60)))
            if time_diff <= 1:
                time_uom = "hour"
            else:
                time_uom = "hours"
            if time_diff < 1:
                time_diff = int(abs((d2 - d1).seconds / 60))
                if time_diff <= 1:
                    time_uom = "minute"
                else:
                    time_uom = "minutes"
        date_diffs[session.id] = {"time_diff": time_diff, "time_uom": time_uom}
    return render_template("user_profile.html", user_sessions=user_sessions, date_diffs=date_diffs)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user_to_create = User(
            user_name=form.user_name.data,
            email=form.email.data.lower(),
            password=generate_password_hash(
                form.password.data, "pbkdf2:sha256", salt_length=8
            )
        )
        db.session.add(user_to_create)
        db.session.commit()
        if current_user:
            logout_user()
        login_user(user_to_create)
        flash("Account created successfuly! You are logged in.",
              category="success")
        flash(
            "Head's Up, We are working on proccessing decimal amounts;\
            currently, on checkout, decimal amounts are rounded down, '2.5 > 2, 3 > 3, 2 > 2'",
            category="danger"
        )
        flash("Use 4242 4242 4242 4242 as a test card-number.",
              category="info")
        cart = ShoppingCart(
            owner_id=current_user.id
        )
        db.session.add(cart)
        db.session.commit()
        return redirect(url_for("leb_shop", category="all"))
    if form.errors:
        for msg in form.errors.values():
            flash(f"ERROR: {msg}", category="danger")
    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            user_name=form.unique_identifier.data).first()
        if not user:
            user = User.query.filter_by(
                email=form.unique_identifier.data.lower()).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                if current_user:
                    logout_user()
                login_user(user)
                # next = request.form.get("next")
                flash(f"Login Successful, you are logged in as {user.user_name}",
                      category="success")
                flash(
                    "Head's Up, We are working on proccessing decimal amounts;\
                    currently, on checkout, decimal amounts are rounded down, ex: '2.5 > 2, 3 > 3, 2 > 2' ",
                    category="danger"
                )
                # return redirect(next or url_for("leb_shop", category="all"))
                return redirect(url_for("leb_shop", category="all"))
            else:
                flash(
                    "Password and username don't match", category="danger")
        else:
            flash(
                "User not found make sure you are using a valid username or email-adress", category="danger")
    if form.errors:
        for msg in form.errors.values():
            flash(f"ERROR: {msg}", category="danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
