import secrets
import string

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorCazador(Exception):
    """Excepción base para el juego."""
    pass

class LongitudInvalidaError(ErrorCazador):
    """Se lanza cuando la longitud no cumple con los rangos permitidos (Muestra un error técnico)."""
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
        
        # VALIDACIÓN ESTRICTA: Si usa un carácter fuera de la lista, se desata la maldición
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
            
        max_posible = 26 + 26 + 10 + len(self.especiales_limpios)
        if valor > max_posible:
            raise LongitudInvalidaError(
                f"¡Demasiado larga! Con los {len(self.especiales_limpios)} especiales que diste, "
                f"el tamaño máximo sin repetir es de {max_posible}."
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
    RECOMPENSAS_BASE = {
        "Común": 10,
        "Raro": 25,
        "Legendario": 50
    }

    def __init__(self, tipo_fijo: str = None, longitud_password: int = 0, cant_especiales: int = 0):
        # Si le pasamos un tipo fijo (como "Maldito"), se salta la aleatoriedad
        if tipo_fijo == "Maldito":
            self.tipo = "Maldito"
            self.puntos = -20
        else:
            # Cofres buenos aleatorios
            self.tipo = secrets.choice(list(self.RECOMPENSAS_BASE.keys()))
            base = self.RECOMPENSAS_BASE[self.tipo]
            
            # Puntuación dinámica basada en la dificultad que eligió el usuario
            factor_longitud = longitud_password / 10  
            bonus_especiales = cant_especiales * 5
            self.puntos = int((base * factor_longitud) + bonus_especiales)


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
            # Intentamos crear la contraseña
            password_objeto = Contrasena(longitud_usuario, especiales_usuario)
            
            # Si todo sale bien, se abre un cofre de recompensa positivo
            print(f"\n🔮 ¡Contraseña forjada automáticamente!: {password_objeto.valor}")
            cofre_abierto = Cofre(
                longitud_password=password_objeto.longitud, 
                cant_especiales=len(password_objeto.especiales_limpios)
            )
            print(f"🎁 ¡Has abierto un Cofre [{cofre_abierto.tipo}]! (+{cofre_abierto.puntos} puntos)")
            self.puntaje_acumulado += cofre_abierto.puntos

        except EspecialesInvalidosError as error:
            # === AQUÍ ESTÁ TU NUEVO AJUSTE ===
            # Capturamos los caracteres prohibidos y desatamos la penalización directa
            print(f"\n💀 ERROR DE SELECCIÓN: {error}")
            cofre_maldito = Cofre(tipo_fijo="Maldito")
            print(f"🏮 ¡La codicia rompió el sello! Se abrió un Cofre [{cofre_maldito.tipo}] ({cofre_maldito.puntos} puntos)")
            self.puntaje_acumulado += cofre_maldito.puntos

        except (DatoNoNumericoError, LongitudInvalidaError) as error:
            # Los errores de formato de número o límites matemáticos solo te hacen perder el turno
            print(f"\n❌ ERROR DE CONFIGURACIÓN: {error}")
            print("⚠️ El hechizo falló. Perdiste el turno por malas especificaciones (sin penalización).")
            
        except ContrasenaIncorrectaError as error:
            # Error interno del motor de generación
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
        print("Reglas:")
        print("1. Elige una longitud adecuada (Mínimo 8).")
        print(f"2. Ingresa SOLO caracteres especiales de esta lista: {Contrasena.ESPECIALES_PERMITIDOS}")
        print("🔥 ¡CUIDADO!: Si ingresas letras, números o símbolos prohibidos,")
        print("   ¡invocarás un COFRE MALDITO y perderás 20 puntos de inmediato!")
        print("==================================================")
        
        jugando = True
        while jugando:
            jugando = self.ejecutar_ronda()


if __name__ == "__main__":
    partida = JuegoCazador()
    partida.iniciar()
