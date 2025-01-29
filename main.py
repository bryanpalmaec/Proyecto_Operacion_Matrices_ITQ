# Proyecto Final
# Elaborado por: Casa, Palma, Piedra, Hidalgo, Zumárraga, Lopez
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QMessageBox,
)
import sys
import numpy as np
from sympy import Matrix

class AplicacionMatrices(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones con Matrices")
        self.setGeometry(200, 100, 800, 600)  # Posición (200, 100) y tamaño (800x600)
        self.layout = QVBoxLayout()

        # Configuración inicial
        self.crear_interfaz()
        self.setLayout(self.layout)

    def crear_interfaz(self):
        # Layouts
        titulo_layout = QHBoxLayout()
        control_layout = QHBoxLayout()
        entrada_layout = QGridLayout()
        botones_layout = QHBoxLayout()
        salida_layout = QGridLayout()

        # Agregar logo en la sección de Título
        logo_label = QLabel()
        imagen_logo = QPixmap("recursos/logo.png")  # Ruta relativa a la imagen
        logo_label.setPixmap(imagen_logo)
        titulo_layout.addWidget(logo_label,alignment=Qt.AlignmentFlag.AlignCenter)

        # Controles para dimensiones de matrices
        #Matriz 1
        #Dimensiones de Filas Matriz 1
        control_layout.addWidget(QLabel("Filas Matriz 1:"))
        self.incremental_filas1 = (
            QSpinBox() # Tipo de objeto para modificar las filas de las Matriz 1
        )
        self.incremental_filas1.setValue(1)  # Valor por defecto = 1
        self.incremental_filas1.valueChanged.connect(
            self.act_matriz1_dimensiones
        ) # Conecta el valor del spinbox con las dimensiones de la tabla
        control_layout.addWidget(self.incremental_filas1)
        # Dimensiones de Columnas Matriz 1
        control_layout.addWidget(QLabel("Columnas Matriz 1:"))
        self.incremental_columnas1 = QSpinBox()
        self.incremental_columnas1.setValue(1)
        self.incremental_columnas1.valueChanged.connect(self.act_matriz1_dimensiones)
        control_layout.addWidget(self.incremental_columnas1)

        # Matriz 2
        # Dimensiones de Filas Matriz 2
        control_layout.addWidget(QLabel("Filas Matriz 2:"))
        self.incremental_filas2 = QSpinBox()
        self.incremental_filas2.setValue(1)
        self.incremental_filas2.valueChanged.connect(self.act_matriz2_dimensiones)
        control_layout.addWidget(self.incremental_filas2)
        # Dimensiones de Columnas Matriz 1
        control_layout.addWidget(QLabel("Columnas Matriz 2:"))
        self.incremental_columnas2 = QSpinBox()
        self.incremental_columnas2.setValue(1)
        self.incremental_columnas2.valueChanged.connect(self.act_matriz2_dimensiones)
        control_layout.addWidget(self.incremental_columnas2)

        # Matriz 1
        entrada_layout.addWidget(QLabel("Matriz 1"), 0, 0) #Posición (0,0) de la cuadrícula
        self.matriz1 = QTableWidget(1, 1)  # Tabla de entrada para Matriz 1
        entrada_layout.addWidget(self.matriz1, 1, 0) #Posición (1,0) de la cuadrícula

        # Matriz 2
        entrada_layout.addWidget(QLabel("Matriz 2"), 0, 1) #Posición (0,1) de la cuadrícula
        self.matriz2 = QTableWidget(1, 1)  # Tabla de entrada para Matriz 2
        entrada_layout.addWidget(self.matriz2, 1, 1) #Posición (1,1) de la cuadrícula

        # Botones para operaciones
        self.boton_suma = QPushButton("Suma")
        self.boton_suma.clicked.connect(self.sumar_matrices)
        botones_layout.addWidget(self.boton_suma)

        self.boton_resta = QPushButton("Resta")
        self.boton_resta.clicked.connect(self.restar_matrices)
        botones_layout.addWidget(self.boton_resta)

        self.boton_mutiplicar = QPushButton("Multiplicación")
        self.boton_mutiplicar.clicked.connect(self.multiplicar_matrices)
        botones_layout.addWidget(self.boton_mutiplicar)

        self.boton_gaussjordan = QPushButton("Gauss-Jordan")
        self.boton_gaussjordan.clicked.connect(self.gaussjordan_matrices)
        botones_layout.addWidget(self.boton_gaussjordan)

        # Resultado
        salida_layout.addWidget(QLabel("RESULTADO: "), 0, 0)
        self.resultado_matriz = QTableWidget(1, 1)
        salida_layout.addWidget(self.resultado_matriz, 1, 0)

        # Agregar al layout principal
        self.layout.addLayout(titulo_layout)
        self.layout.addLayout(control_layout)
        self.layout.addLayout(entrada_layout)
        self.layout.addLayout(botones_layout)
        self.layout.addLayout(salida_layout)

    def act_matriz1_dimensiones(self):
        filas = self.incremental_filas1.value()
        columnas = self.incremental_columnas1.value()
        self.matriz1.setRowCount(filas)
        self.matriz1.setColumnCount(columnas)

    def act_matriz2_dimensiones(self):
        filas = self.incremental_filas2.value()
        columnas = self.incremental_columnas2.value()
        self.matriz2.setRowCount(filas)
        self.matriz2.setColumnCount(columnas)

    def obtener_matriz(self, tabla):
        filas = tabla.rowCount()
        columnas = tabla.columnCount()
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                try:
                    valor = float(tabla.item(i, j).text()) if tabla.item(i, j) else 0
                except ValueError:
                    valor = 0
                fila.append(valor)
            matriz.append(fila)
        return np.array(matriz)

    def imprimir_resultado(self, tabla, matriz):
        filas, columnas = matriz.shape
        tabla.setRowCount(filas)
        tabla.setColumnCount(columnas)
        for i in range(filas):
            for j in range(columnas):
                tabla.setItem(i, j, QTableWidgetItem(str(matriz[i, j])))

    def sumar_matrices(self):
        matriz1 = self.obtener_matriz(self.matriz1)
        matriz2 = self.obtener_matriz(self.matriz2)
        if matriz1.shape != matriz2.shape:
            QMessageBox.warning(
                self, "Error", "Error: Las dimensiones no coinciden para la suma."
            )
        else:
            try:
                resultado = np.array(matriz1)+np.array(matriz2)
                self.imprimir_resultado(self.resultado_matriz, resultado)
            except ValueError:
                QMessageBox.warning(
                self, "Error", "Error: Compruebe los valores ingresados."
                )
    def restar_matrices(self):
        matriz1 = self.obtener_matriz(self.matriz1)
        matriz2 = self.obtener_matriz(self.matriz2)
        if matriz1.shape != matriz2.shape:
            QMessageBox.warning(
                self, "Error", "Error: Las dimensiones no coinciden para la resta."
            )
        else:
            try:
                resultado = matriz1 - matriz2
                self.imprimir_resultado(self.resultado_matriz, resultado)
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "Error: Las dimensiones no coinciden para la resta."
                    )

    def multiplicar_matrices(self):
        matriz1 = self.obtener_matriz(self.matriz1)
        matriz2 = self.obtener_matriz(self.matriz2)
        try:
            resultado = np.dot(matriz1, matriz2)
            self.imprimir_resultado(self.resultado_matriz, resultado)
        except ValueError:
            QMessageBox.warning(
                self,
                "Error",
                "Error: Las dimensiones no son compatibles para la multiplicación.",
            )
            return

    def gaussjordan_matrices(self):
        matriz1 = self.obtener_matriz(self.matriz1)
        try:
            sympy_matriz = Matrix(matriz1)
            rref_matriz, _ = sympy_matriz.rref()
            resultado = np.array(rref_matriz, dtype=float)
            self.imprimir_resultado(self.resultado_matriz, resultado)
        except ValueError:
            QMessageBox.warning(
                self,
                "Error",
                "Error: La matriz no es apta para aplicar Gauss-Jordan.",
            )
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AplicacionMatrices()
    window.show()
    sys.exit(app.exec())
