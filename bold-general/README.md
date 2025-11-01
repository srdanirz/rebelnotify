# Monitor Bold General

Monitor de nuevos productos en el catálogo general de Bold.cl. Este monitor detecta cuando se agregan nuevos productos al inventario de Bold y envía notificaciones automáticas a Discord con información de stock y precio.

## Descripción

Este es un monitor "general" que rastrea el catálogo completo de Bold.cl (no solo SNKRS/Drops). Utiliza la API de Bold para obtener productos y una base de datos SQLite local para trackear qué productos ya han sido notificados. Soporta filtrado por keywords, multi-threading, y proxy rotation automática.

## Cómo Funciona

1. **Inicialización de Base de Datos**: Crea una base de datos SQLite local (`bold.db`) para trackear productos
2. **Multi-Threading**: Ejecuta 2 threads simultáneos para mayor velocidad de monitoreo
3. **Scraping de API**: Consulta múltiples páginas de la API de Bold (hasta 5 páginas, 50 productos por página)
4. **Detección de Nuevos**: Compara contra la base de datos local
5. **Productos en Stock**: Solo notifica productos que están actualmente en stock
6. **Notificación**: Envía webhook a Discord con detalles completos
7. **Registro en DB**: Guarda el producto en la base de datos para evitar duplicados
8. **Limpieza Automática**: Elimina productos de la DB cuando salen de stock

## Requisitos

- Python 3.7 o superior
- SQLite3 (incluido con Python)
- Dependencias de Python
- Webhook de Discord
- Proxies opcionales (free proxy support incluido)

## Instalación

1. Navega al directorio:
```bash
cd bold-general
```

2. Instala las dependencias:
```bash
pip install requests
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
    code = Column(String, primary_key=True)

engine = create_engine('sqlite:///bold.db')
Base.metadata.create_all(engine)
```

La base de datos almacena:
- `title`: Nombre del producto
- `code`: Código/SKU del producto

## Uso

1. Configura `config.py` con tus valores

2. Ejecuta el monitor:
```bash
python __main__.py
```

3. Logs esperados:
```
STARTING MONITOR
[Scanning page 1...]
[Scanning page 2...]
[Scanning page 3...]
```

4. Al detectar un nuevo producto:
```
Payload delivered successfully, code 200.
```

5. La notificación de Discord incluye:
   - Título del producto
   - Enlace al producto
   - Imagen del producto
   - SKU/Code
   - Precio
   - Nivel de stock
   - Estado: "In Stock"

## Estructura de Archivos

```
bold-general/
├── __main__.py       # Script principal del monitor
├── config.py         # Configuración de Discord y opciones
├── db.py             # Modelo de base de datos SQLite
├── bold.db           # Base de datos SQLite (se crea automáticamente)
└── README.md         # Esta documentación
```

## API de Bold

El monitor consulta la siguiente API:

```
https://api.cxl8rgz-articulos1-p1-public.model-t.cc.commerce.ondemand.com/rest/v2/boldb2cstore/products/search
```

**Parámetros:**
- `fields`: Campos a retornar (url, code, name, price, images, stock, etc.)
- `query`: Filtro (`:DEFAULT:allCategories:boldMarcas`)
- `currentPage`: Número de página (1-5)
- `pageSize`: Productos por página (50)
- `lang`: Idioma (es_CL)
- `curr`: Moneda (CLP)

## Estructura de la Base de Datos

### Tabla: products

| Campo | Tipo | Descripción |
|-------|------|-------------|
| title | String (PK) | Nombre del producto |
| code | String (PK) | SKU/código del producto |

**Operaciones:**
- **INSERT**: Cuando se detecta un nuevo producto en stock
- **DELETE**: Cuando un producto sale de stock
- **SELECT**: Para verificar si un producto ya fue notificado

## Troubleshooting

### Error: "No module named 'sqlalchemy'"
**Problema:** SQLAlchemy no está instalado.

**Solución:**
```bash
pip install sqlalchemy
```

### Error: "unable to open database file"
**Problema:** No hay permisos de escritura en el directorio.

**Solución:**
- Verifica permisos del directorio
- Ejecuta con permisos adecuados
- La base de datos se creará automáticamente en el primer run

### Productos duplicados en notificaciones
**Problema:** La base de datos puede estar corrupta o no se está consultando correctamente.

**Solución:**
- Elimina `bold.db` y deja que se recree
- Verifica que el código de comparación funcione correctamente
- Reinicia el monitor

### No detecta productos nuevos
**Problema:** Todos los productos ya están en la base de datos o no hay productos en stock.

**Solución:**
- Elimina `bold.db` para limpiar el cache
- Verifica que Bold.cl tenga productos en stock
- Revisa los logs para errores de conexión

### Error de conexión constante
**Problema:** Problemas de red o la API de Bold no responde.

**Solución:**
- Verifica tu conexión a internet
- Bold puede estar en mantenimiento
- Prueba habilitando `ENABLE_FREE_PROXY = True`
- Aumenta el delay entre requests (modifica `time.sleep(2.5)`)

### Free proxy no funciona
**Problema:** Los proxies gratuitos son inestables.

**Solución:**
- Cambia `ENABLE_FREE_PROXY = False` para usar conexión directa
- Los proxies gratuitos son lentos y poco confiables
- Para uso en producción, considera proxies de pago

### Webhook no se entrega
**Problema:** URL incorrecta o rate limit de Discord.

**Solución:**
- Verifica `WEBHOOK_URL` en `config.py`
- Discord limita a 30 webhooks por minuto
- Verifica que el canal exista
- Prueba el webhook manualmente

### El monitor se detiene inesperadamente
**Problema:** Excepciones no manejadas o problemas de red.

**Solución:**
- Revisa los logs para el error específico
- El monitor tiene manejo amplio de excepciones
- Si persiste, contacta soporte con el traceback completo

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
- Mayor velocidad de monitoreo
- Mejor cobertura del catálogo

**Consideraciones:**
- Cada thread tiene su propia sesión de base de datos
- Locks automáticos de SQLite previenen race conditions
- Delay de 0.5s entre inicio de threads

## Detalles Técnicos

### User Agent Rotation
- Si `USERAGENT` está vacío, rota automáticamente
- Usa `random-user-agent` para user agents realistas
- Se enfoca en Chrome Mobile

### Proxy Support
- Free proxy via `free-proxy` library
- Soporta proxies de GB, US, CL
- Rotación automática en caso de fallo
- Modo localhost (sin proxy) por defecto

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
- `Exception` (catch-all)

### Stock Detection
```python
if product['stock']['stockLevelStatus'] == 'inStock' and query is None:
    # Nuevo producto en stock - notificar
elif product['stock']['stockLevelStatus'] != 'InStock' and query is not None:
    # Producto fuera de stock - eliminar de DB
```

## Comparación con Otros Monitores

| Feature | Bold General | Bold Restock | SNKRS |
|---------|--------------|--------------|-------|
| Target | Catálogo completo | SKUs específicos | SNKRS Releases |
| Base de Datos | SQLite | In-memory | In-memory |
| Threads | 2 | Variable | 1 |
| API | SAP Commerce | Hybris Cart | Nike API |
| Proxy | Optional/Free | Required | None |

## Mejores Prácticas

1. **Primera Ejecución**: En la primera ejecución, se notificarán muchos productos (todos los que estén en stock)
2. **Limpieza Periódica**: Considera eliminar `bold.db` semanalmente para limpiar productos obsoletos
3. **Webhook Dedicado**: Usa un canal/webhook dedicado debido al volumen
4. **Delay Apropiado**: El delay de 2.5s es generalmente adecuado
5. **Monitoreo de DB**: Revisa el tamaño de `bold.db` periódicamente

## Limitaciones

- **Páginas Limitadas**: Solo escanea las primeras 5 páginas (250 productos)
- **Free Proxies**: Son lentos y poco confiables
- **Stock Level**: Muestra cantidad pero no tamaño específico
- **Sin Filtrado**: No tiene sistema de keywords como SNKRS monitor

## Mejoras Futuras Sugeridas

- Sistema de filtrado por keywords
- Configuración de número de páginas
- Soporte para proxies de pago
- Dashboard web para visualizar la DB
- Sistema de alertas por marca específica

## Soporte

Para problemas o preguntas:
- Verifica que `config.py` esté correctamente configurado
- Asegúrate de que todas las dependencias estén instaladas
- Revisa `bold.db` para verificar qué productos están trackeados
- Contacta al equipo de Rebel Notify para soporte adicional
