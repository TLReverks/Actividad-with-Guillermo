class Producto:
    def __init__(self, codigo, nombre, precio, cantidad, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria

    def valor_total(self):
        return self.precio * self.cantidad

    def mostrar_info(self):
        return f"Código: {self.codigo}, Nombre: {self.nombre}, Precio: ${self.precio:.2f}, Cantidad: {self.cantidad}, Categoría: {self.categoria}"


class SistemaInventario:
    def __init__(self):
        self.productos = []

    def registrar_producto(self):
        codigo = input("Ingrese el código del producto: ").strip()
        if not codigo:
            print("El código no puede estar vacío.")
            return

        if any(prod.codigo == codigo for prod in self.productos):
            print("El código ya existe. Por favor ingrese otro código.")
            return

        nombre = input("Ingrese el nombre del producto: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            return

        while True:
            try:
                precio = float(input("Ingrese el precio del producto: "))
                if precio < 0:
                    print("El precio no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("Ingrese un valor numérico válido para el precio.")

        while True:
            try:
                cantidad = int(input("Ingrese la cantidad disponible: "))
                if cantidad < 0:
                    print("La cantidad no puede ser negativa.")
                    continue
                break
            except ValueError:
                print("Ingrese un valor numérico válido para la cantidad.")

        categoria = input("Ingrese la categoría del producto: ").strip()
        if not categoria:
            print("La categoría no puede estar vacía.")
            return

        nuevo_producto = Producto(codigo, nombre, precio, cantidad, categoria)
        self.productos.append(nuevo_producto)
        print("Producto registrado exitosamente.\n")

    def mostrar_productos(self):
        if len(self.productos) == 0:
            print("No hay productos registrados.\n")
            return
        print("\n--- PRODUCTOS REGISTRADOS ---")
        for prod in self.productos:
            print(prod.mostrar_info())
        print()

    def buscar_producto(self):
        print("\nBuscar por:")
        print("1. Código")
        print("2. Nombre")
        opcion = input("Seleccione la opción: ").strip()

        if opcion == "1":
            codigo_buscar = input("Ingrese el código del producto: ").strip()
            for prod in self.productos:
                if prod.codigo == codigo_buscar:
                    print("Producto encontrado:")
                    print(prod.mostrar_info())
                    print()
                    return
            print("No se encontró un producto con ese código.\n")
        elif opcion == "2":
            nombre_buscar = input("Ingrese el nombre del producto: ").strip()
            encontrados = [prod for prod in self.productos if nombre_buscar.lower() in prod.nombre.lower()]
            if encontrados:
                print("Productos encontrados:")
                for prod in encontrados:
                    print(prod.mostrar_info())
                print()
            else:
                print("No se encontraron productos con ese nombre.\n")
        else:
            print("Opción inválida.\n")

    def actualizar_producto(self):
        codigo_buscar = input("Ingrese el código del producto a actualizar: ").strip()
        for prod in self.productos:
            if prod.codigo == codigo_buscar:
                print("Producto encontrado:")
                print(prod.mostrar_info())
                
                print("\nQué desea actualizar?")
                print("1. Precio")
                print("2. Cantidad")
                print("3. Categoría")
                opcion = input("Seleccione la opción: ").strip()

                if opcion == "1":
                    while True:
                        try:
                            nuevo_precio = float(input("Ingrese el nuevo precio: "))
                            if nuevo_precio < 0:
                                print("El precio no puede ser negativo.")
                                continue
                            prod.precio = nuevo_precio
                            print("Precio actualizado exitosamente.")
                            break
                        except ValueError:
                            print("Ingrese un valor numérico válido.")
                elif opcion == "2":
                    while True:
                        try:
                            nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                            if nueva_cantidad < 0:
                                print("La cantidad no puede ser negativa.")
                                continue
                            prod.cantidad = nueva_cantidad
                            print("Cantidad actualizada exitosamente.")
                            break
                        except ValueError:
                            print("Ingrese un valor numérico válido.")
                elif opcion == "3":
                    nueva_categoria = input("Ingrese la nueva categoría: ").strip()
                    if not nueva_categoria:
                        print("La categoría no puede estar vacía.")
                        return
                    prod.categoria = nueva_categoria
                    print("Categoría actualizada exitosamente.")
                else:
                    print("Opción inválida.")
                    return

                print(f"Nueva información: {prod.mostrar_info()}\n")
                return

        print("No se encontró un producto con ese código.\n")

    def eliminar_producto(self):
        codigo_eliminar = input("Ingrese el código del producto a eliminar: ").strip()
        for prod in self.productos:
            if prod.codigo == codigo_eliminar:
                self.productos.remove(prod)
                print("Producto eliminado exitosamente.\n")
                return
        print("No se encontró un producto con ese código.\n")

    def calcular_total_inventario(self):
        if len(self.productos) == 0:
            print("No hay productos registrados.\n")
            return
        
        total = sum(prod.valor_total() for prod in self.productos)
        print("\n--- VALOR TOTAL DEL INVENTARIO ---")
        for prod in self.productos:
            print(f"{prod.nombre}: {prod.cantidad} x ${prod.precio:.2f} = ${prod.valor_total():.2f}")
        print(f"\nValor total del inventario: ${total:.2f}\n")

    def mostrar_agotados(self):
        agotados = [prod for prod in self.productos if prod.cantidad == 0]
        
        if len(agotados) == 0:
            print("No hay productos agotados.\n")
            return
        
        print("\n--- PRODUCTOS AGOTADOS ---")
        for prod in agotados:
            print(prod.mostrar_info())
        print()

    def guardar_archivo(self):
        if len(self.productos) == 0:
            print("No hay productos para guardar.\n")
            return

        try:
            with open("inventario.txt", "w", encoding="utf-8") as archivo:
                archivo.write("=" * 80 + "\n")
                archivo.write("INVENTARIO DE PRODUCTOS\n")
                archivo.write("=" * 80 + "\n\n")
                
                for prod in self.productos:
                    archivo.write(f"Código: {prod.codigo}\n")
                    archivo.write(f"Nombre: {prod.nombre}\n")
                    archivo.write(f"Precio: ${prod.precio:.2f}\n")
                    archivo.write(f"Cantidad: {prod.cantidad}\n")
                    archivo.write(f"Categoría: {prod.categoria}\n")
                    archivo.write(f"Valor Total: ${prod.valor_total():.2f}\n")
                    archivo.write("-" * 80 + "\n\n")
                
                total_inventario = sum(prod.valor_total() for prod in self.productos)
                archivo.write("=" * 80 + "\n")
                archivo.write(f"VALOR TOTAL DEL INVENTARIO: ${total_inventario:.2f}\n")
                archivo.write("=" * 80 + "\n")
            
            print("Inventario guardado exitosamente en 'inventario.txt'.\n")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}\n")

    def menu(self):
        while True:
            print("\n--- SISTEMA DE INVENTARIO ---")
            print("1. Registrar producto")
            print("2. Mostrar todos los productos")
            print("3. Buscar producto")
            print("4. Actualizar producto")
            print("5. Eliminar producto")
            print("6. Calcular valor total del inventario")
            print("7. Mostrar productos agotados")
            print("8. Guardar inventario en archivo")
            print("9. Salir")
            print("-" * 40)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.registrar_producto()
            elif opcion == "2":
                self.mostrar_productos()
            elif opcion == "3":
                self.buscar_producto()
            elif opcion == "4":
                self.actualizar_producto()
            elif opcion == "5":
                self.eliminar_producto()
            elif opcion == "6":
                self.calcular_total_inventario()
            elif opcion == "7":
                self.mostrar_agotados()
            elif opcion == "8":
                self.guardar_archivo()
            elif opcion == "9":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Por favor seleccione una opción válida.\n")


if __name__ == "__main__":
    SistemaInventario().menu()