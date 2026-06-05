import re
from datetime import datetime


ROLES_VALIDOS = ["Administrador", "Aprendiz", "Instructor"]


class Usuario:
    def __init__(self, documento, nombre, correo, rol, estado="Activo"):
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.rol = rol
        self.estado = estado

    def mostrar_info(self):
        return (
            f"Documento: {self.documento} | Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Rol: {self.rol} | Estado: {self.estado}"
        )


class SistemaUsuarios:
    def __init__(self):
        self.usuarios = []

    # ─── Validaciones internas ───────────────────────────────────────────────

    def _correo_valido(self, correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(patron, correo) is not None

    def _documento_existe(self, documento):
        return any(u.documento == documento for u in self.usuarios)

    def _correo_existe(self, correo, excluir_documento=None):
        for u in self.usuarios:
            if u.correo.lower() == correo.lower():
                if excluir_documento is None or u.documento != excluir_documento:
                    return True
        return False

    def _mostrar_roles(self):
        print("Roles disponibles:")
        for i, rol in enumerate(ROLES_VALIDOS, 1):
            print(f"  {i}. {rol}")

    # ─── 1. Registrar usuario ────────────────────────────────────────────────

    def registrar_usuario(self):
        print("\n--- REGISTRAR USUARIO ---")

        documento = input("Documento: ").strip()
        if not documento:
            print("El documento no puede estar vacío.\n")
            return
        if self._documento_existe(documento):
            print("Ya existe un usuario con ese documento.\n")
            return

        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.\n")
            return

        correo = input("Correo electrónico: ").strip()
        if not correo:
            print("El correo no puede estar vacío.\n")
            return
        if not self._correo_valido(correo):
            print("El correo no tiene un formato válido.\n")
            return
        if self._correo_existe(correo):
            print("Ya existe un usuario con ese correo.\n")
            return

        self._mostrar_roles()
        opcion_rol = input("Seleccione el número del rol: ").strip()
        if opcion_rol not in ["1", "2", "3"]:
            print("Rol inválido.\n")
            return
        rol = ROLES_VALIDOS[int(opcion_rol) - 1]

        nuevo_usuario = Usuario(documento, nombre, correo, rol)
        self.usuarios.append(nuevo_usuario)
        print(f"Usuario '{nombre}' registrado exitosamente.\n")

    # ─── 2. Mostrar usuarios ─────────────────────────────────────────────────

    def mostrar_usuarios(self):
        if not self.usuarios:
            print("\nNo hay usuarios registrados.\n")
            return
        print(f"\n--- USUARIOS REGISTRADOS ({len(self.usuarios)}) ---")
        for u in self.usuarios:
            print(u.mostrar_info())
        print()

    # ─── 3. Buscar usuario ───────────────────────────────────────────────────

    def buscar_usuario(self):
        print("\nBuscar por:")
        print("1. Documento")
        print("2. Correo")
        opcion = input("Seleccione la opción: ").strip()

        if opcion == "1":
            doc = input("Ingrese el documento: ").strip()
            for u in self.usuarios:
                if u.documento == doc:
                    print("\nUsuario encontrado:")
                    print(u.mostrar_info())
                    print()
                    return
            print("No se encontró un usuario con ese documento.\n")

        elif opcion == "2":
            correo = input("Ingrese el correo: ").strip()
            for u in self.usuarios:
                if u.correo.lower() == correo.lower():
                    print("\nUsuario encontrado:")
                    print(u.mostrar_info())
                    print()
                    return
            print("No se encontró un usuario con ese correo.\n")

        else:
            print("Opción inválida.\n")

    # ─── 4. Actualizar usuario ───────────────────────────────────────────────

    def actualizar_usuario(self):
        print("\n--- ACTUALIZAR USUARIO ---")
        doc = input("Ingrese el documento del usuario a actualizar: ").strip()

        for u in self.usuarios:
            if u.documento == doc:
                print("\nUsuario encontrado:")
                print(u.mostrar_info())
                print("\n¿Qué desea modificar?")
                print("1. Nombre")
                print("2. Correo")
                print("3. Rol")
                print("4. Estado")
                opcion = input("Seleccione la opción: ").strip()

                if opcion == "1":
                    nuevo_nombre = input("Nuevo nombre: ").strip()
                    if not nuevo_nombre:
                        print("El nombre no puede estar vacío.\n")
                        return
                    u.nombre = nuevo_nombre
                    print("Nombre actualizado correctamente.\n")

                elif opcion == "2":
                    nuevo_correo = input("Nuevo correo: ").strip()
                    if not nuevo_correo:
                        print("El correo no puede estar vacío.\n")
                        return
                    if not self._correo_valido(nuevo_correo):
                        print("El correo no tiene un formato válido.\n")
                        return
                    if self._correo_existe(nuevo_correo, excluir_documento=doc):
                        print("Ese correo ya está en uso por otro usuario.\n")
                        return
                    u.correo = nuevo_correo
                    print("Correo actualizado correctamente.\n")

                elif opcion == "3":
                    self._mostrar_roles()
                    opcion_rol = input("Seleccione el número del nuevo rol: ").strip()
                    if opcion_rol not in ["1", "2", "3"]:
                        print("Rol inválido.\n")
                        return
                    u.rol = ROLES_VALIDOS[int(opcion_rol) - 1]
                    print("Rol actualizado correctamente.\n")

                elif opcion == "4":
                    print("Estados disponibles: 1. Activo  2. Inactivo")
                    opcion_estado = input("Seleccione el estado: ").strip()
                    if opcion_estado == "1":
                        u.estado = "Activo"
                    elif opcion_estado == "2":
                        u.estado = "Inactivo"
                    else:
                        print("Opción inválida.\n")
                        return
                    print("Estado actualizado correctamente.\n")

                else:
                    print("Opción inválida.\n")
                    return

                print(f"Información actualizada: {u.mostrar_info()}\n")
                return

        print("No se encontró un usuario con ese documento.\n")

    # ─── 5. Eliminar usuario ─────────────────────────────────────────────────

    def eliminar_usuario(self):
        print("\n--- ELIMINAR USUARIO ---")
        doc = input("Ingrese el documento del usuario a eliminar: ").strip()

        for u in self.usuarios:
            if u.documento == doc:
                print(f"\nUsuario encontrado: {u.mostrar_info()}")
                confirmacion = input("¿Está seguro que desea eliminarlo? (s/n): ").strip().lower()
                if confirmacion == "s":
                    self.usuarios.remove(u)
                    print("Usuario eliminado exitosamente.\n")
                else:
                    print("Eliminación cancelada.\n")
                return

        print("No se encontró un usuario con ese documento.\n")

    # ─── 6. Mostrar usuarios activos ─────────────────────────────────────────

    def mostrar_activos(self):
        activos = [u for u in self.usuarios if u.estado == "Activo"]
        if not activos:
            print("\nNo hay usuarios activos registrados.\n")
            return
        print(f"\n--- USUARIOS ACTIVOS ({len(activos)}) ---")
        for u in activos:
            print(u.mostrar_info())
        print()

    # ─── 7. Contar usuarios por rol ──────────────────────────────────────────

    def contar_roles(self):
        if not self.usuarios:
            print("\nNo hay usuarios registrados.\n")
            return
        print("\n--- CONTEO POR ROL ---")
        for rol in ROLES_VALIDOS:
            cantidad = sum(1 for u in self.usuarios if u.rol == rol)
            print(f"  {rol}s: {cantidad}")
        print(f"  Total de usuarios: {len(self.usuarios)}\n")

    # ─── 8. Exportar a archivo .txt ──────────────────────────────────────────

    def guardar_archivo(self):
        if not self.usuarios:
            print("\nNo hay usuarios para guardar.\n")
            return

        nombre_archivo = "usuarios.txt"
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("=" * 80 + "\n")
                archivo.write("SISTEMA DE GESTIÓN DE USUARIOS\n")
                archivo.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                archivo.write("=" * 80 + "\n\n")

                for u in self.usuarios:
                    archivo.write(f"Documento      : {u.documento}\n")
                    archivo.write(f"Nombre         : {u.nombre}\n")
                    archivo.write(f"Correo         : {u.correo}\n")
                    archivo.write(f"Rol            : {u.rol}\n")
                    archivo.write(f"Estado         : {u.estado}\n")
                    archivo.write("-" * 80 + "\n\n")

                archivo.write("=" * 80 + "\n")
                archivo.write(f"Total de usuarios registrados: {len(self.usuarios)}\n")
                for rol in ROLES_VALIDOS:
                    cantidad = sum(1 for u in self.usuarios if u.rol == rol)
                    archivo.write(f"  {rol}s: {cantidad}\n")
                archivo.write("=" * 80 + "\n")

            print(f"Usuarios exportados correctamente en '{nombre_archivo}'.\n")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}\n")

    # ─── Menú principal ──────────────────────────────────────────────────────

    def menu(self):
        while True:
            print("\n--- SISTEMA DE USUARIOS ---")
            print("1. Registrar usuario")
            print("2. Mostrar todos los usuarios")
            print("3. Buscar usuario")
            print("4. Actualizar usuario")
            print("5. Eliminar usuario")
            print("6. Mostrar usuarios activos")
            print("7. Contar usuarios por rol")
            print("8. Exportar usuarios a archivo .txt")
            print("9. Salir")
            print("-" * 40)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.mostrar_usuarios()
            elif opcion == "3":
                self.buscar_usuario()
            elif opcion == "4":
                self.actualizar_usuario()
            elif opcion == "5":
                self.eliminar_usuario()
            elif opcion == "6":
                self.mostrar_activos()
            elif opcion == "7":
                self.contar_roles()
            elif opcion == "8":
                self.guardar_archivo()
            elif opcion == "9":
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor seleccione una opción del 1 al 9.\n")


if __name__ == "__main__":
    SistemaUsuarios().menu()