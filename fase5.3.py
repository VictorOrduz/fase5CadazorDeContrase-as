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
    """Se lanza cuando la entrada de longitud no es un número entero válido."""
    pass

class EspecialesInvalidosError(ErrorCazador):
    """Se lanza cuando el usuario ingresa letras, números o símbolos prohibidos."""
    pass

class ContrasenaIncorrectaError(ErrorCazador):
    """Se lanza si la contraseña generada falla el control estricto de calidad."""
    pass


# ==========================================
# CLASE: CONTRASEÑA
# ==========================================
class Contrasena:
    # El catálogo oficial de artefactos especiales permitidos en el juego
    ESPECIALES_PERMITIDOS = "¿¡?=)(/*+-%&$#!."

    def __init__(self, longitud_str: str, especiales_usuario: str):
        # 1. Validación estricta de los símbolos especiales del usuario
        self.especiales_limpios = self._validar_y_limpiar_especiales(especiales_usuario)
        
        # 2. Validación estricta de la longitud
        self.longitud = self._validar_entrada_numerica(longitud_str)
        
        # 3. Generación segura de la contraseña incorporando letras y números automáticamente
        self.valor = self._generar_y_validar()

    def _validar_y_limpiar_especiales(self, entrada: str) -> str:
        """Asegura que el usuario SOLO haya ingresado caracteres especiales permitidos y sin repetir."""
        if not entrada:
            raise EspecialesInvalidosError("¡Debes invocar al menos un carácter especial para forjar la llave!")
            
        # Eliminamos duplicados que el usuario haya puesto por error
        unicos = "".join(set(entrada))
        
        # Validación estricta: No se permiten letras ni números, solo el catálogo oficial
        for caracter in unicos:
            if caracter not in self.ESPECIALES_PERMITIDOS:
                raise EspecialesInvalidosError(
                    f"El carácter '{caracter}' es inválido o prohibido. "
                    f"Solo puedes usar estos símbolos: {self.ESPECIALES_PERMITIDOS}"
                )
        return unicos

    def _validar_entrada_numerica(self, entrada: str) -> int:
        if not entrada.isdigit():
            raise DatoNoNumericoError("¡La longitud debe ser un número entero válido!")
        
        valor = int(entrada)
        
        # Necesitamos mínimo 8 para cumplir los requisitos (1 min, 1 may, 1 num, 1 esp + 4 libres)
        if valor < 8:
            raise LongitudInvalidaError("¡Demasiado corta! La longitud mínima obligatoria es de 8 caracteres.")
            
        # El límite máximo físico depende de cuántas letras/números hay disponibles más los especiales del usuario
        # 26 minúsculas + 26 mayúsculas + 10 números + N especiales únicos del usuario
        max_posible = 26 + 26 + 10 + len(self.especiales_limpios)
        if valor > max_posible:
            raise LongitudInvalidaError(
                f"¡Demasiado larga! Con los {len(self.especiales_limpios)} especiales que diste, "
                f"el tamaño máximo sin repetir caracteres es de {max_posible}."
            )
            
        return valor

    def _es_valida(self, cadena: str) -> bool:
        """Valida estrictamente que cumpla con los requisitos y que use los especiales del usuario."""
        if len(set(cadena)) != len(cadena):
            return False
            
        tiene_min = any(c in string.ascii_lowercase for c in cadena)
        tiene_may = any(c in string.ascii_uppercase for c in cadena)
        tiene_num = any(c in string.digits for c in cadena)
        # Debe contener al menos uno de los especiales que el usuario configuró
        tiene_especial_usuario = any(c in self.especiales_limpios for c in cadena)
        
        return tiene_min and tiene_may and tiene_num and tiene_especial_usuario

    def _mezclar_seguro(self, lista: list) -> list:
        lista_mezclada = lista.copy()
        for i in range(len(lista_mezclada) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lista_mezclada[i], lista_mezclada[j] = lista_mezclada[j], lista_mezclada[i]
        return lista_mezclada

    def _generar_y_validar(self) -> str:
        # El pool total se compone de las letras/números del sistema + los especiales del usuario
        pool_letras_numeros = string.ascii_lowercase + string.ascii_uppercase + string.digits
        
        while True:
            # Forzamos los 4 requisitos mínimos en la lista base
            chars = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(self.especiales_limpios) # Uno de los del usuario obligatoriamente
            ]
            
            # Construimos un pool de remanentes excluyendo los ya seleccionados para evitar repeticiones
            pool_restante = [c for c in (pool_letras_numeros + self.especiales_limpios) if c not in chars]
            longitud_restante = self.longitud - len(chars)
            
            for _ in range(longitud_restante):
                if not pool_restante:
                    break
                seleccionado = secrets.choice(pool_restante)
                chars.append(seleccionado)
                pool_restante.remove(seleccionado)
                
            # Caos aleatorio en el orden
            chars = self._mezclar_seguro(chars)
            resultado = "".join(chars)
            
            if self._es_valida(resultado):
                return resultado
                
            raise ContrasenaIncorrectaError("La forja de la contraseña ha fallado inesperadamente.")


# ==========================================
# CLASE: COFRE
# ==========================================
class Cofre:
    RECOMPENSAS_BASE = {
        "Común": 10,
        "Raro": 25,
        "Legendario": 50
    }

    def __init__(self, es_valida: bool, longitud_password: int = 0, cant_especiales: int = 0):
        if es_valida:
            self.tipo = secrets.choice(list(self.RECOMPENSAS_BASE.keys()))
            base = self.RECOMPENSAS_BASE[self.tipo]
            
            # --- NUEVO SISTEMA DE PUNTUACIÓN DINÁMICO ---
            # Factor longitud: Contraseñas largas multiplican el puntaje. Cortas (8) mantienen el multiplicador bajo.
            factor_longitud = longitud_password / 10  # ej: longitud 15 = 1.5x
            
            # Factor especiales: Cada carácter especial único que el usuario configure suma +5 puntos de bonus
            bonus_especiales = cant_especiales * 5
            
            self.puntos = int((base * factor_longitud) + bonus_especiales)
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
        especiales_usuario = input("2. Introduce SOLO los caracteres especiales a inyectar: ")
        
        try:
            # Instanciamos el objeto Contraseña (el sistema genera automáticamente las letras y números)
            password_objeto = Contrasena(longitud_usuario, especiales_usuario)
            
            print(f"\n🔮 ¡Contraseña forjada automáticamente!: {password_objeto.valor}")
            
            # El cofre calcula el puntaje dinámico en base a la longitud y cantidad de especiales provistos
            cofre_abierto = Cofre(
                es_valida=True, 
                longitud_password=password_objeto.longitud, 
                cant_especiales=len(password_objeto.especiales_limpios)
            )
            print(f"🎁 ¡Has abierto un惊 Cofre [{cofre_abierto.tipo}]!")
            print(f"📊 Cálculo de Botín: (Base del cofre adaptada por longitud) + (Bonus por cantidad de símbolos).")
            print(f"✨ ¡Ganaste: +{cofre_abierto.puntos} puntos!")
            self.puntaje_acumulado += cofre_abierto.puntos

        except (DatoNoNumericoError, LongitudInvalidaError, EspecialesInvalidosError) as error:
            print(f"\n❌ ERROR DE CONFIGURACIÓN: {error}")
            print("⚠️ El hechizo falló. Perdiste el turno por malas especificaciones.")
            
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
        print("Reglas:")
        print("1. Elige una longitud (Mínimo 8). ¡A más larga, más puntos ganaras!")
        print(f"2. Ingresa SOLO caracteres especiales de esta lista: {Contrasena.ESPECIALES_PERMITIDOS}")
        print("   ¡Mientras más símbolos raros uses, mayor será tu bonus de puntos!")
        print("3. Las letras (A-Z, a-z) y números (0-9) se generan automáticamente sin repetirse.")
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