import secrets
import string

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorCazador(Exception):
    """Excepción base para el juego."""
    pass

class LongitudInvalidaError(ErrorCazador):
    """Se lanza cuando la longitud no cumple con los rangos permitidos."""
    pass

class DatoNoNumericoError(ErrorCazador):
    """Se lanza cuando la entrada de longitud no es un número entero."""
    pass

class EspecialesInvalidosError(ErrorCazador):
    """Se lanza cuando el usuario ingresa símbolos prohibidos (¡Invoca al Cofre Maldito!)."""
    pass

class ContrasenaIncorrectaError(ErrorCazador):
    """Se lanza si la contraseña generada falla el control de calidad interno."""
    pass


# ==========================================
# CLASE: CONTRASEÑA
# ==========================================
class Contrasena:
    # Catálogo oficial de artefactos especiales del juego
    ESPECIALES_PERMITIDOS = "¿¡?=)(/*+-%&$#!."

    def __init__(self, longitud_str: str, especiales_usuario: str):
        # 1. Validación estricta de los símbolos especiales
        self.especiales_limpios = self._validar_y_limpiar_especiales(especiales_usuario)
        
        # 2. Validación estricta de la longitud
        self.longitud = self._validar_entrada_numerica(longitud_str)
        
        # 3. Generación automática y segura
        self.valor = self._generar_y_validar()

    def _validar_y_limpiar_especiales(self, entrada: str) -> str:
        if not entrada:
            raise EspecialesInvalidosError("¡No puedes dejar la casilla vacía! Debes invocar al menos un símbolo permitido.")
            
        unicos = "".join(set(entrada))
        
        # Si usa un carácter fuera de la lista, se desata la maldición
        for caracter in unicos:
            if caracter not in self.ESPECIALES_PERMITIDOS:
                raise EspecialesInvalidosError(
                    f"Has intentado usar el carácter prohibido '{caracter}'. "
                    f"Solo se permiten estos artefactos: {self.ESPECIALES_PERMITIDOS}"
                )
        return unicos

    def _validar_entrada_numerica(self, entrada: str) -> int:
        if not entrada.isdigit():
            raise DatoNoNumericoError("¡La longitud debe ser un número entero válido!")
        
        valor = int(entrada)
        if valor < 8:
            raise LongitudInvalidaError("¡Demasiado corta! La longitud mínima obligatoria es de 8 caracteres.")
            
        # El límite máximo absoluto según las reglas del juego es 77
        if valor > 77:
            raise LongitudInvalidaError("¡Demasiado larga! La longitud máxima permitida en el juego es de 77 caracteres.")
            
        # Validación física interna: evitar repeticiones según el pool provisto por el usuario
        max_posible = 26 + 26 + 10 + len(self.especiales_limpios)
        if valor > max_posible:
            raise LongitudInvalidaError(
                f"¡Incoherencia matemática! Con los {len(self.especiales_limpios)} especiales que diste, "
                f"el tamaño máximo sin repetir es de {max_posible}. Agrega más caracteres especiales."
            )
            
        return valor

    def _es_valida(self, cadena: str) -> bool:
        if len(set(cadena)) != len(cadena):
            return False
        tiene_min = any(c in string.ascii_lowercase for c in cadena)
        tiene_may = any(c in string.ascii_uppercase for c in cadena)
        tiene_num = any(c in string.digits for c in cadena)
        tiene_esp = any(c in self.especiales_limpios for c in cadena)
        return tiene_min and tiene_may and tiene_num and tiene_esp

    def _mezclar_seguro(self, lista: list) -> list:
        lista_mezclada = lista.copy()
        for i in range(len(lista_mezclada) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lista_mezclada[i], lista_mezclada[j] = lista_mezclada[j], lista_mezclada[i]
        return lista_mezclada

    def _generar_y_validar(self) -> str:
        pool_letras_numeros = string.ascii_lowercase + string.ascii_uppercase + string.digits
        
        while True:
            chars = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(self.especiales_limpios)
            ]
            
            pool_restante = [c for c in (pool_letras_numeros + self.especiales_limpios) if c not in chars]
            longitud_restante = self.longitud - len(chars)
            
            for _ in range(longitud_restante):
                if not pool_restante:
                    break
                seleccionado = secrets.choice(pool_restante)
                chars.append(seleccionado)
                pool_restante.remove(seleccionado)
                
            chars = self._mezclar_seguro(chars)
            resultado = "".join(chars)
            
            if self._es_valida(resultado):
                return resultado
                
            raise ContrasenaIncorrectaError("La forja de la contraseña falló por un error de calidad interno.")


# ==========================================
# CLASE: COFRE
# ==========================================
class Cofre:
    def __init__(self, longitud_password: int = 0, forzar_maldito: bool = False):
        # Si se desató la excepción de caracteres prohibidos, se ignora la longitud y va directo al castigo
        if forzar_maldito:
            self.tipo = "Maldito"
            self.puntos = -20
        else:
            # NUEVO AJUSTE: Determinación estricta y fija por rangos de longitud
            if 8 <= longitud_password <= 25:
                self.tipo = "Común"
                self.puntos = 10
            elif 26 <= longitud_password <= 50:
                self.tipo = "Raro"
                self.puntos = 25
            elif 51 <= longitud_password <= 77:
                self.tipo = "Legendario"
                self.puntos = 50
            else:
                self.tipo = "Desconocido"
                self.puntos = 0


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
        especiales_usuario = input("2. Introduce SOLO los caracteres especiales a inyectar: ")
        
        try:
            # Intentamos forjar la contraseña aplicando validaciones
            password_objeto = Contrasena(longitud_usuario, especiales_usuario)
            
            print(f"\n🔮 ¡Contraseña forjada automáticamente!: {password_objeto.valor}")
            
            # El cofre evalúa directamente la longitud obtenida
            cofre_abierto = Cofre(longitud_password=password_objeto.longitud)
            print(f"🎁 ¡Has abierto un Cofre [{cofre_abierto.tipo}]! ✨ Puntaje básico asignado.")
            print(f"✨ ¡Ganaste: +{cofre_abierto.puntos} puntos!")
            self.puntaje_acumulado += cofre_abierto.puntos

        except EspecialesInvalidosError as error:
            # Penalización directa por usar símbolos corruptos / prohibidos
            print(f"\n💀 ERROR DE SELECCIÓN: {error}")
            cofre_maldito = Cofre(forzar_maldito=True)
            print(f"🏮 ¡La codicia rompió el sello! Se abrió un Cofre [{cofre_maldito.tipo}] ({cofre_maldito.puntos} puntos)")
            self.puntaje_acumulado += cofre_maldito.puntos

        except (DatoNoNumericoError, LongitudInvalidaError) as error:
            # Errores técnicos de tipeo o límites insuperables solo saltan el turno
            print(f"\n❌ ERROR DE CONFIGURACIÓN: {error}")
            print("⚠️ El hechizo falló. Perdiste el turno por malas especificaciones (sin penalización).")
            
        except ContrasenaIncorrectaError as error:
            print(f"\n⚙️ ERROR TÉCNICO: {error}")
            print("⚠️ El motor no pudo procesar la solicitud. Intenta de nuevo.")
            
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
        print("Tabla de Recompensas de la Mazmorra:")
        print("  • Longitud de 8 a 25  -> 🎁 Cofre Común (+10 pts)")
        print("  • Longitud de 26 a 50 -> 🎁 Cofre Raro (+25 pts)")
        print("  • Longitud de 51 a 77 -> 🎁 Cofre Legendario (+50 pts)")
        print(f"\nRegla de Símbolos Especiales Permitidos: {Contrasena.ESPECIALES_PERMITIDOS}")
        print("🔥 ¡ALERTA!: Si digitas letras, números o símbolos prohibidos en la segunda casilla,")
        print("   ¡invocarás de inmediato un COFRE MALDITO (-20 pts)!")
        print("==================================================")
        
        jugando = True
        while jugando:
            jugando = self.ejecutar_ronda()


if __name__ == "__main__":
    partida = JuegoCazador()
    partida.iniciar()