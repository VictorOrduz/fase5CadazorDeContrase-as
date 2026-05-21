import secrets
import string

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorCazador(Exception):
    """Excepción base para el juego."""
    pass

class LongitudInvalidaError(ErrorCazador):
    """Se lanza cuando la longitud no cumple con los rangos permitidos (8-77)."""
    pass

class DatoNoNumericoError(ErrorCazador):
    """Se lanza cuando la entrada del usuario no es un número entero válido."""
    pass

class PoolCaracteresInvalidoError(ErrorCazador):
    """Se lanza cuando los caracteres provistos por el usuario no cumplen con los mínimos requeridos."""
    pass

class ContrasenaIncorrectaError(ErrorCazador):
    """Se lanza cuando la contraseña generada falla el control estricto de calidad."""
    pass


# ==========================================
# CLASE: CONTRASEÑA
# ==========================================
class Contrasena:
    ESPECIALES_PERMITIDOS = "¿¡?=)(/*+-%&$#!."

    def __init__(self, longitud_str: str, pool_usuario: str):
        # 1. Validación estricta del texto de entrada del usuario
        self.pool_limpio = self._validar_y_limpiar_pool(pool_usuario)
        self.longitud = self._validar_entrada_numerica(longitud_str)
        
        # 2. Una vez configurado el entorno seguro, generamos el valor
        self.valor = self._generar_y_validar()

    def _validar_y_limpiar_pool(self, pool: str) -> str:
        """Asegura que el pool del usuario contenga al menos un elemento de cada grupo obligatorio."""
        # Eliminamos duplicados que el usuario haya metido por error para analizar los caracteres únicos
        caracteres_unicos = "".join(set(pool))
        
        # Filtramos qué elementos válidos ingresó de cada categoría obligatoria
        minusculas = [c for c in caracteres_unicos if c in string.ascii_lowercase]
        mayusculas = [c for c in caracteres_unicos if c in string.ascii_uppercase]
        numeros = [c for c in caracteres_unicos if c in string.digits]
        especiales = [c for c in caracteres_unicos if c in self.ESPECIALES_PERMITIDOS]
        
        # VALIDACIÓN ESTRICTA: Si falta algún grupo, lanzamos excepción personalizada
        faltantes = []
        if not minusculas: faltantes.append("una letra minúscula")
        if not mayusculas: faltantes.append("una letra mayúscula")
        if not numeros: faltantes.append("un número")
        if not especiales: faltantes.append(f"un carácter especial de la lista ({self.ESPECIALES_PERMITIDOS})")
        
        if faltantes:
            error_msg = "Tus caracteres no sirven para forjar la llave. Te falta: " + ", ".join(faltantes)
            raise PoolCaracteresInvalidoError(error_msg)
            
        return caracteres_unicos

    def _validar_entrada_numerica(self, entrada: str) -> int:
        if not entrada.isdigit():
            raise DatoNoNumericoError("¡Eso no es un número! Debes ingresar caracteres numéricos.")
        
        valor = int(entrada)
        
        if valor < 8:
            raise LongitudInvalidaError("¡Demasiado corta! La longitud mínima obligatoria es de 8 caracteres.")
            
        # El tamaño máximo ahora depende de cuántos caracteres únicos nos dio el usuario
        pool_maximo = len(self.pool_limpio)
        if valor > pool_maximo:
            raise LongitudInvalidaError(
                f"¡Demasiado larga! Con los caracteres que nos diste, la longitud máxima sin repetir es de {pool_maximo}."
            )
        
        return valor

    def _es_valida(self, cadena: str) -> bool:
        """Verifica que no haya duplicados y que mantenga los 4 requisitos obligatorios."""
        if len(set(cadena)) != len(cadena):
            return False
            
        tiene_min = any(c in string.ascii_lowercase for c in cadena)
        tiene_may = any(c in string.ascii_uppercase for c in cadena)
        tiene_num = any(c in string.digits for c in cadena)
        tiene_esp = any(c in self.ESPECIALES_PERMITIDOS for c in cadena)
        
        return tiene_min and tiene_may and tiene_num and tiene_esp

    def _mezclar_seguro(self, lista: list) -> list:
        lista_mezclada = lista.copy()
        for i in range(len(lista_mezclada) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lista_mezclada[i], lista_mezclada[j] = lista_mezclada[j], lista_mezclada[i]
        return lista_mezclada

    def _generar_y_validar(self) -> str:
        # Separamos los caracteres ingresados por el usuario para garantizar los obligatorios
        minusculas = [c for c in self.pool_limpio if c in string.ascii_lowercase]
        mayusculas = [c for c in self.pool_limpio if c in string.ascii_uppercase]
        numeros = [c for c in self.pool_limpio if c in string.digits]
        especiales = [c for c in self.pool_limpio if c in self.ESPECIALES_PERMITIDOS]
        
        # Bucle de control por si ocurre una mutación inválida al rellenar de forma aleatoria
        while True:
            # Aseguramos un elemento obligatorio de los conjuntos del usuario
            chars = [
                secrets.choice(minusculas),
                secrets.choice(mayusculas),
                secrets.choice(numeros),
                secrets.choice(especiales)
            ]
            
            # El resto se rellena con el pool del usuario, evitando los que ya elegimos para cumplir el "sin repetir"
            caracteres_restantes = [c for c in self.pool_limpio if c not in chars]
            longitud_restante = self.longitud - len(chars)
            
            for _ in range(longitud_restante):
                if not caracteres_restantes:
                    break
                seleccionado = secrets.choice(caracteres_restantes)
                chars.append(seleccionado)
                caracteres_restantes.remove(seleccionado) # Evita repeticiones físicas
                
            # Quitamos el orden predecible
            chars = self._mezclar_seguro(chars)
            resultado = "".join(chars)
            
            if self._es_valida(resultado):
                return resultado
                
            raise ContrasenaIncorrectaError("La contraseña generada rompió las reglas del juego de forma imprevista.")


# ==========================================
# CLASE: COFRE
# ==========================================
class Cofre:
    RECOMPENSAS = {
        "Común": 10,
        "Raro": 25,
        "Legendario": 50
    }

    def __init__(self, es_valida: bool):
        if es_valida:
            self.tipo = secrets.choice(list(self.RECOMPENSAS.keys()))
            self.puntos = self.RECOMPENSAS[self.tipo]
        else:
            self.tipo = "Maldito"
            self.puntos = -20


# ==========================================
# CLASE: JUEGO CAZADOR
# ==========================================
class JuegoCazador:
    def __init__(self):
        self.puntaje_acumulado = 0
        self.ronda = 1

    def ejecutar_ronda(self) -> bool:
        print(f"\n=== RONDA {self.ronda} ===")
        print(f"Puntaje Actual: {self.puntaje_acumulado} pts")
        
        longitud_usuario = input("1. Introduce la longitud de la contraseña: ")
        pool_usuario = input("2. Introduce los caracteres permitidos a usar: ")
        
        try:
            # Intentamos instanciar el objeto Contraseña pasándole ambos datos del usuario
            password_objeto = Contrasena(longitud_usuario, pool_usuario)
            
            print(f"\n🔮 ¡Contraseña conjurada con éxito!: {password_objeto.valor}")
            cofre_abierto = Cofre(es_valida=True)
            print(f"🎁 ¡Has abierto un Cofre [{cofre_abierto.tipo}]! (+{cofre_abierto.puntos} puntos)")
            self.puntaje_acumulado += cofre_abierto.puntos

        except (DatoNoNumericoError, LongitudInvalidaError, PoolCaracteresInvalidoError) as error:
            # Atrapa cualquier error de configuración o carencia de caracteres
            print(f"\n❌ ERROR DE CONFIGURACIÓN: {error}")
            print("⚠️ Perdiste el turno por malas especificaciones.")
            
        except ContrasenaIncorrectaError as error:
            print(f"\n💀 ERROR DE CALIDAD: {error}")
            cofre_maldito = Cofre(es_valida=False)
            print(f"🏮 ¡Se activó un Cofre [{cofre_maldito.tipo}]! ({cofre_maldito.puntos} puntos)")
            self.puntaje_acumulado += cofre_maldito.puntos
            
        self.ronda += 1
        
        while True:
            decision = input("\n¿Quieres seguir cazando contraseñas? (s/n): ").strip().lower()
            if decision == 's':
                return True
            elif decision == 'n':
                print(f"\nTe retiras de la mazmorra con un botín total de: {self.puntaje_acumulado} puntos.")
                return False
            print("Opción inválida. Presiona 's' para continuar o 'n' para salir.")

    def iniciar(self):
        print("==================================================")
        print("⚔️  ¡BIENVENIDO AL JUEGO DEL CAZADOR DE CONTRASENAS! ⚔️")
        print("==================================================")
        print(f"Reglas: Tú das los caracteres, pero la contraseña debe tener al menos:")
        print(f"una minúscula, una mayúscula, un número y un especial de estos: {Contrasena.ESPECIALES_PERMITIDOS}")
        print("¡Y no se puede repetir ninguno!")
        print("==================================================")
        
        jugando = True
        while jugando:
            jugando = self.ejecutar_ronda()


# ==========================================
# INVOCACIÓN DEL JUEGO
# ==========================================
if __name__ == "__main__":
    partida = JuegoCazador()
    partida.iniciar()
    
    