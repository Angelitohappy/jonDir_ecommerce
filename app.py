from flask import Flask, flash, redirect, render_template, jsonify, request, session
from connection import verificar_usuario, registrar_usuario, email_existentes, consultar_productos, productos_x_categoria, consultar_usuario, consultar_producto, modificar_usuario, modificar_contrasena
from email_sending import send_email

from werkzeug.security import check_password_hash, generate_password_hash
import bot

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['PERMANENT_SESSION_LIFETIME'] = 31536000
app.config["SESSION_TYPE"] = "filesystem"
app.config['MYSQL_SSL_DISABLED'] = True
app.secret_key = 'Ah3G4rtLb1tM'

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    
    name = False
    
    if session.get("user_data"):
        name = session.get("user_data").get("name")
    
    return render_template("index.html", data={
        "logged": session.get("logueado"),
        "name": name
    })

@app.route("/sign-in", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['password']
        resultado = verificar_usuario(email, contraseña)
        
        if resultado:
            session['logueado'] = True
            print("id: ")
            print(resultado['id'])
            session['id'] = resultado['id']
            user_data = consultar_usuario(session['id']) 
            session['user_data'] = user_data            
            return redirect("/")  
        else:
            return render_template("sign-in.html", data={
                "logged": session.get("logueado"),
                "login_failed": True
            })  
    
    return render_template("sign-in.html", data={
        "logged": session.get("logueado"),
        "login_failed": False
    })

@app.route("/log-out")
def log_out():
    session['logueado'] = False
    session['id'] = None
    return redirect("/")

@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method != 'GET':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        birthdate = request.form['birthdate']
        genre = request.form['genre']
        resultado = email_existentes(email)
        if email == resultado:
            return render_template("sign-up.html", data={
                "logged": session.get("logueado"),
                "invalid_email": True,
            })
        else:
            registrar_usuario(email,password,name,birthdate,genre)
        return redirect("/sign-in")
            
    return render_template("sign-up.html", data={
        "logged": session.get("logueado"),
        "invalid_email": False,
    })



@app.route("/redirect-to", methods=["GET", "POST"])
def redirect_to(): 
    client_message = request.get_json(request.get_data)
    destination = bot.manage_conversation(client_message["destination"])
    redirect(destination)
    

@app.route("/contact", methods=["GET", "POST"])
def contact(): 
    if request.method == "GET":
        return render_template("contact.html", data={
        "logged": session.get("logueado"),
        "email": session.get("user_data")["email"],
        "email_error": False
    })
        
    sender = request.form.get("email")
    subject = request.form.get("subject")
    content = request.form.get("body")
    send_email(subject, content, sender)
    
    return render_template("contact.html", data={
        "logged": session.get("logueado"),
        "email": session.get("user_data")["email"],
        "sent": True
    })


@app.route("/about")
def about(): 
    return render_template("about.html", data={
        "logged": session.get("logueado")
    })


@app.route("/profile", methods=["GET", "POST"])
def profile(): 
    if request.method == "GET":
        print(session.get("user_data"))
        return render_template("profile.html", data={
        "logged": session.get("logueado"),
        "user_data": session.get("user_data"),
        "password_error": False
    })
        
    # post
    name = request.form.get("nombre")
    email = request.form.get("email")
    result = modificar_usuario(session["user_data"]["id"], name, email)
    new_user = consultar_usuario(session["user_data"]["id"])
    session["user_data"]["name"] = new_user["name"]
    session["user_data"]["email"] = new_user["email"]

    return render_template("profile.html", data={
        "logged": session.get("logueado"),
        "user_data": session.get("user_data"),
        "password_error": False,
        "modified": True
    })
        
@app.route("/reset-password", methods=["POST"])
def reset_password():
    new_password = request.form.get("new-password")
    modificar_contrasena(session["user_data"]["id"], new_password)
    new_user = consultar_usuario(session["user_data"]["id"])
    print("usuario")
    print(new_user)
    session["user_data"]["password"] = new_user["password"]
    
    return render_template("profile.html", data={
        "logged": session.get("logueado"),
        "user_data": session.get("user_data"),
        "password_error": False,
        "modified_pass": True
    })

@app.route("/products", methods=["GET", "POST"])
def products(): 
    if request.method == "GET":
        resultado = consultar_productos()
        print(resultado)
        return render_template("products.html", data={
        "logged": session.get("logueado"), "resultado": resultado 
    })
        
@app.route("/category", methods=["GET", "POST"])
def category():
    resultado = []  # Inicializa resultado como una lista vacía
    search_empty = False
    if request.method == "GET":
        category = request.args.get('category')  # Obtén la categoría de la solicitud GET
        name = request.args.get('search')
        if not(category or name):
            resultado = consultar_productos()
            return render_template("products.html", data={
            "logged": session.get("logueado"), "resultado": resultado, "search_error": True  
            })
        if category or name:
            resultado = productos_x_categoria(category, name)  # Llama a la función con la categoría
            print(resultado)  # Imprime el resultado en la consola
    
    if not resultado:
        search_empty = True
    
    return render_template("products.html", data={
        "logged": session.get("logueado"), "resultado": resultado, "search_empty": search_empty
    })


@app.route("/detailed-product")
def detailed_product(): 
    producto = consultar_producto(request.args.get("id"))
    
    return render_template("product.html", data={
        "logged": session.get("logueado"),
        "producto": producto
    })


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method != "POST":
        return render_template("chatbot.html", data={
        "logged": session.get("logueado")
    })
    
    client_message = request.get_json(request.get_data)
    respose = bot.manage_conversation(client_message["input"])
    data = {
        "bot_response": respose
    }
    return jsonify(data) 

@app.route("/carrito")
def carrito(): 
    return render_template("carrito.html", data={
        "logged": session.get("logueado")
    })

