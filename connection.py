import mysql.connector as connector
from mysql.connector import Error
from flask import jsonify, redirect
from flask.globals import session 
from datetime import datetime

host = 'localhost'
user = 'root'
password = ''
port = 3306
db = 'jondir'

def obtener_conexion():
    try:
        conn = connector.connect(
            host=host,
            user=user,
            passwd=password,
            port=port,
            database=db,
        )
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
# code all the functions related with database communication 

#Selecters
def verificar_usuario(email, contraseña):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email,contraseña))
        resultado = cursor.fetchone()
        columnas = [i[0] for i in cursor.description]
        if resultado:
            dato = dict(zip(columnas, resultado))
            cursor.close()
            conn.close()
            return dato
        else:
            return False
    except Error as e:
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


def email_existentes(email):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0]
        else:
            return False
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
            cursor.close()
            conn.close()
            
            
def email_by_id(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE id = %s", (id,))
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0]
        else:
            return False
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
            cursor.close()
            conn.close()
            

def productos_x_categoria(category=None,name=None):
    pc = None
    # logica para consultar productos, en caso de que se proporcione categoria filtrarlo segun tal cateogira
    try:
        print(category)
        print(name)
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        if category and name:
            cursor.execute("SELECT * FROM products WHERE name like %s and category = %s ", ('%'+name+'%',category))
        elif category:
            cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
        elif name:
            cursor.execute("SELECT * FROM products WHERE name like %s ",('%'+name+'%',))
            
        pc = cursor.fetchall()
        print(pc)
        if pc:
            return pc
        else:
            return pc
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
            cursor.close()
            conn.close()

def consultar_productos():
    productos = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        productos = cursor.fetchall()
        if productos:
            return productos
        else:
            return productos
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
            cursor.close()
            conn.close()

def consultar_producto(id):
    producto = None
    # logica para obtener datos de producto
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products inner join post on products.id = %s and post.id = %s", (id,id))
        producto = cursor.fetchall()
        print("consultado")
        if producto:
            producto[0]["imagen"] = f"static/images/product_{producto[0]['id']}.png"
           
            return producto[0]
        else:
            print("malo")
            return False
    except Error as e:
        print("jaipapa", e)
        return jsonify({'error': str(e)}), 500
    finally:
            cursor.close()
            conn.close()
    
    
def consultar_usuario(id_usuario):

    try:

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (id_usuario,))
        datos_sql = cursor.fetchone()

        columnas = [i[0] for i in cursor.description] 
        datos_perfil = dict(zip(columnas, datos_sql))
        return datos_perfil
    
    except Exception as e:
        print(e)
    
    finally:
        
        cursor.close()
        conn.close()


def consultar_carrito(id_usuario):
    car = None
    # logica para conseguir productos del carrito de un usuario
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT p.name, p.price, p.quantity FROM products as p inner join cart_has_products as c on p.id = c.product_id WHERE c.cart_id = %s", (id_usuario))
        return car
    except Error as e:
        jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


#Insertions
def registrar_usuario(email,password,name,birthdate,genre):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        timestamp = datetime.now()
        cursor.execute("INSERT INTO users (email,password,name,birthdate,genre,created_at) VALUES (%s, %s, %s, %s, %s, %s)", (email,password,name,birthdate,genre,timestamp))
        conn.commit()
        ultimo_id = cursor.lastrowid
        print("Último ID insertado:", ultimo_id)
        cursor.execute("INSERT INTO carts (user_id) VALUES (%s) ",(ultimo_id))
        conn.commit()
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
            cursor.close()
            conn.close()
        

def insertar_producto_carrito(id_usuario, id_producto):
    # logica para insertar un producto en el carrito de un usuario
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cart_has_products (cart_id, product_id) VALUES (%s, %s)", (id_usuario, id_producto))
        conn.commit()
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def insertar_compra(id_usuario):
    # logica para realizar compra en funcion de los productos presentes en el carrito
    pass
        
    
#Modifies
def modificar_usuario(id_usuario, name = None, email = None):
    # logica para modificar los datos no nulos del usuario
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET  name = %s, email = %s WHERE id = %s ", (name, email, id_usuario)) 
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def modificar_contrasena(id_usuario, contraseña = None):
    #Modificar contrasena
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE users SET password = %s WHERE id = %s ", (contraseña, id_usuario)) 
        conn.commit()
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


#Deletes
def eliminar_producto_carrito(id_usuario, id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO cart_has_products (cart_id, product_id) VALUES (%s, %s)", (id_usuario, id_producto))
        conn.commit()

    except Error as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()