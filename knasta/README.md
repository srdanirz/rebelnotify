# Monitor Knasta

Monitor de ofertas y descuentos en Knasta.cl. Este monitor detecta nuevas ofertas publicadas en la categoría de Knasta Day y envía notificaciones a Discord con información detallada del producto, precio, y porcentaje de descuento.

## Descripción

Monitor especializado para Knasta.cl, enfocado en la sección de Knasta Day (ofertas especiales con descuentos significativos). Utiliza web scraping avanzado para extraer datos de JSON embebido en el HTML y puede filtrar ofertas por keywords específicas.

## Cómo Funciona

1. **Cache Inicial**: En el primer ciclo, carga todas las ofertas actuales en memoria
2. **Web Scraping Avanzado**: Extrae JSON del script `__NEXT_DATA__` embebido en el HTML
3. **Parsing de JSON**: Procesa datos estructurados de la página Next.js
4. **Extracción de Datos**: Obtiene título, precio actual, imagen, URL, y porcentaje de descuento
5. **Detección de Nuevos**: Compara contra el cache en memoria (lista INSTOCK)
6. **Filtrado por Keywords**: Opcionalmente filtra ofertas por palabras clave
7. **Notificación**: Envía webhook a Discord con detalles completos
8. **Actualización de Cache**: Agrega la nueva oferta al cache
9. **Rotación de User Agent**: Cambia user agent automáticamente en caso de error

## Requisitos

- Python 3.7 o superior
- Dependencias de Python
- Archivo `.env` con configuración
- Webhook de Discord
- Conexión a internet estable

## Instalación

1. Navega al directorio:
```bash
cd knasta
```

2. Instala las dependencias:
```bash
pip install requests
pip install beautifulsoup4
pip install python-dotenv
pip install urllib3
pip install random-user-agent
```

3. Crea el archivo `.env` con la configuración

## Configuración

### Archivo .env

Crea un archivo `.env` en el directorio del proyecto:

```env
# Discord Webhook Configuration
WEBHOOK=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
USERNAME=Knasta Monitor
AVATAR_URL=https://example.com/knasta-avatar.png
COLOUR=3447003

# Monitor Configuration
DELAY=10
KEYWORDS=
```

**Parámetros:**

- `WEBHOOK`: URL del webhook de Discord
- `USERNAME`: Nombre que aparecerá en Discord
- `AVATAR_URL`: URL de imagen de avatar (opcional)
- `COLOUR`: Color del embed en decimal (3447003 = azul)
- `DELAY`: Segundos entre cada ciclo de monitoreo (recomendado: 10-15)
- `KEYWORDS`: Palabras clave separadas por `%` para filtrar (opcional)

### Ejemplos de Keywords

**Sin filtros (todas las ofertas):**
```env
KEYWORDS=
```

**Filtrar tecnología:**
```env
KEYWORDS=notebook%laptop%tablet%smartphone%auriculares%parlante
```

**Filtrar hogar:**
```env
KEYWORDS=aspiradora%microondas%refrigerador%lavadora
```

## URL de Scraping

El monitor escanea:
```
https://knasta.cl/results?category=20106&knastaday=3
```

**Parámetros:**
- `category=20106`: Categoría específica
- `knastaday=3`: Filtro de Knasta Day (ofertas especiales)

## Uso

1. Configura el archivo `.env`

2. Ejecuta el monitor:
```bash
python knasta.py
```

3. Logs esperados:
```
STARTING MONITOR
Request delivered successfully, code 200.
[2025-11-01 14:30:45] [LOG] - Cycle #1 Complete
    [2025-11-01 14:30:45] [EVENT] - Checking Link #1
45
Initial Listing Load Complete, checking for changes in future cycles.
```

El número (45) indica cuántos productos encontró.

4. Al detectar una nueva oferta:
```
PRODUCT FOUND: Aspiradora Robot Xiaomi S10
Request delivered successfully, code 200.
```

5. La notificación de Discord incluye:
   - Título del producto con porcentaje de descuento (ej: "ASPIRADORA ROBOT [45%]")
   - Precio actual (en formato correcto: $199.990)
   - Enlace directo al producto
   - Imagen del producto
   - Autor: "New Discount - knasta.cl" con enlace a la categoría
   - Footer: "Rebel Notify"
   - Timestamp

## Estructura de Archivos

```
knasta/
├── knasta.py         # Script principal del monitor
├── .env              # Configuración (crear manualmente)
└── README.md         # Esta documentación
```

## Extracción de Datos

### Estructura del JSON Embebido

Knasta usa Next.js, que embebe datos en un script:

```html
<script id="__NEXT_DATA__" type="application/json">
{
  "props": {
    "pageProps": {
      "initialData": {
        "products": [
          {
            "title": "Producto",
            "current_price": 199990,
            "url": "/producto-url",
            "image": "https://...",
            "percent": 45
          }
        ]
      }
    }
  }
}
</script>
```

### Código de Extracción

```python
soup = soup.find('script', {'id': '__NEXT_DATA__'}).decode_contents()
json_data = json.loads(soup)
products = json_data['props']['pageProps']['initialData']['products']

for product in products:
    item = [
        product['title'],
        product['current_price'],
        product['url'],
        product['image'],
        product['percent'],
        url
    ]
```

## Formato de Datos

### Precio
```python
embed["description"] = f"**[PRICE]:** {int(product_item[1])/1000}"
```
El precio viene en formato integer (ejemplo: 199990) y se convierte a formato decimal (199.99) para mostrar.

### Título con Descuento
```python
embed["title"] = f'{product_item[0].upper()} [{product_item[4]}%]'
```
Ejemplo: "ASPIRADORA ROBOT XIAOMI [45%]"

### URL del Producto
```python
if product_item[2] == "":
    embed['url'] = f'{product_item[5]}'
else:
    embed['url'] = f'{product_item[2]}'
```
Usa la URL del producto si está disponible, sino usa la URL base de la búsqueda.

## Troubleshooting

### Error: "No module named 'dotenv'"
**Problema:** python-dotenv no está instalado.

**Solución:**
```bash
pip install python-dotenv
```

### Error: KeyError al parsear JSON
**Problema:** La estructura del JSON cambió o no se encontró.

**Solución:**
- Knasta puede haber actualizado su estructura
- Inspecciona manualmente el script `__NEXT_DATA__`
- Verifica que la página cargue correctamente
- Puede requerir actualización del código

### Error: "list index out of range"
**Problema:** No se encontró el script `__NEXT_DATA__`.

**Solución:**
- Verifica que la URL esté correcta
- Knasta puede estar bloqueando el scraping
- Intenta con diferentes user agents
- Verifica tu conexión a internet

### No detecta ofertas nuevas
**Problema:** Todas las ofertas ya están en cache o no hay nuevas.

**Solución:**
- Reinicia el monitor para limpiar el cache
- Verifica que knasta.cl tenga ofertas activas
- Las ofertas de Knasta Day cambian periódicamente
- Aumenta el DELAY para reducir frecuencia

### Exception: "Exception found"
**Problema:** Error durante el scraping o parsing.

**Solución:**
- Revisa el mensaje de error completo
- El monitor rota user agent automáticamente
- Verifica que la página cargue manualmente
- Knasta puede tener protecciones anti-bot

### Precio mal formateado
**Problema:** El precio aparece como "199.99" en lugar de "$199.990".

**Solución:**
- Esto es comportamiento actual del código
- Para formato chileno, modifica la línea de descripción
- Ejemplo: `f"**[PRICE]:** ${int(product_item[1]):,}"`

### Webhook no se entrega
**Problema:** URL incorrecta o rate limit.

**Solución:**
- Verifica la URL del webhook en `.env`
- Discord limita a 30 webhooks/minuto
- Prueba el webhook manualmente
- Verifica que el canal exista

### "Cache Cleared" pero no más notificaciones
**Problema:** Comportamiento esperado del primer ciclo.

**Solución:**
- El primer ciclo solo carga el cache
- Espera al menos DELAY segundos
- Los nuevos descuentos se detectarán después
- Verifica que haya nuevas ofertas en el sitio

### Keywords no filtran
**Problema:** Sintaxis incorrecta de keywords.

**Solución:**
- Usa `%` como separador, NO comas
- Keywords son case-insensitive
- Ejemplo correcto: `KEYWORDS=notebook%laptop`
- Ejemplo incorrecto: `KEYWORDS=notebook, laptop`

## Detalles Técnicos

### Sistema de Cache (INSTOCK)
```python
INSTOCK = []

def checker(item):
    for product in INSTOCK:
        if product == item:
            return True
    return False
```

- Cache en memoria (no persistente)
- Se limpia al reiniciar el monitor
- Compara arrays completos de datos del producto
- Previene duplicados durante la sesión

### Filtrado por Keywords
```python
for key in keywords:
    if key.lower() in item[0].lower():
        check = True
        break
```

- Case-insensitive
- Busca en el título del producto
- Si encuentra cualquier keyword, pasa el filtro
- Si keywords está vacío, pasa todo

### User Agent Rotation
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Accept': 'text/html,application/xhtml+xml,...',
    'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'knasta.cl',
}
```

- User agent de Safari en macOS
- Rota automáticamente en caso de error
- Headers específicos para knasta.cl

### JSON Parsing con BeautifulSoup
```python
soup = soup.find('script', {'id': '__NEXT_DATA__'}).decode_contents()
json_data = json.loads(soup)
```

- Busca el script específico por ID
- Extrae el contenido como string
- Parsea como JSON para acceso estructurado

### Comparator System
```python
def comparitor(item, start):
    if not checker(item):
        INSTOCK.append(item)
        if start == 0:
            discord_webhook(item)
```

- `start = 1`: Primer ciclo, solo carga cache
- `start = 0`: Ciclos subsecuentes, notifica nuevos

## Comparación con Otros Monitores

| Feature | Knasta | Descuentos Rata | Bold General |
|---------|--------|-----------------|--------------|
| Target | Knasta Day | Descuentos generales | Bold catálogo |
| Método | JSON embebido | HTML scraping | API REST |
| Cache | In-memory | In-memory | SQLite |
| Datos | Estructurados | Semi-estructurados | Estructurados |
| Complejidad | Media-Alta | Media | Baja |
| Robustez | Media | Baja | Alta |

## Mejores Prácticas

1. **DELAY Apropiado**: Usa 10-15 segundos entre ciclos
2. **Keywords Específicas**: Filtra por categorías de interés
3. **Canal Dedicado**: Usa un webhook dedicado para ofertas
4. **Primer Ciclo**: Ignora notificaciones del primer ciclo (es el cache inicial)
5. **Monitoreo Periódico**: Verifica que el código siga funcionando tras actualizaciones del sitio
6. **Reinicio Diario**: Considera reiniciar cada 24h para limpiar cache

## Limitaciones

- **Cache No Persistente**: Se pierde al reiniciar
- **Una Categoría**: Solo Knasta Day (category=20106)
- **Scraping de Next.js**: Vulnerable a cambios en estructura
- **Sin Validación**: No verifica si el descuento es real
- **Formato de Precio**: Puede necesitar ajustes para formato chileno

## Mejoras Futuras Sugeridas

- Base de datos SQLite para persistencia
- Soporte para múltiples categorías
- Validación de precios y descuentos
- Historial de precios
- Sistema de alertas por precio mínimo
- Formato de precio chileno (CLP)
- Detección de cambios de precio en productos existentes

## Estructura de Next.js

Knasta usa Next.js, que tiene características específicas:

1. **Server-Side Rendering (SSR)**: Los datos se renderizan en el servidor
2. **JSON Embebido**: `__NEXT_DATA__` contiene el estado inicial
3. **Hydration**: El JSON se usa para "hidratar" la app en el cliente
4. **Estructura Consistente**: La ruta al array de productos es predecible

Esto hace el scraping más robusto que HTML puro, pero requiere conocimiento de la estructura.

## Uso Responsable

- Usa DELAY apropiado (10+ segundos) para no sobrecargar el servidor
- No abuses del sistema para reventas masivas
- Respeta los términos de servicio de Knasta
- Considera el impacto de tu uso del monitor
- Las ofertas son para consumidores finales

## Soporte

Para problemas o preguntas:
- Verifica que el archivo `.env` esté correctamente configurado
- Asegúrate de que knasta.cl esté accesible
- Revisa que todas las dependencias estén instaladas
- Si hay errores de parsing, inspecciona el JSON embebido manualmente
- Knasta puede actualizar su estructura - contacta soporte con detalles
- Provee el traceback completo del error para mejor ayuda
