class Estudiante:
    def __init__(self, codigo, nombre, nota):
        self.codigo = codigo
        self.nombre = nombre
        self.nota = nota

    def estado(self):
        return "Aprobado" if self.nota >= 3.0 else "Reprobado"

    def mostrar_info(self):
        return f"Codigo: {self.codigo}, Nombre: {self.nombre}, Nota: {self.nota}, Estado: {self.estado()}"


class SistemaEstudiantes:
    def __init__(self):
        self.estudiantes = []

    def registrar_estudiante(self):
        codigo = input("Codigo del estudiante: ").strip()
        if any(est.codigo == codigo for est in self.estudiantes):
            print("El codigo ya existe")
            return

        nombre = input("Nombre del estudiante: ").strip()
        while True:
            try:
                nota = float(input("Nota del estudiante (0-5): "))
            except ValueError:
                print("Nota invalida. Ingresa un número entre 0 y 5.")
                continue
            if 0 <= nota <= 5:
                break
            print("Nota invalida. Por favor ingrese una nota entre 0 y 5.")

        nuevo_estudiante = Estudiante(codigo, nombre, nota)
        self.estudiantes.append(nuevo_estudiante)
        print("Estudiante registrado exitosamente.")

    def mostrar_estudiantes(self):
        if len(self.estudiantes) == 0:
            print("No hay estudiantes registrados.")
            return
        for est in self.estudiantes:
            print(est.mostrar_info())

    def buscar_estudiante(self):
        codigo_buscar = input("Ingrese el codigo del estudiante a buscar: ").strip()
        for est in self.estudiantes:
            if est.codigo == codigo_buscar:
                print("Estudiante encontrado:")
                print(est.mostrar_info())
                return
        print("No se encontró un estudiante con el codigo proporcionado.")

    def eliminar_estudiante(self):
        codigo_eliminar = input("Ingrese el codigo del estudiante a eliminar: ").strip()
        for est in self.estudiantes:
            if est.codigo == codigo_eliminar:
                self.estudiantes.remove(est)
                print("Estudiante eliminado exitosamente.")
                return
        print("No se encontró un estudiante con el codigo proporcionado.")

    def actualizar_nota(self):
        codigo_buscar = input("Ingrese el codigo del estudiante para actualizar la nota: ").strip()
        for est in self.estudiantes:
            if est.codigo == codigo_buscar:
                print("Estudiante encontrado:")
                print(est.mostrar_info())
                while True:
                    try:
                        nueva_nota = float(input("Ingrese la nueva nota (0-5): "))
                    except ValueError:
                        print("Nota invalida. Ingresa un número entre 0 y 5.")
                        continue
                    if 0 <= nueva_nota <= 5:
                        break
                    print("Nota invalida. Por favor ingrese una nota entre 0 y 5.")

                est.nota = nueva_nota
                print("Nota actualizada exitosamente.")
                print(f"Nueva información: {est.mostrar_info()}")
                return
        print("No se encontró un estudiante con el codigo proporcionado.")

    def calcular_promedio(self):
        if len(self.estudiantes) == 0:
            print("No hay estudiantes registrados para calcular el promedio.")
            return
        suma = sum(est.nota for est in self.estudiantes)
        promedio = suma / len(self.estudiantes)
        print(f"El promedio de las notas de los estudiantes es: {promedio:.2f}")

    
    def guardar_archivo(self):
        if len(self.estudiantes) == 0:
            print("No hay estudiantes para guardar.")
            return
        try:
            with open("estudiantes.txt", "w", encoding="utf-8") as archivo:
                for est in self.estudiantes:
                    archivo.write(f"{est.codigo},{est.nombre},{est.nota}\n")
            print("Datos guardados en estudiantes.txt")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def estadisticas(self):

        aprobados = 0 
        reprobados = 0

        for est in self.estudiantes:
            if est.nota >= 3:
                aprobados += 1
            else:
                reprobados += 1

                print("\n--- Estadísticas ---")
                print("Aprobados:", aprobados)

    def menu(self):
        while True:
            print("\n--- Sistema de Estudiantes ---")
            print("1. Registrar estudiante")
            print("2. Mostrar estudiantes")
            print("3. Buscar estudiante")
            print("4. Eliminar estudiante")
            print("5. Actualizar nota")
            print("6. Calcular promedio")
            print("7. Guardar estudiantes en archivo")
            print("8. Salir")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                self.registrar_estudiante()
            elif opcion == "2":
                self.mostrar_estudiantes()
            elif opcion == "3":
                self.buscar_estudiante()
            elif opcion == "4":
                self.eliminar_estudiante()
            elif opcion == "5":
                self.actualizar_nota()
            elif opcion == "6":
                self.calcular_promedio()
            elif opcion == "7":
                self.guardar_archivo()
            elif opcion == "8":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Por favor seleccione una opción válida.")


if __name__ == "__main__":
    SistemaEstudiantes().menu()