# cazador de contraseñas

''' Para la aleatoriedad en seguridad, usamos el módulo secrets de Python (diseñado para criptografía)
    en lugar de random (que es predecible).''' 
     
import secrets
import string

# Clase responsable de la aleatoriedad segura.
class MotorCriptografico:
    def elegir_caracter(self, opciones: str) -> str: # Método que recibe un string opciones y devuelve un string (un solo carácter). 
        return secrets.choice(opciones) # Elige un carácter al azar del string opciones usando criptografía 
    
    def mezclar_lista(self, lista: list) -> list: # Mezcla una lista de caracteres de forma segura e impredecible
        lista_mezclada = lista.copy() # Crea una copia superficial de la lista original para no modificarla directamente 
        for i in range(len(lista_mezclada) - 1, 0, -1): # Itera desde el último índice hasta el índice 1 (no llega a 0), yendo hacia atrás. Algoritmo Fisher-Yates.
            j = secrets.randbelow(i + 1) # Genera un número aleatorio seguro entre 0 y i (inclusive). Este será el índice con el que se hará el intercambio.
            lista_mezclada[i], lista_mezclada[j] = lista_mezclada[j], lista_mezclada[i] # Intercambia los elementos en las posiciones i y j usando asignación múltiple de Python 
        return lista_mezclada # devuelve la lista mezclada.

# Define la clase principal del generador de contraseñas, usa la clase MotorCriptografico como dependencia externa.
class GeneradorContrasenaAvanzado:
    ESPECIALES = "¿¡?=)(/*+-%&$#!." # Lista de caracteres especiales obligatorios solicitados

    def __init__(self, longitud: int, motor_aleatorio): # Guarda el motor criptográfico como atributo.  
        self.motor = motor_aleatorio # En lugar de crearlo internamente lo recibe desde afuera, lo que facilita pruebas y reutilización.
        self.longitud = longitud # Asignar aquí no es una asignación simple: dispara automáticamente el @longitud.setter definido más abajo, ejecutando todas las validaciones.

    @property # El decorador @property convierte el método en un getter
    def longitud(self) -> int: #  Cuando alguien lee obj.longitud, ejecuta este método y devuelve self._longitud
        return self._longitud # el valor real almacenado con guión bajo, por convención "privado"

    @longitud.setter # El setter se activa cada vez que se hace self.longitud = algo
    def longitud(self, valor: int): # metodo que recibe el valor a asignar en valor.
        if not isinstance(valor, int):
            raise TypeError("La longitud debe ser un número entero.") # Verifica que el valor sea exactamente un int. Si pasas 8.0 (float) o "8" (string), lanza error.
        if valor < 8: 
            raise ValueError("Por seguridad, la longitud mínima debe ser de 8 caracteres.") # Regla de seguridad: contraseñas de menos de 8 caracteres son rechazadas.
        
        # Validación estricta física: el pool total de caracteres únicos disponibles
        # (26 min + 26 may + 10 num + 15 esp = 77). No podemos pedir más de 77 caracteres sin repetir.
        pool_maximo = 26 + 26 + 10 + len(self.ESPECIALES)
        if valor > pool_maximo:
            raise ValueError(f"Para evitar caracteres repetidos, la longitud máxima admisible es de {pool_maximo} caracteres.")
            
        self._longitud = valor # Solo si pasó todas las validaciones, guarda el valor en el atributo "privado" _longitud.

# """VALIDACIÓN ESTRICTA: Verifica que la contraseña cumpla TODAS las reglas."""
    def _es_valida(self, contrasena: str) -> bool: # El guión bajo al inicio es una convención que indica que es un método interno, no pensado para usarse fuera de la clase.
        # 1. No debe tener caracteres repetidos
        if len(set(contrasena)) != len(contrasena): # set() elimina duplicados. Si el conjunto tiene menos elementos que el string original, hay caracteres repetidos → inválida.
            return False
            
        # 2. Verificar presencia de cada grupo obligatorio
        # any() con una expresión generadora recorre la contraseña y devuelve True en cuanto encuentra un solo carácter que cumpla la condición.
        tiene_minuscula = any(c in string.ascii_lowercase for c in contrasena)
        tiene_mayuscula = any(c in string.ascii_uppercase for c in contrasena)
        tiene_numero = any(c in string.digits for c in contrasena)
        tiene_especial = any(c in self.ESPECIALES for c in contrasena)
        
        # Solo retorna True si los cuatro grupos están presentes simultáneamente.
        return tiene_minuscula and tiene_mayuscula and tiene_numero and tiene_especial

    # Genera y valida estrictamente la contraseña antes de retornarla.
    def generar(self) -> str:
        # Construye el alfabeto completo de 77 caracteres concatenando todos los grupos. Es el menú de donde se elegirán los caracteres extra.
        pool_total = string.ascii_lowercase + string.ascii_uppercase + string.digits + self.ESPECIALES
        
        # Bucle de control: se repite hasta que la contraseña sea 100% válida
        while True: # Bucle infinito intencional. Se repetirá hasta que se genere una contraseña válida y se ejecute el return.
            password_chars = []
            
            # PASO 1: Asegurar los 4 requisitos mínimos obligatorios primero
            password_chars.append(self.motor.elegir_caracter(string.ascii_lowercase))
            password_chars.append(self.motor.elegir_caracter(string.ascii_uppercase))
            password_chars.append(self.motor.elegir_caracter(string.digits))
            password_chars.append(self.motor.elegir_caracter(self.ESPECIALES))
            
            # PASO 2: Rellenar el resto de la longitud deseada con el pool total
            longitud_restante = self.longitud - len(password_chars)
            for _ in range(longitud_restante):
                password_chars.append(self.motor.elegir_caracter(pool_total)) 
                            
            # PASO 3: Romper el orden predecible (Principio de Aleatoriedad)
            # Como pusimos los obligatorios al inicio, si no los mezclamos,
            # las contraseñas siempre empezarían con: minúscula, mayúscula, número, especial.
            password_chars = self.motor.mezclar_lista(password_chars)
            
            # Une la lista de caracteres en un único string. "".join(lista) es el idioma estándar de Python para esto.
            contrasena_candidata = "".join(password_chars)
            
            # PASO 4: Validación estricta del resultado final
            if self._es_valida(contrasena_candidata):
                return contrasena_candidata
            
# Inicializamos nuestros componentes
motor = MotorCriptografico()
generador = GeneradorContrasenaAvanzado(longitud=12, motor_aleatorio=motor)

# Generamos 3 ejemplos distintos
print("Contraseña 1:", generador.generar())
print("Contraseña 2:", generador.generar())
print("Contraseña 3:", generador.generar())
