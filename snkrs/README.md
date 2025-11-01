# Monitor SNKRS Chile

Monitor de nuevos releases en la sección SNKRS de Nike Chile. Este monitor detecta cuando se agregan nuevos productos a la sección de futuros lanzamientos y envía notificaciones detalladas a Discord.

## Descripción

Este monitor rastrea continuamente la página de futuros lanzamientos de SNKRS Chile (nike.cl/snkrs/futuros) y detecta cuando se agregan nuevos productos. A diferencia de los monitores de SKU específicos, este monitor es "general" y captura todos los nuevos productos que aparecen en la categoría SNKRS.

## Cómo Funciona

1. **Scraping Inicial**: En el primer ciclo, carga todos los productos actuales en memoria (cache inicial)
2. **Monitoreo Continuo**: En cada ciclo subsecuente, compara los productos actuales con el cache
3. **Detección de Nuevos**: Cuando encuentra un producto que no está en el cache, lo considera nuevo
4. **Filtrado por Keywords**: Opcionalmente filtra productos por palabras clave positivas y negativas
5. **Notificación**: Envía webhook a Discord con información completa del producto
6. **Actualización de Cache**: Agrega el nuevo producto al cache para evitar duplicados

El monitor usa una URL traducida de Google Translate para evitar ciertas protecciones y obtener JSON limpio.

## Requisitos

- Python 3.7 o superior
- Archivo `.env` con configuración
- Webhook de Discord
- Conexión a internet estable

## Instalación

1. Navega al directorio:
```bash
cd snkrs
```

2. Instala las dependencias:
```bash
pip install requests
pip install beautifulsoup4
pip install python-dotenv
pip install urllib3
pip install random-user-agent
```

3. Crea el archivo `.env` con la configuración necesaria

## Configuración

### Archivo .env

Crea un archivo `.env` en el directorio del proyecto con el siguiente contenido:

```env
# Discord Webhook Configuration
WEBHOOK=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
USERNAME=Rebel Notify - SNKRS
AVATAR_URL=https://thumbs.dreamstime.com/b/web-183282388.jpg
COLOUR=15158332

# Monitor Configuration
DELAY=5
KEYWORDS=
NEG_KEYWORDS=
```

**Parámetros:**

- `WEBHOOK`: URL del webhook de Discord
- `USERNAME`: Nombre que aparecerá en las notificaciones de Discord
- `AVATAR_URL`: URL de la imagen de avatar para el webhook
- `COLOUR`: Color del embed en decimal (15158332 = rojo)
- `DELAY`: Segundos entre cada ciclo de monitoreo (recomendado: 5-10)
- `KEYWORDS`: Palabras clave separadas por `%` para filtrar productos (ejemplo: `Jordan%Dunk%Air Max`)
- `NEG_KEYWORDS`: Palabras clave negativas separadas por `%` para excluir productos (ejemplo: `Kids%Toddler`)

### Configuración de Keywords

**Sin filtros (monitorear todo):**
```env
KEYWORDS=
NEG_KEYWORDS=
```

**Con filtros positivos (solo Jordan y Dunk):**
```env
KEYWORDS=Jordan%Dunk
NEG_KEYWORDS=
```

**Con filtros negativos (todo excepto productos de niños):**
```env
KEYWORDS=
NEG_KEYWORDS=Kids%Toddler%Infant
```

**Con ambos filtros:**
```env
KEYWORDS=Jordan%Dunk%Air Max
NEG_KEYWORDS=Kids%Toddler%Women
```

## Uso

1. Configura el archivo `.env` con tus valores

2. Ejecuta el monitor:
```bash
python snkrs.py
```

3. Logs esperados:
```
STARTING MONITOR
[2025-11-01 14:30:45] [LOG] - Cycle #1 Complete
    [2025-11-01 14:30:45] [EVENT] - Checking Link #1
Initial Listing Load Complete, checking for changes in future cycles.
[2025-11-01 14:30:50] [LOG] - Cycle #2 Complete
    [2025-11-01 14:30:50] [EVENT] - Checking Link #1
```

4. Al detectar un nuevo producto:
```
PRODUCT FOUND: Air Jordan 1 Retro High OG
Payload delivered successfully, code 200.
```

5. La notificación de Discord incluye:
   - Título del producto
   - Enlace al producto
   - Imagen del producto
   - SKU (Product Reference)
   - Color
   - Fecha de lanzamiento
   - Hora de lanzamiento
   - Tallas disponibles con cantidades

## Estructura de la Notificación

El webhook de Discord incluye:

```
AUTHOR: Product Added @ SNKRS Chile
TITLE: [Nombre del Producto]
URL: [Enlace directo al producto]
THUMBNAIL: [Imagen del producto]

FIELDS:
- SKU: [Código del producto]
- Color: [Color del producto]
- Release Date: [Fecha de lanzamiento]
- Release Hour: [Hora de lanzamiento]

SIZES:
[US 8] - [QTY: 10]
[US 8.5] - [QTY: 15]
[US 9] - [QTY: 20]
...
```

## Estructura de Archivos

```
snkrs/
├── snkrs.py          # Script principal del monitor
├── .env              # Configuración (crear manualmente)
├── test.log          # Logs de ejecución (se crea automáticamente)
└── README.md         # Esta documentación
```

## Troubleshooting

### Error: "No se encuentra el módulo dotenv"
**Problema:** python-dotenv no está instalado.

**Solución:**
```bash
pip install python-dotenv
```

### Error: "KeyError" al leer configuración
**Problema:** Falta un parámetro en el archivo `.env`.

**Solución:**
- Verifica que todos los parámetros estén presentes en `.env`
- Asegúrate de que no haya espacios extra
- Verifica que el formato sea `KEY=value` sin espacios alrededor del `=`

### No detecta productos nuevos
**Problema:** El cache inicial puede estar incorrecto o hay problemas de conectividad.

**Solución:**
- Verifica tu conexión a internet
- Visita manualmente https://www.nike.cl/snkrs/futuros para confirmar que carga
- Elimina el archivo de logs y reinicia el monitor
- Aumenta el DELAY a 10 segundos

### Recibe notificación de "Cache Cleared" pero nada más
**Problema:** Este es el comportamiento esperado en el primer ciclo.

**Solución:**
- Es normal, el primer ciclo solo carga el cache
- Espera al menos un ciclo más (DELAY segundos)
- Los productos nuevos se detectarán en ciclos subsecuentes

### Webhook no se entrega
**Problema:** URL incorrecta o rate limit de Discord.

**Solución:**
- Verifica la URL del webhook en `.env`
- Discord limita a 30 webhooks por minuto
- Prueba el webhook manualmente
- Verifica que el canal de Discord exista

### Error de conexión o timeout
**Problema:** Problemas de red o Nike bloqueó la conexión.

**Solución:**
- Verifica tu conexión a internet
- El monitor rota user agents automáticamente
- Aumenta el DELAY para reducir la frecuencia de requests
- Nike puede tener rate limiting temporal

### Keywords no filtran correctamente
**Problema:** Sintaxis incorrecta de keywords.

**Solución:**
- Las keywords son case-insensitive (no distinguen mayúsculas)
- Usa `%` como separador, NO comas ni espacios
- Ejemplo correcto: `KEYWORDS=Jordan%Dunk%Air`
- Ejemplo incorrecto: `KEYWORDS=Jordan, Dunk, Air`

### El monitor encuentra el mismo producto repetidamente
**Problema:** El sistema de cache no está funcionando correctamente.

**Solución:**
- Verifica que el monitor no se esté reiniciando constantemente
- El cache se mantiene en memoria (variable INSTOCK)
- Si reinicias el monitor, el cache se limpia
- Esto es comportamiento esperado después de reiniciar

## Detalles Técnicos

### URL de Scraping
El monitor usa una URL traducida por Google Translate:
```
https://www-nike-cl.translate.goog/api/catalog_system/pub/products/search?fq=B:2000002&_from=0&_to=49&O=OrderByReleaseDateDESC&_x_tr_sl=el&_x_tr_tl=en&_x_tr_hl=en-GB&_x_tr_pto=wapp
```

Esto ayuda a:
- Evitar algunas protecciones anti-bot
- Obtener respuestas JSON consistentes
- Reducir la probabilidad de bloqueos

### Sistema de Cache
- El cache (INSTOCK) almacena arrays de datos de productos
- Cada producto es único por su combinación de campos
- Los duplicados se eliminan automáticamente
- El cache persiste durante toda la ejecución del monitor

### User Agent Rotation
- El monitor usa random-user-agent para rotar user agents
- Se enfoca en Chrome Mobile para parecer más natural
- Rota automáticamente en caso de error

### Rate Limiting
- Nike tiene rate limiting pero es relativamente permisivo para esta API
- DELAY de 5 segundos es generalmente seguro
- Para uso intensivo, considera aumentar a 10-15 segundos

## Comparación con Otros Monitores

| Feature | SNKRS Monitor | SKU Monitors | General Monitors |
|---------|---------------|--------------|------------------|
| Target | SNKRS Releases | SKU específicos | Catálogo general |
| Filtrado | Keywords | Por SKU | Keywords/Categoría |
| Complejidad | Media | Alta (Bifrost) | Media |
| Información | Release completo | Disponibilidad | Productos nuevos |
| Uso | Futuros drops | Restocks | Nuevos listados |

## Mejores Prácticas

1. **DELAY Apropiado**: Usa al menos 5 segundos para evitar rate limiting
2. **Keywords Específicos**: Usa keywords específicos para reducir ruido
3. **Monitoreo de Logs**: Revisa `test.log` regularmente para errores
4. **Webhook Dedicado**: Usa un webhook/canal dedicado para SNKRS
5. **Restart Periódico**: Considera reiniciar el monitor cada 24 horas para limpieza

## Notas Adicionales

- Este monitor es para notificaciones de **anuncios de productos**, no de restocks
- Los productos detectados son futuros lanzamientos, no disponibilidad actual
- La información de tallas puede incluir cantidades o enlaces ATC dependiendo del estado
- El primer ciclo siempre envía "Cache Cleared" - esto es normal
- Los logs se guardan en `test.log` con timestamp y nivel de logging

## Soporte

Para problemas o preguntas:
- Verifica que el archivo `.env` esté correctamente configurado
- Revisa los logs en `test.log` para mensajes de error detallados
- Asegúrate de que Nike SNKRS esté accesible desde tu ubicación
- Contacta al equipo de Rebel Notify para soporte adicional
