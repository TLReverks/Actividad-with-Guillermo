class Estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota

    def mostrar_informacion(self):
        estado = "Aprobado" if self.nota >= 3 else "Reprobado"
        return f"Nombre: {self.nombre}, Nota: {self.nota}, Estado: {estado}"


def main():
    estudiantes = []
    for i in range(3):
        print(f"\nRegistro del estudiante {i + 1}:")
        nombre = input("Nombre del estudiante: ").strip()
        while True:
            try:
                nota = float(input("Nota del estudiante: "))
                break
            except ValueError:
                print("Por favor ingresa una nota válida.")

        estudiantes.append(Estudiante(nombre, nota))

    print("\nInformación de los estudiantes registrados:")
    for estudiante in estudiantes:
        print(estudiante.mostrar_informacion())


if __name__ == "__main__":
    main()
