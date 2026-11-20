locals {
  fichas = {
    portal = {
      nombre  = var.nombre_aplicacion
      entorno = var.entorno
    }
    ayuda = {
      nombre  = "portal-ayuda"
      entorno = var.entorno
    }
  }
}

module "fichas" {
  for_each = local.fichas
  source   = "./modulo_ficha"
  nombre   = each.value.nombre
  entorno  = each.value.entorno
}
