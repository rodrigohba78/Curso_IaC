resource "terraform_data" "ficha" {
  input = {
    nombre   = var.nombre
    proyecto = var.proyecto
    entorno  = var.entorno
    equipo   = var.equipo
  }
}
