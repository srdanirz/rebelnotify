# MOREDROPS RESTOCK SKU Monitor

Monitor de restocks para productos específicos en MoreDrops.cl basado en SKU y talla. Este monitor detecta cuando una talla específica de un producto vuelve a estar disponible y envía notificaciones automáticas a Discord.

## Descripción

Este monitor utiliza el método de "add to cart" para verificar la disponibilidad de productos en MoreDrops.cl. Funciona de manera similar al monitor de Bold, pero adaptado específicamente para la plataforma MoreDrops. Intenta agregar productos al carrito basándose en el SKU del producto y la talla específica.

## Cómo Funciona

1. **Inicialización**: El monitor carga la configuración desde `settings.json` y lee los PIDs con tallas desde `pids.txt`
2. **Inicio de Sesión**: Para cada PID+talla, se crea una sesión y se obtiene el token CSRF necesario de MoreDrops
3. **Monitoreo Continuo**: El bot intenta constantemente agregar el producto al carrito
4. **Detección de Stock**: Cuando el producto se agrega exitosamente al carrito, significa que está disponible
5. **Notificación**: Se envía un webhook a Discord con la información detallada del producto
6. **Sistema de Cooldown**: Después de notificar, espera 30 segundos antes de volver a notificar el mismo producto
7. **Limpieza**: El carrito se vacía automáticamente después de cada detección

El monitor utiliza multi-threading para monitorear múltiples productos simultáneamente con delays controlados.

## Requisitos

- Python 3.7 o superior
- Dependencias listadas en `requirements.txt`
- Webhook de Discord válido
- Proxies (opcional, recomendado para múltiples tareas concurrentes)

## Instalación

1. Navega al directorio del proyecto:
```bash
cd moredrops-restock-sku
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura los archivos necesarios (ver sección de Configuración)

## Configuración

### settings.json

Crea o edita el archivo `settings.json` con la siguiente estructura:

```json
{
  "webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
  "log_mode": true,
  "localhost": true
}
```

**Parámetros:**
- `webhook_url`: URL del webhook de Discord para recibir notificaciones de restocks
- `log_mode`: `true` para guardar logs detallados en la carpeta `logs/`, `false` para desactivar logging
- `localhost`: `true` para ejecutar sin proxies (modo local/testing), `false` para usar proxies de producción

### pids.txt

Lista de productos a monitorear en formato `SKU:TALLA`, uno por línea:

```
NIDH6927161:9
NIDH6927161:10.5
NIDH6927161:8
```

**Formato del SKU:**
- SKU completo del producto en MoreDrops.cl (mismo formato que Bold)
- Dos puntos `:`
- Talla en formato US (7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13)

**Ejemplo de URL del producto:** `https://moredrops.cl/p/NIDH6927161090` (donde 090 es la talla 9)

### proxies.txt (Opcional)

Lista de proxies en formato `IP:PORT:USERNAME:PASSWORD`, uno por línea:

```
192.168.1.1:8080:username:password
192.168.1.2:8080:username:password
```

**Nota:** Si `localhost` está en `true`, los proxies no se utilizarán. Si `localhost` es `false`, asegúrate de tener al menos tantos proxies como PIDs.

## Uso

1. Configura todos los archivos necesarios (`settings.json`, `pids.txt`, `proxies.txt` si aplica)

2. Crea la carpeta `logs` si no existe:
```bash
mkdir logs
```

3. Ejecuta el monitor:
```bash
python moredropsrestock.py
```

4. El monitor comenzará a verificar la disponibilidad de cada producto:
```
[11-01-2025 14:30:45] - [1] - [Drops Monitor] - (NIDH6927161070) - Starting session...
[11-01-2025 14:30:46] - [1] - [Drops Monitor] - (NIDH6927161070) - Size not available.
[11-01-2025 14:30:49] - [1] - [Drops Monitor] - (NIDH6927161070) - Size not available.
```

5. Cuando un producto esté disponible, verás:
```
[11-01-2025 14:35:22] - [1] - [Drops Monitor] - (Air Jordan 1 Retro) - Size available.
[11-01-2025 14:35:22] - [1] - [Drops Monitor] - (Air Jordan 1 Retro) - Emptying cart...
```

6. Recibirás una notificación en Discord con:
   - Nombre del producto
   - Imagen del producto
   - PID
   - Talla con enlace directo al producto
   - Timestamp de detección

## Estructura de Archivos

```
moredrops-restock-sku/
├── moredropsrestock.py   # Script principal del monitor
├── _utils.py             # Utilidades (configuración de proxies)
├── settings.json         # Configuración principal
├── pids.txt              # Lista de productos a monitorear
├── proxies.txt           # Lista de proxies (opcional)
├── requirements.txt      # Dependencias de Python
└── logs/                 # Carpeta para logs (se crea automáticamente)
```

## Troubleshooting

### Error: "Not enough proxies for pids"
**Problema:** No hay suficientes proxies para el número de PIDs configurados cuando `localhost` es `false`.

**Solución:**
- Agrega más proxies a `proxies.txt`, o
- Reduce el número de PIDs en `pids.txt`, o
- Cambia `localhost` a `true` en `settings.json` para testing sin proxies

### Error: "Product page not found"
**Problema:** El SKU del producto no es válido o el producto no existe en MoreDrops.

**Solución:**
- Verifica que el SKU esté correcto y sea un producto de MoreDrops
- Verifica que la talla esté en formato US correcto (7-13)
- Visita manualmente `https://moredrops.cl/p/[SKU+CODIGO_TALLA]` para confirmar que existe
- Ejemplo: `https://moredrops.cl/p/NIDH6927161090` (para talla 9)

### Error: "Invalid proxy"
**Problema:** El formato del proxy es incorrecto.

**Solución:** Asegúrate de que cada proxy siga exactamente el formato `IP:PORT:USERNAME:PASSWORD`

### El monitor no detecta productos disponibles
**Problema:** Puede haber rate limiting, bloqueos de IP, o el producto realmente no está disponible.

**Solución:**
- Verifica manualmente que el producto esté disponible en MoreDrops
- Aumenta el delay entre requests (modifica `time.sleep(3)` a un valor mayor)
- Usa proxies residenciales de mejor calidad
- Reduce el número de tareas simultáneas
- Verifica que el CSRF token se esté obteniendo correctamente

### Los logs no se guardan
**Problema:** La carpeta `logs/` no existe o no hay permisos de escritura.

**Solución:**
- Crea la carpeta manualmente: `mkdir logs`
- En Windows: `md logs`
- Verifica los permisos de escritura en la carpeta

### Webhook de Discord no funciona
**Problema:** URL incorrecta, webhook deshabilitado, o límite de rate exceeded.

**Solución:**
- Verifica que la URL del webhook sea correcta y válida
- Prueba el webhook manualmente usando curl o Postman
- Asegúrate de que el canal de Discord aún existe y el webhook está activo
- Discord tiene límites de rate: máximo 30 webhooks por minuto

### Error de CSRF Token
**Problema:** El token CSRF no se puede obtener de la página.

**Solución:**
- Verifica tu conexión a internet
- Comprueba que MoreDrops.cl esté accesible
- Intenta con diferentes proxies si estás usando
- MoreDrops puede haber cambiado su estructura - contacta soporte

## Notas Adicionales

- El monitor vacía el carrito automáticamente después de detectar disponibilidad para evitar conflictos
- Cada tarea espera 2 segundos antes de iniciar para distribuir la carga
- El sistema de notificación tiene un cooldown de 30 segundos por producto para evitar spam
- Los códigos de talla se convierten automáticamente (ejemplo: 9 → 090, 10.5 → 105)
- El monitor maneja automáticamente errores 404 (producto no encontrado) y 500 (server error)
- Se recomienda usar proxies residenciales para evitar bloqueos en sesiones largas

## Diferencias con Bold Monitor

- **URL Base**: Usa `moredrops.cl` en lugar de `bold.cl`
- **Footer del Webhook**: Identifica como "Rebel Notify Drops Monitor"
- **Mismo Sistema de Tallas**: Compatible con el mismo formato de tallas que Bold
- **API Compatible**: Ambos sitios usan APIs similares de Hybris

## Soporte

Para problemas o preguntas, contacta al equipo de Rebel Notify.
