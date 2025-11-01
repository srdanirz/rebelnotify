# Monitor Descuentos Rata

Monitor de descuentos y ofertas en DescuentosRata.com. Este monitor detecta nuevos descuentos publicados en la página principal y envía notificaciones a Discord con información del producto y porcentaje de descuento.

## Descripción

Monitor especializado para el sitio de descuentos DescuentosRata.com. Rastrea la página principal en busca de nuevas ofertas publicadas y puede filtrarlas por keywords específicas. Es ideal para detectar ofertas de tecnología, ropa, y otros productos populares en Chile.

## Cómo Funciona

1. **Cache Inicial**: En el primer ciclo, carga todos los descuentos actuales en memoria
2. **Web Scraping**: Parsea el HTML de la página principal usando BeautifulSoup
3. **Extracción de Datos**: Obtiene título, precio/descuento, URL, e imagen de cada oferta
4. **Detección de Nuevos**: Compara contra el cache en memoria (lista INSTOCK)
5. **Filtrado por Keywords**: Opcionalmente filtra ofertas por palabras clave
6. **Notificación**: Envía webhook a Discord con detalles de la oferta
7. **Actualización de Cache**: Agrega la nueva oferta al cache para evitar duplicados
8. **Rotación de User Agent**: Cambia user agent automáticamente en caso de error

## Requisitos

- Python 3.7 o superior
- Dependencias de Python
- Archivo `.env` con configuración
- Webhook de Discord
- Conexión a internet

## Instalación

1. Navega al directorio:
```bash
cd descuentosrata
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
USERNAME=Descuentos Rata Monitor
AVATAR_URL=https://example.com/avatar.png
COLOUR=15158332

# Monitor Configuration
DELAY=10
KEYWORDS=
```

**Parámetros:**

- `WEBHOOK`: URL del webhook de Discord
- `USERNAME`: Nombre que aparecerá en Discord
- `AVATAR_URL`: URL de imagen de avatar (opcional)
- `COLOUR`: Color del embed en decimal (15158332 = rojo)
- `DELAY`: Segundos entre cada ciclo de monitoreo (recomendado: 10-15)
- `KEYWORDS`: Palabras clave separadas por `%` para filtrar (opcional)

### Ejemplos de Keywords

**Sin filtros (todos los descuentos):**
```env
KEYWORDS=
```

**Filtrar solo tecnología:**
```env
KEYWORDS=notebook%laptop%tablet%smartphone%monitor%teclado%mouse
```

**Filtrar ropa y zapatillas:**
```env
KEYWORDS=zapatillas%polera%polerón%pantalón%nike%adidas
```

## URL de Scraping

El monitor escanea:
```
https://descuentosrata.com/
```

## Uso

1. Configura el archivo `.env`

2. Ejecuta el monitor:
```bash
python descuentosrata.py
```

3. Logs esperados:
```
STARTING CYCLES - DESCUENTOSRATA
Request delivered successfully, code 200.
[2025-11-01 14:30:45] [LOG] - Cycle #1 Complete
    [2025-11-01 14:30:45] [EVENT] - Checking Link #1
30
Initial Listing Load Complete, checking for changes in future cycles.
```

El número (30) indica cuántos productos encontró en la página.

4. Al detectar un nuevo descuento:
```
PRODUCT FOUND: Notebook Gamer ASUS ROG
Request delivered successfully, code 200.
```

5. La notificación de Discord incluye:
   - Título del producto
   - Precio/Descuento
   - Enlace al descuento
   - Imagen del producto
   - Autor: "New Discount - DESCUENTOSRATA"
   - Footer: "Rebel Notify"
   - Timestamp

## Estructura de Archivos

```
descuentosrata/
├── descuentosrata.py   # Script principal del monitor
├── .env                # Configuración (crear manualmente)
└── README.md           # Esta documentación
```

## Extracción de Datos

### Estructura HTML

El monitor busca elementos con la siguiente estructura:

```html
<div class="my-2 col-md-4 col-lg-3 col-6">
    <span class="font-weight-bold">Título del Producto</span>
    <span class="font-weight-normal">-50% $19.990</span>
    <a href="/oferta-url">Ver oferta</a>
    <div class="img-responsive" style="url(/imagen.jpg)">Imagen</div>
</div>
```

### Código de Extracción

```python
item = [
    product.find('span', {'class':'font-weight-bold'}).text.strip(),  # Título
    product.find('span', {'class':'font-weight-normal'}).text.strip(),  # Precio/Desc
    product.find('a')['href'],  # URL
    product.find('div', {'class':'img-responsive'})['style'],  # Imagen
    url  # URL base
]
```

## Troubleshooting

### Error: "No module named 'dotenv'"
**Problema:** python-dotenv no está instalado.

**Solución:**
```bash
pip install python-dotenv
```

### Error: KeyError al leer configuración
**Problema:** Falta un parámetro en `.env`.

**Solución:**
- Verifica que todos los parámetros estén presentes
- Formato correcto: `KEY=value` sin espacios
- No uses comillas en los valores

### No detecta descuentos nuevos
**Problema:** Todos los descuentos ya están en cache o la página no carga.

**Solución:**
- Reinicia el monitor para limpiar el cache
- Verifica que descuentosrata.com esté accesible
- Aumenta el DELAY a 15 segundos
- Verifica tu conexión a internet

### Error de parsing HTML
**Problema:** El sitio cambió su estructura.

**Solución:**
- Inspecciona la página manualmente con DevTools
- Verifica las clases CSS usadas
- Puede requerir actualización del código
- Contacta soporte con detalles

### Exception: "Exception found"
**Problema:** Error genérico durante el scraping.

**Solución:**
- Revisa el mensaje de error completo
- El monitor rota user agent automáticamente
- Verifica que la página cargue manualmente
- Aumenta el DELAY entre ciclos

### Webhook no se entrega
**Problema:** URL incorrecta o rate limit.

**Solución:**
- Verifica la URL del webhook en `.env`
- Discord limita a 30 webhooks/minuto
- Prueba el webhook manualmente
- Verifica que el canal exista

### "Cache Cleared" pero no recibe más notificaciones
**Problema:** Comportamiento esperado del primer ciclo.

**Solución:**
- El primer ciclo solo carga el cache
- Espera al menos DELAY segundos
- Los nuevos descuentos se detectarán en ciclos siguientes
- Si persiste, verifica que haya nuevos descuentos en el sitio

### Keywords no filtran correctamente
**Problema:** Sintaxis incorrecta o keywords muy específicas.

**Solución:**
- Usa `%` como separador, NO comas
- Keywords son case-insensitive
- Ejemplo correcto: `KEYWORDS=notebook%laptop%pc`
- Ejemplo incorrecto: `KEYWORDS=notebook, laptop, pc`
- Prueba con keywords más generales

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
- Compara arrays completos de datos
- Previene duplicados dentro de la misma sesión

### Filtrado por Keywords
```python
for key in keywords:
    if key.lower() in item[0].lower():
        check = True
        break
```

- Case-insensitive (no distingue mayúsculas)
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
    'Host': 'descuentosrata.com',
}
```

- User agent de Safari en macOS
- Rota automáticamente en caso de error
- Headers específicos para descuentosrata.com

### Remove Duplicates
```python
def remove_duplicates(mylist):
    return [list(t) for t in set(tuple(element) for element in mylist)]
```

- Elimina duplicados de la lista de productos
- Convierte listas a tuplas para usar set()
- Previene notificaciones duplicadas en el mismo ciclo

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
- Agrega al cache antes de notificar

## Comparación con Otros Monitores

| Feature | Descuentos Rata | Knasta | SNKRS |
|---------|-----------------|--------|-------|
| Target | Descuentos generales | Knasta deals | SNKRS releases |
| Método | Web Scraping | Web Scraping (JSON) | API |
| Cache | In-memory | In-memory | In-memory |
| Filtrado | Keywords | Keywords | Keywords |
| Complejidad | Media | Media | Media |
| Frecuencia | Media | Media | Baja |

## Mejores Prácticas

1. **DELAY Apropiado**: Usa al menos 10 segundos entre ciclos
2. **Keywords Específicas**: Reduce ruido con keywords bien elegidas
3. **Canal Dedicado**: Usa un canal/webhook dedicado para descuentos
4. **Primer Ciclo**: Ignora las notificaciones del primer ciclo
5. **Reinicio Periódico**: Considera reiniciar cada 24h para limpiar cache

## Limitaciones

- **Cache No Persistente**: Se pierde al reiniciar
- **Solo Página Principal**: No escanea categorías
- **Sin Base de Datos**: No hay historial de descuentos
- **Scraping Simple**: Vulnerable a cambios en HTML
- **Sin Validación de Precio**: No verifica si el descuento es real

## Mejoras Futuras Sugeridas

- Base de datos SQLite para persistencia
- Escaneo de múltiples categorías
- Validación de precios/descuentos
- Sistema de alertas por precio mínimo
- Historial de precios
- Notificaciones de cambios de precio

## Uso Responsable

- Usa DELAY apropiado para no sobrecargar el servidor
- No compartas ofertas de manera masiva sin permiso
- Respeta los términos de servicio de DescuentosRata
- Considera el impacto de tu uso del monitor

## Soporte

Para problemas o preguntas:
- Verifica que el archivo `.env` esté correctamente configurado
- Asegúrate de que descuentosrata.com esté accesible
- Revisa que las dependencias estén instaladas
- Inspecciona manualmente la página si hay errores de parsing
- Contacta al equipo de Rebel Notify con logs de error
