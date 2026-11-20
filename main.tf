locals {
  catalogo = {
    portal = var.nombre_aplicacion
    ayuda  = "portal-ayuda"
  }
}

module "fichas" {
  for_each = local.catalogo
  source   = "./modulo_ficha"
  nombre   = each.value
  proyecto = "nexo-portal"
  entorno  = var.entorno
  equipo   = var.equipo_responsable
}
