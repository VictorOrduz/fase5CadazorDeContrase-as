# cazador de contraseñas

''' Para la aleatoriedad en seguridad, usamos el módulo secrets de Python (diseñado para criptografía)
    en lugar de random (que es predecible).'''  
import secrets
import string

class MotorCriptografico:
    '''Clase responsable exclusivamente de la aleatoriedad segura.'''
    def elegir_caracter(self, opciones: str) -> str:
        return secrets.choice(opciones)


class GeneradorContrasena:
    def __init__(self, longitud: int, usar_mayusculas: bool, motor_aleatorio):
        # Guardamos el motor que maneja la aleatoriedad (Inyección de dependencias)
        self.motor = motor_aleatorio
        self.usar_mayusculas = usar_mayusculas
        
        # Usamos el setter para aplicar la validación estricta desde el nacimiento del objeto
        self.longitud = longitud

    @property
    def longitud(self) -> int:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: int):
        # VALIDACIÓN ESTRICTA: El objeto no permite configuraciones inseguras o absurdas
        if not isinstance(valor, int):
            raise TypeError("La longitud debe ser un número entero.")
        if valor < 8:
            raise ValueError("Por seguridad, la longitud mínima debe ser de 8 caracteres.")
        if valor > 128:
            raise ValueError("La longitud máxima permitida es de 128 caracteres.")
            
        self._longitud = valor

    def generar(self) -> str:
        """Crea la contraseña usando el pool de caracteres y el motor inyectado."""
        caracteres = string.ascii_lowercase + string.digits
        if self.usar_mayusculas:
            caracteres += string.ascii_uppercase

        # Construimos la contraseña interactuando con el motor de aleatoriedad
        contrasena = "".join(self.motor.elegir_caracter(caracteres) for _ in range(self.longitud))
        return contrasena