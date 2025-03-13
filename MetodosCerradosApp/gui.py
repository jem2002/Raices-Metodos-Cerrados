import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from metodos import bisection, false_position, velocity_function

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RootFinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Cerrados - Laboratorio 2")
        self.geometry("1200x1000")
        self._create_widgets()

    def _create_widgets(self):
        # Frame de entrada
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Campos de entrada
        self.a_entry = ctk.CTkEntry(input_frame, placeholder_text="a", width=120)
        self.a_entry.insert(0, "50")
        self.a_entry.pack(side="left", padx=5)
        self.b_entry = ctk.CTkEntry(input_frame, placeholder_text="b", width=120)
        self.b_entry.insert(0, "60")
        self.b_entry.pack(side="left", padx=5)
        self.tol_entry = ctk.CTkEntry(input_frame, placeholder_text="Tolerancia", width=120)
        self.tol_entry.insert(0, "0.001")
        self.tol_entry.pack(side="left", padx=5)

        # Botón de cálculo
        self.calculate_btn = ctk.CTkButton(input_frame, text="Calcular Ambos Métodos", command=self._calculate)
        self.calculate_btn.pack(side="left", padx=10)

        # Frame de resultados
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Tabla comparativa
        self.tree = ttk.Treeview(
            results_frame, 
            columns=("Método", "Iteración", "a", "b", "c", "f(c)", "Error"), 
            show="headings",
            height=10
        )
        self.tree.heading("Método", text="Método")
        self.tree.heading("Iteración", text="Iteración")
        self.tree.heading("a", text="a")
        self.tree.heading("b", text="b")
        self.tree.heading("c", text="c")
        self.tree.heading("f(c)", text="f(c)")
        self.tree.heading("Error", text="Error")
        self.tree.pack(side="top", fill="x", padx=5, pady=5)

        # Scrollbar para la tabla
        scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)

        # Gráficos divididos
        self.figure = plt.figure(figsize=(10, 5))
        self.ax1 = self.figure.add_subplot(121)  # Bisección
        self.ax2 = self.figure.add_subplot(122)  # Falsa Posición
        self.canvas = FigureCanvasTkAgg(self.figure, results_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _calculate(self):
        # Limpiar datos anteriores
        self.tree.delete(*self.tree.get_children())
        self.ax1.clear()
        self.ax2.clear()

        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
        except ValueError:
            self._show_error("Valores inválidos")
            return

        try:
            # Ejecutar ambos métodos
            root_bis, iter_bis = bisection(velocity_function, a, b, tol)
            root_fp, iter_fp = false_position(velocity_function, a, b, tol)
        except Exception as e:
            self._show_error(str(e))
            return

        # Llenar la tabla
        self._fill_table("Bisección", iter_bis)
        self._fill_table("Falsa Posición", iter_fp)

        # Graficar
        self._plot_method(self.ax1, iter_bis, "Bisección")
        self._plot_method(self.ax2, iter_fp, "Falsa Posición")
        self.canvas.draw()

    def _fill_table(self, method_name, iterations):
        for iter_data in iterations:
            self.tree.insert("", "end", values=(
                method_name,
                iter_data["Iteración"],
                f"{iter_data['a']:.4f}",
                f"{iter_data['b']:.4f}",
                f"{iter_data['c']:.6f}",
                f"{iter_data['f(c)']:.6f}",
                f"{iter_data['Error']:.6f}"
            ))

    def _plot_method(self, ax, iterations, title):
        m = [50 + (60 - 50) * i / 100 for i in range(100)]
        v = [velocity_function(x) for x in m]
        ax.plot(m, v, label="f(m)", color="blue")
        ax.scatter(
            [step["c"] for step in iterations],
            [0]*len(iterations),
            color="red",
            label="Aproximaciones"
        )
        ax.axhline(0, color="gray", linestyle="--")
        ax.set_title(title)
        ax.legend()

    def _show_error(self, message):
        self.tree.insert("", "end", values=("ERROR", message, "", "", "", "", ""))

if __name__ == "__main__":
    app = RootFinderApp()
    app.mainloop()