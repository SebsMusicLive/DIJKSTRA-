import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import heapq
import math

class SimuladorDijkstra:
    def __init__(self, root):
        self.root = root
        self.root.title("Routing Simulator")
        self.root.geometry("1280x800")
        self.root.configure(bg="#09090B")
        
        self.colores = {
            "bg_base": "#09090B",
            "bg_panel": "#18181B",
            "bg_canvas": "#000000",
            "texto_primario": "#FAFAFA",
            "texto_sec": "#A1A1AA",
            "nodo_base": "#3B82F6",
            "nodo_sel": "#F59E0B",
            "enlace_base": "#3F3F46",
            "ruta_principal": "#10B981",
            "ruta_alt": "#8B5CF6",
            "bg_input": "#27272A",
            "terminal_fg": "#4ADE80",
            "terminal_bg": "#050505"
        }

        self.nodos = {}
        self.red = {}
        self.rutas_optimas = []
        
        self.nodo_origen_enlace = None
        self.nodo_arrastrado = None
        self.modo_actual = "NODO"
        self.botones_modo = {}
        
        self.configurar_ui()

    def configurar_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Primary.TButton', font=('Segoe UI', 11, 'bold'), foreground='#000000', background=self.colores["ruta_principal"], borderwidth=0, padding=12)
        style.map('Primary.TButton', background=[('active', '#34D399')])
        
        style.configure('Danger.TButton', font=('Segoe UI', 11, 'bold'), foreground='#FFFFFF', background='#E11D48', borderwidth=0, padding=12)
        style.map('Danger.TButton', background=[('active', '#BE123C')])

        main_frame = tk.Frame(self.root, bg=self.colores["bg_base"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.frame_canvas = tk.Frame(main_frame, bg=self.colores["bg_canvas"], bd=1, relief="solid")
        self.frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        self.canvas = tk.Canvas(self.frame_canvas, bg=self.colores["bg_canvas"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_press_izq)    
        self.canvas.bind("<B1-Motion>", self.on_drag)             
        self.canvas.bind("<ButtonRelease-1>", self.on_release_izq)
        self.canvas.bind("<Double-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", lambda e: self.ejecutar_borrado(e.x, e.y))        
        
        self.frame_controles = tk.Frame(main_frame, width=380, bg=self.colores["bg_panel"], bd=0)
        self.frame_controles.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_controles.pack_propagate(False)
        
        header_frame = tk.Frame(self.frame_controles, bg=self.colores["bg_panel"])
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 15))
        tk.Label(header_frame, text="R O U T I N G   E N G I N E", font=("Segoe UI", 14, "bold"), bg=self.colores["bg_panel"], fg=self.colores["texto_primario"], anchor="w").pack(fill=tk.X)
        tk.Label(header_frame, text="Estudiante: Johan Sebastián López Ortega", font=("Segoe UI", 9), bg=self.colores["bg_panel"], fg=self.colores["texto_sec"], anchor="w").pack(fill=tk.X, pady=(5, 0))
        tk.Label(header_frame, text="Código: 1152196", font=("Segoe UI", 9), bg=self.colores["bg_panel"], fg=self.colores["texto_sec"], anchor="w").pack(fill=tk.X)
        tk.Frame(header_frame, height=1, bg=self.colores["enlace_base"]).pack(fill=tk.X, pady=(10, 0))
        
        toolbar_frame = tk.Frame(self.frame_controles, bg=self.colores["bg_panel"])
        toolbar_frame.pack(fill=tk.X, padx=30, pady=10)
        
        toolbar_frame.columnconfigure(0, weight=1)
        toolbar_frame.columnconfigure(1, weight=1)

        modos_config = [
            ("SELECCION", "↖  Seleccionar"),
            ("NODO", "⨁  Añadir Router"),
            ("ENLACE", "🔗  Conectar"),
            ("BORRAR", "✖  Eliminar")
        ]

        for i, (val, texto) in enumerate(modos_config):
            btn = tk.Button(toolbar_frame, text=texto, font=("Segoe UI", 10, "bold"), bg=self.colores["bg_input"], fg=self.colores["texto_sec"], bd=0, relief="flat", cursor="hand2", activebackground=self.colores["ruta_principal"], activeforeground="#000000", pady=8, command=lambda m=val: self.set_modo(m))
            btn.grid(row=i//2, column=i%2, padx=4, pady=4, sticky="ew")
            self.botones_modo[val] = btn

        self.set_modo("NODO")
        
        form_frame = tk.Frame(self.frame_controles, bg=self.colores["bg_panel"])
        form_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(form_frame, text="ORIGEN", bg=self.colores["bg_panel"], fg=self.colores["texto_sec"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.entry_origen = tk.Entry(form_frame, width=10, font=("Segoe UI", 14, "bold"), bg=self.colores["bg_input"], fg=self.colores["texto_primario"], insertbackground=self.colores["texto_primario"], justify="center", bd=0)
        self.entry_origen.grid(row=1, column=0, padx=(0, 20), ipady=8)
        
        tk.Label(form_frame, text="DESTINO", bg=self.colores["bg_panel"], fg=self.colores["texto_sec"], font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w", pady=(0, 5))
        self.entry_destino = tk.Entry(form_frame, width=10, font=("Segoe UI", 14, "bold"), bg=self.colores["bg_input"], fg=self.colores["texto_primario"], insertbackground=self.colores["texto_primario"], justify="center", bd=0)
        self.entry_destino.grid(row=1, column=1, ipady=8)

        frame_btns = tk.Frame(self.frame_controles, bg=self.colores["bg_panel"])
        frame_btns.pack(fill=tk.X, padx=30, pady=5)
        
        ttk.Button(frame_btns, text="Ejecutar Dijkstra", style='Primary.TButton', command=self.pedir_datos_ruta).pack(fill=tk.X, pady=(0, 10))
        ttk.Button(frame_btns, text="Limpiar Entorno", style='Danger.TButton', command=self.limpiar_red).pack(fill=tk.X)
        
        terminal_container = tk.Frame(self.frame_controles, bg=self.colores["terminal_bg"], bd=1, relief="solid")
        terminal_container.pack(padx=30, pady=(20, 30), fill=tk.BOTH, expand=True)
        
        term_header = tk.Frame(terminal_container, bg="#1E1E1E", height=25)
        term_header.pack(fill=tk.X)
        term_header.pack_propagate(False)
        tk.Label(term_header, text="bash ~ estado", font=("Consolas", 8), bg="#1E1E1E", fg="#858585").pack(side=tk.LEFT, padx=10)
        
        self.texto_informe = tk.Text(terminal_container, font=("Consolas", 10), state=tk.DISABLED, bg=self.colores["terminal_bg"], fg=self.colores["terminal_fg"], bd=0, padx=15, pady=15, insertbackground=self.colores["terminal_fg"])
        self.texto_informe.pack(fill=tk.BOTH, expand=True)

    def set_modo(self, modo):
        self.modo_actual = modo
        self.nodo_origen_enlace = None
        for key, btn in self.botones_modo.items():
            if key == modo:
                btn.configure(bg=self.colores["nodo_base"], fg="#FFFFFF")
            else:
                btn.configure(bg=self.colores["bg_input"], fg=self.colores["texto_sec"])
        self.dibujar_red()

    def obtener_siguiente_letra(self):
        existentes = set(self.nodos.keys())
        i = 0
        while True:
            letra = chr(65 + i)
            if letra not in existentes:
                return letra
            i += 1

    def solicitar_peso(self, u, v, peso_actual=None):
        ventana_peso = tk.Toplevel(self.root)
        ventana_peso.title("Métrica de Enlace")
        
        width, height = 280, 140
        self.root.update_idletasks() 
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (height // 2)
        
        ventana_peso.geometry(f"{width}x{height}+{x}+{y}")
        ventana_peso.configure(bg=self.colores["bg_panel"])
        
        ventana_peso.transient(self.root)
        ventana_peso.attributes('-topmost', True) 
        ventana_peso.grab_set()
        
        tk.Frame(ventana_peso, bg=self.colores["ruta_principal"], height=4).pack(fill=tk.X)
        
        titulo = "Editar Peso" if peso_actual else "Nueva Métrica"
        tk.Label(ventana_peso, text=f"{titulo}: {u} ⟷ {v}", bg=self.colores["bg_panel"], fg=self.colores["texto_primario"], font=("Segoe UI", 12, "bold")).pack(pady=(15, 10))
        
        entry_peso = tk.Entry(ventana_peso, justify="center", font=("Consolas", 14, "bold"), bd=0, bg=self.colores["bg_input"], fg=self.colores["texto_primario"])
        if peso_actual:
            entry_peso.insert(0, str(peso_actual))
        entry_peso.pack(ipady=6, ipadx=10)
        entry_peso.focus_force() 
        
        def guardar_peso(event=None):
            try:
                peso = int(entry_peso.get())
                if peso > 0:
                    self.red[u][v] = peso
                    self.red[v][u] = peso
                    self.rutas_optimas = []
                    ventana_peso.grab_release() 
                    ventana_peso.destroy()      
                    self.dibujar_red()
                    if peso_actual:
                        self.actualizar_informe(f"Métrica actualizada: {u}-{v} = {peso}ms")
                else:
                    messagebox.showwarning("Error", "El valor debe ser positivo.", parent=ventana_peso)
            except ValueError:
                messagebox.showwarning("Error", "Ingrese un número válido.", parent=ventana_peso)

        ventana_peso.bind('<Return>', guardar_peso)
        ventana_peso.bind('<Escape>', lambda e: ventana_peso.destroy())

    def on_press_izq(self, event):
        nodo = self.detectar_nodo(event.x, event.y)
        if self.modo_actual == "SELECCION":
            if nodo:
                self.nodo_arrastrado = nodo
        elif self.modo_actual == "NODO":
            if not nodo:
                nombre = self.obtener_siguiente_letra()
                self.nodos[nombre] = (event.x, event.y)
                self.red[nombre] = {}
                self.dibujar_red()
        elif self.modo_actual == "ENLACE":
            if nodo:
                if self.nodo_origen_enlace is None:
                    self.nodo_origen_enlace = nodo
                else:
                    if self.nodo_origen_enlace != nodo:
                        u, v = self.nodo_origen_enlace, nodo
                        self.nodo_origen_enlace = None
                        self.solicitar_peso(u, v)
                    else:
                        self.nodo_origen_enlace = None
                self.dibujar_red()
        elif self.modo_actual == "BORRAR":
            self.ejecutar_borrado(event.x, event.y)

    def on_drag(self, event):
        if self.modo_actual == "SELECCION" and self.nodo_arrastrado:
            self.nodos[self.nodo_arrastrado] = (event.x, event.y)
            self.dibujar_red()

    def on_release_izq(self, event):
        if self.modo_actual == "SELECCION":
            self.nodo_arrastrado = None

    def on_double_click(self, event):
        if self.modo_actual == "SELECCION":
            enlace = self.detectar_enlace(event.x, event.y)
            if enlace:
                u, v = enlace
                self.solicitar_peso(u, v, self.red[u][v])

    def ejecutar_borrado(self, x, y):
        nodo_a_borrar = self.detectar_nodo(x, y)
        if nodo_a_borrar:
            del self.nodos[nodo_a_borrar]
            self.red.pop(nodo_a_borrar)
            for conex in self.red.values():
                if nodo_a_borrar in conex:
                    del conex[nodo_a_borrar]
            if self.nodo_origen_enlace == nodo_a_borrar:
                self.nodo_origen_enlace = None
            self.rutas_optimas = []
            self.actualizar_informe(f"rm -rf router_{nodo_a_borrar}")
            self.dibujar_red()
            return

        enlace_a_borrar = self.detectar_enlace(x, y)
        if enlace_a_borrar:
            u, v = enlace_a_borrar
            del self.red[u][v]
            del self.red[v][u]
            self.rutas_optimas = []
            self.actualizar_informe(f"rm enlace_{u}_{v}")
            self.dibujar_red()

    def detectar_nodo(self, x, y):
        for nombre, (nx, ny) in self.nodos.items():
            if math.hypot(nx - x, ny - y) <= 24:
                return nombre
        return None

    def detectar_enlace(self, x, y):
        for u, vecinos in self.red.items():
            for v in vecinos:
                x1, y1 = self.nodos[u]
                x2, y2 = self.nodos[v]
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                if math.hypot(mx - x, my - y) <= 18:
                    return (u, v)
        return None

    def dibujar_red(self):
        self.canvas.delete("all")
        dibujados = set()
        for u, vecinos in self.red.items():
            for v, peso in vecinos.items():
                enlace = tuple(sorted([u, v]))
                if enlace not in dibujados:
                    x1, y1 = self.nodos[u]
                    x2, y2 = self.nodos[v]
                    color = self.colores["enlace_base"]
                    grosor = 2
                    if self.rutas_optimas:
                        if self.enlace_en_ruta(u, v, self.rutas_optimas[0]):
                            color, grosor = self.colores["ruta_principal"], 5
                        else:
                            for ruta_alt in self.rutas_optimas[1:]:
                                if self.enlace_en_ruta(u, v, ruta_alt):
                                    color, grosor = self.colores["ruta_alt"], 3
                                    break
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor)
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    self.canvas.create_oval(mx-15, my-15, mx+15, my+15, fill=self.colores["bg_canvas"], outline="")
                    self.canvas.create_text(mx, my, text=str(peso), fill=self.colores["texto_primario"], font=("Consolas", 11, "bold"))
                    dibujados.add(enlace)
        
        for nombre, (x, y) in self.nodos.items():
            color_fondo = self.colores["nodo_base"]
            if nombre == self.nodo_origen_enlace: 
                color_fondo = self.colores["nodo_sel"]
            en_ruta = any(nombre in r for r in self.rutas_optimas) if self.rutas_optimas else False
            if en_ruta:
                color_fondo = self.colores["ruta_principal"] if nombre in self.rutas_optimas[0] else self.colores["ruta_alt"]
            self.canvas.create_oval(x-24, y-24, x+24, y+24, fill=self.colores["bg_canvas"], outline=color_fondo, width=3)
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=color_fondo, outline="")
            self.canvas.create_text(x, y, text=nombre, fill="#FFFFFF", font=("Segoe UI", 12, "bold"))

    def enlace_en_ruta(self, u, v, ruta):
        for i in range(len(ruta) - 1):
            if (ruta[i] == u and ruta[i+1] == v) or (ruta[i] == v and ruta[i+1] == u):
                return True
        return False

    def limpiar_red(self):
        self.nodos, self.red, self.rutas_optimas = {}, {}, []
        self.nodo_origen_enlace = None
        self.entry_origen.delete(0, tk.END)
        self.entry_destino.delete(0, tk.END)
        self.actualizar_informe("Reiniciando servicios de red... OK")
        self.dibujar_red()

    def pedir_datos_ruta(self):
        inicio = self.entry_origen.get().strip().upper()
        destino = self.entry_destino.get().strip().upper()
        
        if len(self.nodos) < 2:
            messagebox.showwarning("Datos Faltantes", "Debe existir al menos una topología básica de 2 routers para calcular una ruta.")
            self.actualizar_informe("ERR_TOPOLOGÍA: Nodos insuficientes")
            return
            
        if not inicio or not destino:
            messagebox.showwarning("Datos Faltantes", "Debe ingresar el router de origen y de destino en los campos para ejecutar el algoritmo.")
            self.actualizar_informe("ERR_ENTRADA: Valores nulos proporcionados")
            return
            
        self.calcular_dijkstra_ecmp(inicio, destino)

    def calcular_dijkstra_ecmp(self, inicio, destino):
        if inicio not in self.nodos or destino not in self.nodos:
            messagebox.showerror("Error de Topología", f"El nodo '{inicio}' o el nodo '{destino}' no existen en la red actual.")
            self.actualizar_informe("ERR_NODO_NO_ENCONTRADO")
            return
            
        distancias = {nodo: float('inf') for nodo in self.red}
        distancias[inicio] = 0
        cola = [(0, inicio)]
        predecesores = {nodo: [] for nodo in self.red}
        
        while cola:
            dist_actual, u = heapq.heappop(cola)
            if dist_actual > distancias[u]: continue
            for v, peso in self.red[u].items():
                dist_nueva = dist_actual + peso
                if dist_nueva < distancias[v]:
                    distancias[v], predecesores[v] = dist_nueva, [u]
                    heapq.heappush(cola, (dist_nueva, v))
                elif dist_nueva == distancias[v]:
                    predecesores[v].append(u)
                    
        if distancias[destino] == float('inf'):
            messagebox.showwarning("Ruta Inalcanzable", f"No existe ninguna conexión física posible entre {inicio} y {destino}.")
            self.actualizar_informe("ERR_HOST_INALCANZABLE")
            self.rutas_optimas = []
        else:
            self.rutas_optimas = []
            def reconstruir(nodo, ruta):
                if nodo == inicio: self.rutas_optimas.append([inicio] + ruta[::-1]); return
                for p in predecesores[nodo]: reconstruir(p, ruta + [nodo])
            reconstruir(destino, [])
            self.generar_informe_claro(inicio, destino, distancias[destino])
            
        self.dibujar_red()

    def generar_informe_claro(self, inicio, destino, costo):
        informe = f"root@routing:~$ ./dijkstra {inicio} {destino}\n\n"
        informe += f"Trazando ruta hacia {destino}:\n"
        informe += f"Latencia total : {costo}ms\n\n"
        informe += f"[Ruta Principal]\n{' -> '.join(self.rutas_optimas[0])}\n"
        if len(self.rutas_optimas) > 1:
            informe += f"\n[Rutas ECMP Alternativas]\n"
            for i, r in enumerate(self.rutas_optimas[1:], 1):
                informe += f"{i}. {' -> '.join(r)}\n"
        informe += f"\nProceso finalizado con código de salida 0"
        self.actualizar_informe(informe)

    def actualizar_informe(self, texto):
        self.texto_informe.config(state=tk.NORMAL)
        self.texto_informe.delete(1.0, tk.END)
        self.texto_informe.insert(tk.END, f"{texto}\nroot@routing:~$ ")
        self.texto_informe.see(tk.END)
        self.texto_informe.config(state=tk.DISABLED)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = SimuladorDijkstra(ventana)
    app.actualizar_informe("Inicializando motor de enrutamiento... OK")
    ventana.mainloop()