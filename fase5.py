# cazador de contraseñas

''' Para la aleatoriedad en seguridad, usamos el módulo secrets de Python (diseñado para criptografía)
    en lugar de random (que es predecible).'''  
import secrets
import string

class MotorCriptografico:
    """Clase responsable de la aleatoriedad segura."""
    def elegir_caracter(self, opciones: str) -> str:
        return secrets.choice(opciones)
    
    def mezclar_lista(self, lista: list) -> list:
        """Mezcla una lista de caracteres de forma segura e impredecible."""
        # Creamos una copia para no mutar la original directamente
        lista_mezclada = lista.copy()
        # Algoritmo de mezcla usando secretos criptográficos
        for i in range(len(lista_mezclada) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lista_mezclada[i], lista_mezclada[j] = lista_mezclada[j], lista_mezclada[i]
        return lista_mezclada


class GeneradorContrasenaAvanzado:
    # Lista de caracteres especiales obligatorios solicitados
    ESPECIALES = "¿¡?=)(/*+-%&$#!."

    def __init__(self, longitud: int, motor_aleatorio):
        self.motor = motor_aleatorio
        # Validación estricta de la longitud al instanciar el objeto
        self.longitud = longitud

    @property
    def longitud(self) -> int:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("La longitud debe ser un número entero.")
        if valor < 8:
            raise ValueError("Por seguridad, la longitud mínima debe ser de 8 caracteres.")
        
        # Validación estricta física: el pool total de caracteres únicos disponibles
        # (26 min + 26 may + 10 num + 15 esp = 77). No podemos pedir más de 77 caracteres sin repetir.
        pool_maximo = 26 + 26 + 10 + len(self.ESPECIALES)
        if valor > pool_maximo:
            raise ValueError(f"Para evitar caracteres repetidos, la longitud máxima admisible es de {pool_maximo} caracteres.")
            
        self._longitud = valor

    def _es_valida(self, contrasena: str) -> bool:
        """VALIDACIÓN ESTRICTA: Verifica que la contraseña cumpla TODAS las reglas."""
        # 1. No debe tener caracteres repetidos
        if len(set(contrasena)) != len(contrasena):
            return False
            
        # 2. Verificar presencia de cada grupo obligatorio
        tiene_minuscula = any(c in string.ascii_lowercase for c in contrasena)
        tiene_mayuscula = any(c in string.ascii_uppercase for c in contrasena)
        tiene_numero = any(c in string.digits for c in contrasena)
        tiene_especial = any(c in self.ESPECIALES for c in contrasena)

        return tiene_minuscula and tiene_mayuscula and tiene_numero and tiene_especial

    def generar(self) -> str:
        """Genera y valida estrictamente la contraseña antes de retornarla."""
        pool_total = string.ascii_lowercase + string.ascii_uppercase + string.digits + self.ESPECIALES
        
        # Bucle de control: se repite hasta que la contraseña sea 100% válida
        while True:
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
