![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg)  [![Paypal.me][paypalbedge]][paypalme] [![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

# CRTM - Home Assistant

Integration de Home Assistant para obtener información en tiempo real de los autobuses interurbanos de la Comunidad de Madrid.

## Instalación

### Instalación via HACS

Esta integración puede instalarse a través de HACS.

Puedes añadirla pulsando este botón:

[![image](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=joeltoumi&repository=sensor_crtm&category=integration)

Si el botón no funciona, añade `https://github.com/joeltoumi/sensor_crtm` como repositorio personalizado de tipo integración en HACS.

- Click en instalar en la integración `CRTM`.
- Reinicia Home Assistant.

### Instalación manual

- Copia la carpeta `crtm` de la [última release](https://github.com/joeltoumi/sensor_crtm/releases/latest) a tu `<directorio de configuración>/custom_components/`.
- Reinicia Home Assistant.

## Configuración

Añadir CRTM a tu instalación de Home Assistant puede hacerse vía UI usando este botón:

[![image](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=crtm_bus_stop_integration)

### Configuración manual

Si el botón superior no funciona, también puedes añadirlo siguiendo estos pasos:

- Navega a tu instancia de Home Assistant.
- En la barra lateral, click en Ajustes.
- En el menú de configuración, selecciona: Dispositivos y Servicios.
- En la esquina inferior derecha, click en Añadir integración.
- En la lista, busca y selecciona `CRTM Integration`.
- Sigue las instrucciones de la pantalla para completar la configuración.

## Debugging

Para habilitar el debug para la integración de CRTM, añade lo siguiente a tu `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.crtm: debug
```

## Crea una tarjeta

Esta integración requiere instalar [crtm-mobility-card](https://github.com/joeltoumi/crtm-mobility-card)

```yaml
type: custom:crtm-mobility-card
entity: sensor.crtm_stop_XXXX
stop_name: Nombre personalizado
```
| Parámetros  | Type     | Descripción                                                                                                                |
|:------------| :------- |:---------------------------------------------------------------------------------------------------------------------------|
| `type`      | `string` | **Requerido**. Tipo de la tarjeta                                                                                          |
| `entity`    | `string` | **Requerido**. Entidad de la integración CRTM                                                                              |
| `stop_name` | `string` | **Opcional**. Nombre personalizado de la parada de bus. <br/>Si no se indica se mostrará el número de parada en el nombre. |


Después de la instalación, la tarjeta debería verse de la siguiente manera:

![image](https://raw.githubusercontent.com/joeltoumi/sensor_crtm/f5d1b4e463a4e1128b87cefb50fd7839982107af/card.png)

[paypalme]: https://www.paypal.me/joelruiz
[paypalbedge]: https://camo.githubusercontent.com/3073969b3e2923ae564193fabf646ce6a85329cd39cbdfd3fa4d814cb5b48e92/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465
