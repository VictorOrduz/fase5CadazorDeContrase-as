import secrets
import string

# ==========================================
# EXCEPCIONES PERSONALIZADAS (Validación Estricta)
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

class ContrasenaIncorrectaError(ErrorCazador):
    """Se lanza cuando la contraseña generada falla el control estricto de calidad."""
    pass


# ==========================================
# CLASE: CONTRASEÑA
# ==========================================
class Contrasena:
    ESPECIALES = "¿¡?=)(/*+-%&$#!."

    def __init__(self, longitud_str: str):
        # Validamos estrictamente que la entrada sea numérica
        self.longitud = self._validar_entrada_numerica(longitud_str)
        self.valor = self._generar_y_validar()

    def _validar_entrada_numerica(self, entrada: str) -> int:
        if not entrada.isdigit():
            raise DatoNoNumericoError("¡Eso no es un número! Debes ingresar caracteres numéricos.")
        
        valor = int(entrada)
        pool_maximo = 26 + 26 + 10 + len(self.ESPECIALES) # 77 caracteres únicos máximos
        
        if valor < 8:
            raise LongitudInvalidaError("¡Demasiado corta! La longitud mínima obligatoria es de 8 caracteres.")
        if valor > pool_maximo:
            raise LongitudInvalidaError(f"¡Demasiado larga! Para evitar repetir caracteres, el máximo es {pool_maximo}.")
        
        return valor

    def _es_valida(self, cadena: str) -> bool:
        """Verifica los 4 grupos obligatorios y la ausencia de duplicados."""
        if len(set(cadena)) != len(cadena):
            return False
            
        tiene_min = any(c in string.ascii_lowercase for c in cadena)
        tiene_may = any(c in string.ascii_uppercase for c in cadena)
        tiene_num = any(c in string.digits for c in cadena)
        tiene_esp = any(c in self.ESPECIALES for c in cadena)
        
        return tiene_min and tiene_may and tiene_num and tiene_esp

    def _mezclar_seguro(self, lista: list) -> list:
        """Mezcla aleatoria usando criptografía para evitar orden predecible."""
        lista_mezclada = lista.copy()
        for i in range(len(lista_mezclada) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lista_mezclada[i], lista_mezclada[j] = lista_mezclada[j], lista_mezclada[i]
        return lista_mezclada

    def _generar_y_validar(self) -> str:
        """Genera la contraseña. Si falla la validación, lanza la excepción de negocio."""
        pool_total = string.ascii_lowercase + string.ascii_uppercase + string.digits + self.ESPECIALES
        
        # Construimos una candidata
        chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(self.ESPECIALES)
        ]
        
        for _ in range(self.longitud - len(chars)):
            chars.append(secrets.choice(pool_total))
            
        chars = self._mezclar_seguro(chars)
        resultado = "".join(chars)
        
        # Simulación de validación estricta de salida
        if not self._es_valida(resultado):
            raise ContrasenaIncorrectaError("La contraseña generada mutó erróneamente y rompió las reglas.")
            
        return resultado


# ==========================================
# CLASE: COFRE
# ==========================================
class Cofre:
    # Tipos de cofres válidos y sus recompensas
    RECOMPENSAS = {
        "Común": 10,
        "Raro": 25,
        "Legendario": 50
    }

    def __init__(self, es_valida: bool):
        if es_valida:
            # Selecciona un cofre positivo al azar
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
        longitud_usuario = input("Introduce la longitud para conjurar tu contraseña: ")
        
        try:
            # Intentamos instanciar el objeto Contraseña (aquí se disparan las validaciones)
            password_objeto = Contrasena(longitud_usuario)
            
            # Si pasa, la contraseña es totalmente válida
            print(f"\n🔮 ¡Contraseña conjurada con éxito!: {password_objeto.valor}")
            cofre_abierto = Cofre(es_valida=True)
            print(f"🎁 ¡Has abierto un Cofre [{cofre_abierto.tipo}]! (+{cofre_abierto.puntos} puntos)")
            self.puntaje_acumulado += cofre_abierto.puntos

        except (DatoNoNumericoError, LongitudInvalidaError) as error:
            # Captura errores de entrada de datos
            print(f"\n❌ ERROR DE CONFIGURACIÓN: {error}")
            print("⚠️ Perdiste el turno por malas coordenadas.")
            
        except ContrasenaIncorrectaError as error:
            # Captura fallos de la contraseña en sí misma (invoca al cofre maldito)
            print(f"\n💀 ERROR DE CALIDAD: {error}")
            cofre_maldito = Cofre(es_valida=False)
            print(f"🏮 ¡Se activó un Cofre [{cofre_maldito.tipo}]! ({cofre_maldito.puntos} puntos)")
            self.puntaje_acumulado += cofre_maldito.puntos
            
        self.ronda += 1
        
        # Menú de continuación
        while True:
            decision = input("\n¿Quieres seguir cazando contraseñas? (s/n): ").strip().lower()
            if decision == 's':
                return True
            elif decision == 'n':
                print(f"\nPrudente decisión. Te retiras con un botín total de: {self.puntaje_acumulado} puntos.")
                return False
            print("Opción inválida. Presiona 's' para continuar o 'n' para salir.")

    def iniciar(self):
        print("==================================================")
        print("⚔️  ¡BIENVENIDO AL JUEGO DEL CAZADOR DE CONTRASENAS! ⚔️")
        print("==================================================")
        print("Reglas: Genera llaves perfectas sin repetir caracteres.")
        print("Deben incluir: Mayúscula, Minúscula, Número y Especial (¿¡?=)(/*+-%&$#!.).")
        
        jugando = True
        while jugando:
            jugando = self.ejecutar_ronda()


# ==========================================
# INVIOCACIÓN DEL JUEGO
# ==========================================
if __name__ == "__main__":
    partida = JuegoCazador()
    partida.iniciar()   
    
    