# Monitor MoreDrops General

Monitor de nuevos productos en la categoría de sneakers de MoreDrops.cl. Este monitor detecta cuando se agregan nuevos productos al catálogo de Drops > Men > Footwear > Sneakers y envía notificaciones automáticas a Discord.

## Descripción

Monitor "general" que rastrea la categoría específica de sneakers para hombres en MoreDrops.cl. Similar al monitor de Bold General, utiliza web scraping (BeautifulSoup) en lugar de API, y mantiene una base de datos SQLite local para trackear productos ya notificados. Incluye soporte de multi-threading y proxy opcional.

## Cómo Funciona

1. **Inicialización de Base de Datos**: Crea `moredrops.db` (SQLite) para trackear productos
2. **Multi-Threading**: Ejecuta 2 threads simultáneos para mejor cobertura
3. **Web Scraping**: Parsea HTML de la página de productos usando BeautifulSoup
4. **Extracción de Datos**: Obtiene nombre, precio, imagen, y URL de cada producto
5. **Detección de Nuevos**: Compara contra la base de datos usando título y SKU
6. **Notificación**: Envía webhook a Discord con información del producto
7. **Registro en DB**: Guarda el producto para evitar duplicados en el futuro
8. **Manejo de Errores**: Rotación automática de user agents y proxies en caso de fallo

## Requisitos

- Python 3.7 o superior
- SQLite3 (incluido con Python)
- Dependencias de Python
- Webhook de Discord
- Proxies opcionales (free proxy support incluido)

## Instalación

1. Navega al directorio:
```bash
cd moredrops-general
```

2. Instala las dependencias:
```bash
pip install requests
pip install beautifulsoup4
pip install sqlalchemy
pip install random-user-agent
pip install free-proxy
```

3. Configura el archivo `config.py`

## Configuración

### config.py

Edita el archivo `config.py` con tu configuración:

```python
class Discord:
    WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL_HERE'
    USERNAME = 'REBEL NOTIFY'
    AVATAR_URL = 'https://i.pinimg.com/originals/6b/fd/41/6bfd41330325c4ad1f1e0bb6d4291db4.jpg'
    COLOUR = 16777215
    FOOTER_TEXT = 'Rebel Notify'
    FOOTER_URL = 'https://i.pinimg.com/originals/6b/fd/41/6bfd41330325c4ad1f1e0bb6d4291db4.jpg'

class Configuration:
    ENABLE_FREE_PROXY = False
    USERAGENT = ''
```

**Parámetros Discord:**
- `WEBHOOK_URL`: URL del webhook de Discord para notificaciones
- `USERNAME`: Nombre que aparecerá en Discord
- `AVATAR_URL`: URL de la imagen de avatar
- `COLOUR`: Color del embed en decimal (16777215 = blanco)
- `FOOTER_TEXT`: Texto del footer del embed
- `FOOTER_URL`: Icono del footer

**Parámetros Configuration:**
- `ENABLE_FREE_PROXY`: `True` para usar proxies gratuitos automáticos, `False` para conexión directa
- `USERAGENT`: User agent personalizado (déjalo vacío `''` para rotación automática)

## Base de Datos

### db.py

El archivo `db.py` define el modelo de base de datos:

```python
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'
    title = Column(String, primary_key=True)
    sku = Column(String, primary_key=True)

engine = create_engine('sqlite:///moredrops.db')
Base.metadata.create_all(engine)
```

La base de datos almacena:
- `title`: Nombre del producto
- `sku`: SKU extraído de la URL del producto

## URL de Scraping

El monitor escanea la siguiente página:

```
https://moredrops.cl/Drops/Men/Footwear/Sneakers-Men/c/dropsHombreFootwearSneakers?q=%3Acreationtime&page={page}
```

**Parámetros:**
- `q=%3Acreationtime`: Ordenado por fecha de creación
- `page`: Número de página (actualmente solo página 1)

## Uso

1. Configura `config.py` con tus valores

2. Ejecuta el monitor:
```bash
python __main__.py
```

3. Logs esperados:
```
STARTING MONITOR
[Scraping page 1...]
[Checking products...]
```

4. Al detectar un nuevo producto:
```
Payload delivered successfully, code 200.
```

5. La notificación de Discord incluye:
   - Título del producto
   - Enlace al producto
   - Imagen del producto
   - SKU (extraído de URL)
   - Precio
   - Estado: "In Stock"

## Estructura de Archivos

```
moredrops-general/
├── __main__.py       # Script principal del monitor
├── config.py         # Configuración de Discord y opciones
├── db.py             # Modelo de base de datos SQLite
├── moredrops.db      # Base de datos SQLite (se crea automáticamente)
└── README.md         # Esta documentación
```

## Extracción de Datos

### Estructura HTML

El monitor busca elementos con la siguiente estructura:

```html
<div class="product-item">
    <a class="name" href="/producto-url">Nombre del Producto</a>
    <div class="item--price">$99.990</div>
    <img src="https://moredrops.cl/imagen.jpg">
</div>
```

### Código de Extracción

```python
name = product.find('a', {'class':'name'}).text
price = product.find('div', {'class':'item--price'}).text
img = product.find('img')['src']
product_url = product.find('a', {'class': 'name'})['href']
sku = product_url.split('/')[-1]
```

## Troubleshooting

### Error: "No module named 'bs4'"
**Problema:** BeautifulSoup4 no está instalado.

**Solución:**
```bash
pip install beautifulsoup4
```

### Error: "unable to open database file"
**Problema:** No hay permisos de escritura en el directorio.

**Solución:**
- Verifica permisos del directorio
- Ejecuta con permisos adecuados
- La base de datos se creará automáticamente

### Productos duplicados en notificaciones
**Problema:** La base de datos puede estar corrupta.

**Solución:**
- Elimina `moredrops.db` y deja que se recree
- Verifica la lógica de comparación de productos
- Reinicia el monitor completamente

### No detecta productos nuevos
**Problema:** Todos los productos ya están en la base de datos.

**Solución:**
- Elimina `moredrops.db` para limpiar el cache
- Verifica que MoreDrops tenga productos nuevos
- Revisa que la página cargue correctamente

### Error de parsing HTML
**Problema:** MoreDrops cambió la estructura del sitio.

**Solución:**
- Inspecciona la página manualmente con DevTools
- Verifica las clases CSS usadas en el código
- Puede requerir actualización del código de scraping
- Contacta soporte con detalles del cambio

### Error de conexión constante
**Problema:** Problemas de red o MoreDrops bloqueó la IP.

**Solución:**
- Verifica tu conexión a internet
- Prueba habilitando `ENABLE_FREE_PROXY = True`
- Aumenta el delay: modifica `time.sleep(2.5)` a un valor mayor
- MoreDrops puede tener rate limiting

### Free proxy no funciona
**Problema:** Los proxies gratuitos son inestables.

**Solución:**
- Cambia `ENABLE_FREE_PROXY = False`
- Los proxies gratuitos son lentos y poco confiables
- Considera proxies de pago para uso en producción

### Webhook no se entrega
**Problema:** URL incorrecta o rate limit de Discord.

**Solución:**
- Verifica `WEBHOOK_URL` en `config.py`
- Discord limita a 30 webhooks por minuto
- Verifica que el canal exista
- Prueba el webhook manualmente con curl

### Traceback completo sin datos
**Problema:** La página no cargó o no hay productos.

**Solución:**
- El código tiene try/except que captura errores
- Los tracebacks se imprimen pero el monitor continúa
- Verifica los logs para el error específico
- La página puede estar temporalmente inaccesible

## Multi-Threading

El monitor ejecuta 2 threads simultáneos:

```python
if __name__ == '__main__':
    threads = []
    for i in range(2):
        x = threading.Thread(target=monitor)
        threads.append(x)
        x.start()
        time.sleep(0.5)
```

**Ventajas:**
- Mayor velocidad de detección
- Redundancia en caso de que un thread falle

**Consideraciones:**
- Cada thread tiene su propia sesión de base de datos
- SQLite maneja locks automáticamente
- Delay de 0.5s entre inicio de threads

## Detalles Técnicos

### User Agent Rotation
- Si `USERAGENT` está vacío, rota automáticamente
- Usa `random-user-agent` library
- Prefiere Chrome Mobile para parecer más natural

### Proxy Support
- Free proxy via `free-proxy` library
- Soporta proxies de GB, US, CL
- Rotación automática en caso de fallo
- Modo localhost (sin proxy) por defecto

### Session Management
- Cada thread crea su propia `requests.Session()`
- Las sesiones mantienen cookies automáticamente
- Ayuda con la consistencia de scraping

### Error Handling
El monitor maneja estas excepciones:
- `ConnectionError`
- `ConnectTimeout`
- `ChunkedEncodingError`
- `ContentDecodingError`
- `HTTPError`
- `ReadTimeout`
- `SSLError`
- `Timeout`
- `RequestException`
- `TooManyRedirects`
- `Exception` (catch-all con traceback)

### Cookie Handling
El código incluye una cookie de ejemplo en el error handler:

```python
'Cookie': 'anonymous-consents=%5B%5D; _fbp=...; QueueITAccepted-SDFrts345E-V3_drops89=...'
```

Esta puede ser necesaria si MoreDrops usa queue-it para protección.

## Comparación con Otros Monitores

| Feature | MoreDrops General | Bold General | SNKRS |
|---------|-------------------|--------------|-------|
| Target | Sneakers Men | Catálogo completo | SNKRS Releases |
| Método | Web Scraping | API | API |
| Base de Datos | SQLite (sku) | SQLite (code) | In-memory |
| Threads | 2 | 2 | 1 |
| Proxy | Optional/Free | Optional/Free | None |
| Complejidad | Media | Baja | Media |

## Mejores Prácticas

1. **Primera Ejecución**: Notificará todos los productos actuales (50+)
2. **Limpieza Periódica**: Elimina `moredrops.db` semanalmente para refrescar
3. **Webhook Dedicado**: Usa un canal dedicado debido al volumen potencial
4. **Delay Apropiado**: 2.5s entre ciclos es generalmente seguro
5. **Monitoreo Manual**: Verifica periódicamente que la página sigue cargando

## Limitaciones

- **Una Página**: Solo escanea la primera página (~50 productos)
- **Categoría Específica**: Solo sneakers de hombres
- **No Filtra**: No tiene sistema de keywords
- **Free Proxies**: Son lentos e inestables
- **Scraping Frágil**: Cambios en HTML requieren actualización del código

## Mejoras Futuras Sugeridas

- Escaneo de múltiples páginas
- Sistema de filtrado por keywords
- Soporte para otras categorías
- Detección de cambios de precio
- Soporte para proxies de pago
- Validación de HTML antes de parsear

## Diferencias con Bold General

1. **Método de Obtención**:
   - MoreDrops: Web scraping con BeautifulSoup
   - Bold: API REST con JSON

2. **Estructura de Datos**:
   - MoreDrops: Parse manual de HTML
   - Bold: JSON estructurado

3. **SKU/Code**:
   - MoreDrops: Extraído de URL
   - Bold: Provisto por API

4. **Robustez**:
   - MoreDrops: Más frágil (depende de HTML)
   - Bold: Más robusto (API estable)

## Soporte

Para problemas o preguntas:
- Verifica que `config.py` esté correctamente configurado
- Asegúrate de que todas las dependencias estén instaladas
- Revisa `moredrops.db` para ver qué productos están trackeados
- Inspecciona manualmente la página para verificar cambios en HTML
- Contacta al equipo de Rebel Notify con tracebacks específicos
