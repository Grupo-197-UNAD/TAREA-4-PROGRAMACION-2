# ===================== IMPORTACIONES =====================

import tkinter as tk  # Importa la librería para crear interfaces gráficas
from tkinter import messagebox  # Permite mostrar ventanas emergentes
from abc import ABC, abstractmethod  # Para crear clases abstractas
import datetime  # Para registrar fecha y hora en logs


# ===================== FUNCIÓN LOG =====================

def registrar_log(mensaje):  # Función para guardar errores o eventos
    with open("logs.txt", "a") as archivo:  # Abre archivo en modo agregar
        archivo.write(f"{datetime.datetime.now()} - {mensaje}\n")  # Escribe mensaje con fecha


# ===================== EXCEPCIONES PERSONALIZADAS =====================

class ErrorSistema(Exception):  # Clase base de errores del sistema
    pass  # No añade funcionalidad extra


class ErrorValidacion(ErrorSistema):  # Error para validaciones
    pass  # Hereda comportamiento


class ErrorReserva(ErrorSistema):  # Error en reservas
    pass  # Hereda comportamiento


# ===================== CLASE CLIENTE =====================

class Cliente:  # Clase para representar clientes

    def __init__(self, nombre, email):  # Constructor
        if not nombre or not email:  # Valida que no estén vacíos
            raise ErrorValidacion("Nombre o email inválido")  # Lanza error

        self.nombre = nombre  # Guarda nombre
        self.email = email  # Guarda email


# ===================== CLASE ABSTRACTA SERVICIO =====================

class Servicio(ABC):  # Clase abstracta

    def __init__(self, nombre, tarifa):  # Constructor
        self.nombre = nombre  # Nombre del servicio
        self.tarifa = tarifa  # Tarifa base

    @abstractmethod
    def calcular_costo(self, horas):  # Método abstracto
        pass  # Obligatorio implementar en hijos


# ===================== CLASES DERIVADAS =====================

class Sala(Servicio):  # Servicio tipo sala

    def calcular_costo(self, horas):  # Implementación
        return self.tarifa * horas  # Multiplica tarifa por horas


class Equipo(Servicio):  # Servicio de equipos

    def calcular_costo(self, horas):  # Implementación
        return (self.tarifa * horas) + 10  # Añade costo extra


class Asesoria(Servicio):  # Servicio de asesoría

    def calcular_costo(self, horas):  # Implementación
        return self.tarifa * horas * 1.2  # Aplica incremento


# ===================== CLASE RESERVA =====================

class Reserva:  # Clase para reservas

    def __init__(self, cliente, servicio, horas):  # Constructor

        if horas <= 0:  # Validación de horas
            raise ErrorReserva("Horas inválidas")  # Error si no es válido

        self.cliente = cliente  # Guarda cliente
        self.servicio = servicio  # Guarda servicio
        self.horas = horas  # Guarda duración
        self.estado = "Pendiente"  # Estado inicial

    def confirmar(self):  # Método confirmar reserva
        self.estado = "Confirmada"  # Cambia estado

    def calcular_total(self):  # Método para calcular costo total
        return self.servicio.calcular_costo(self.horas)  # Llama al servicio


# ===================== INTERFAZ GRÁFICA =====================

class App:  # Clase principal de la aplicación

    def __init__(self, root):  # Constructor de la interfaz

        self.root = root  # Guarda la ventana principal
        self.root.title("Software FJ - Sistema de Reservas")  # Título

        self.clientes = []  # Lista de clientes
        self.reservas = []  # Lista de reservas

        # ===== LABEL NOMBRE =====
        tk.Label(root, text="Nombre").grid(row=0, column=0)  # Texto nombre
        self.nombre_entry = tk.Entry(root)  # Campo de entrada
        self.nombre_entry.grid(row=0, column=1)  # Posición en grid

        # ===== LABEL EMAIL =====
        tk.Label(root, text="Email").grid(row=1, column=0)  # Texto email
        self.email_entry = tk.Entry(root)  # Campo entrada
        self.email_entry.grid(row=1, column=1)  # Posición

        # ===== LABEL HORAS =====
        tk.Label(root, text="Horas").grid(row=2, column=0)  # Texto horas
        self.horas_entry = tk.Entry(root)  # Campo entrada
        self.horas_entry.grid(row=2, column=1)  # Posición

        # ===== SELECCIÓN SERVICIO =====
        tk.Label(root, text="Servicio").grid(row=3, column=0)  # Texto servicio
        self.servicio_var = tk.StringVar()  # Variable para guardar selección
        self.servicio_var.set("Sala")  # Valor por defecto

        tk.OptionMenu(root, self.servicio_var, "Sala", "Equipo", "Asesoria").grid(row=3, column=1)  # Menú desplegable

        # ===== BOTÓN CREAR RESERVA =====
        tk.Button(root, text="Crear Reserva", command=self.crear_reserva).grid(row=4, column=0, columnspan=2)

        # ===== BOTÓN MOSTRAR =====
        tk.Button(root, text="Mostrar Reservas", command=self.mostrar_reservas).grid(row=5, column=0, columnspan=2)

        # ===== LISTA =====
        self.lista = tk.Listbox(root, width=60)  # Lista visual
        self.lista.grid(row=6, column=0, columnspan=2)  # Posición
        
        # ===== BOTÓN SALIR =====
        tk.Button(root, text="Salir del programa", command=root.quit, fg="red").grid(row=7, column=0, columnspan=2) # Crea botón de salida

    # ===================== FUNCIÓN CREAR RESERVA =====================
    def crear_reserva(self):

        try:  # Inicio manejo de errores

            nombre = self.nombre_entry.get()  # Obtiene nombre
            email = self.email_entry.get()  # Obtiene email
            
            # ===== VALIDACIÓN DE TIPO =====
            try: # Intenta realizar la conversion de tipo
                horas = float(self.horas_entry.get())  # Convierte horas a número decimal
            except ValueError:
                raise ErrorValidacion("El campo 'Horas' debe ser un valor numerico") # Lanza excepción personalizada
            
            cliente = Cliente(nombre, email)  # Crea cliente

            tipo = self.servicio_var.get()  # Obtiene tipo de servicio

            # Selección de servicio (polimorfismo)
            if tipo == "Sala":
                servicio = Sala("Sala", 50)
            elif tipo == "Equipo":
                servicio = Equipo("Equipo", 40)
            else:
                servicio = Asesoria("Asesoria", 100)

            reserva = Reserva(cliente, servicio, horas)  # Crea reserva
            reserva.confirmar()  # Confirma

            self.reservas.append(reserva)  # Guarda reserva

            messagebox.showinfo("Éxito", "Reserva creada correctamente")  # Mensaje éxito
            
            # ===== LLAMADA A LIMPIEZA =====
            self.limpiar_campo() # Llama a la funcion para limpiar el formulario

        except ErrorSistema as e:  # Captura errores personalizados
            registrar_log(str(e))  # Guarda en log
            messagebox.showerror("Error", str(e))  # Muestra error

        except Exception as e:  # Captura errores generales
            registrar_log("Error inesperado: " + str(e))  # Guarda
            messagebox.showerror("Error", "Error inesperado")  # Muestra mensaje

        finally:  # Siempre se ejecuta
            print("Intento de creación finalizado")  # Mensaje consola

    # ===================== MOSTRAR RESERVAS =====================
    def mostrar_reservas(self):

        self.lista.delete(0, tk.END)  # Limpia lista

        for r in self.reservas:  # Recorre reservas
            texto = f"{r.cliente.nombre} - {r.servicio.nombre} - ${r.calcular_total()} - {r.estado}"  # Formato
            self.lista.insert(tk.END, texto)  # Inserta en lista
    
   # ===== FUNCIÓN LIMPIAR CAMPOS =====
    def limpiar_campos(self): # Define método de limpieza
        self.nombre_entry.delete(0, tk.END) # Borra contenido del nombre
        self.email_entry.delete(0, tk.END) # Borra contenido del email
        self.horas_entry.delete(0, tk.END) # Borra contenido de las horas 
        self.nombre_entry.focus() # Pone el cursor de nuevo en el primer campo


# ===================== EJECUCIÓN =====================

if __name__ == "__main__":  # Punto de entrada del programa

    root = tk.Tk()  # Crea ventana principal
    app = App(root)  # Instancia la app
    root.mainloop()  # Ejecuta el loop de la interfaz