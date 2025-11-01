# BOLD RESTOCK SKU Monitor

Monitor de restocks para productos específicos en Bold.cl basado en SKU y talla. Este monitor detecta cuando una talla específica de un producto vuelve a estar disponible y envía notificaciones automáticas a Discord.

## Descripción

Este monitor utiliza el método de "add to cart" para verificar la disponibilidad de productos en Bold.cl. Intenta agregar productos al carrito basándose en el SKU del producto y la talla específica, lo que permite detectar restocks en tiempo real.

## Cómo Funciona

1. **Inicialización**: El monitor carga la configuración desde `settings.json` y lee los PIDs con tallas desde `pids.txt`
2. **Inicio de Sesión**: Para cada PID+talla, se crea una sesión y se obtiene el token CSRF necesario
3. **Monitoreo**: El bot intenta constantemente agregar el producto al carrito
4. **Detección**: Cuando el producto se agrega exitosamente, significa que está disponible
5. **Notificación**: Se envía un webhook a Discord con la información del producto
6. **Cooldown**: Después de notificar, espera 30 segundos antes de volver a notificar el mismo producto

El monitor utiliza multi-threading para monitorear múltiples productos simultáneamente.

## Requisitos

- Python 3.7 o superior
- Dependencias listadas en `requirements.txt`
- Webhook de Discord
- Proxies (opcional, recomendado para múltiples tareas)

## Instalación

1. Clona el repositorio:
```bash
cd bold-restock-sku
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
- `webhook_url`: URL del webhook de Discord para recibir notificaciones
- `log_mode`: `true` para guardar logs detallados en la carpeta `logs/`, `false` para desactivar
- `localhost`: `true` para ejecutar sin proxies (modo local), `false` para usar proxies

### pids.txt

Lista de productos a monitorear en formato `SKU:TALLA`, uno por línea:

```
NIDH6927161:9
NIDH6927161:10.5
NIDH6927161:8
```

**Formato del SKU:**
- SKU completo del producto en Bold.cl
- Dos puntos `:`
- Talla en formato US (7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13)

### proxies.txt (Opcional)

Lista de proxies en formato `IP:PORT:USERNAME:PASSWORD`, uno por línea:

```
192.168.1.1:8080:username:password
192.168.1.2:8080:username:password
```

**Nota:** Si `localhost` está en `true`, los proxies no se utilizarán. Asegúrate de tener al menos tantos proxies como PIDs si `localhost` está en `false`.

## Uso

1. Configura todos los archivos necesarios (`settings.json`, `pids.txt`, `proxies.txt`)

2. Crea la carpeta `logs` si no existe:
```bash
mkdir logs
```

3. Ejecuta el monitor:
```bash
python bot.py
```

4. El monitor comenzará a verificar la disponibilidad de cada producto y mostrará logs en la consola:
```
[11-01-2025 14:30:45] - [1] - [Bold Monitor] - (NIDH6927161070) - Starting session...
[11-01-2025 14:30:46] - [1] - [Bold Monitor] - (NIDH6927161070) - Size not available.
```

5. Cuando un producto esté disponible, recibirás una notificación en Discord con:
   - Nombre del producto
   - Imagen del producto
   - PID
   - Talla con enlace directo
   - Timestamp

## Estructura de Archivos

```
bold-restock-sku/
├── bot.py                 # Script principal del monitor
├── _utils.py             # Utilidades (configuración de proxies)
├── bcolors.py            # Colores para logs en consola
├── settings.json         # Configuración principal
├── pids.txt              # Lista de productos a monitorear
├── proxies.txt           # Lista de proxies (opcional)
├── requirements.txt      # Dependencias de Python
└── logs/                 # Carpeta para logs (se crea automáticamente)
```

## Troubleshooting

### Error: "Not enough proxies for pids"
**Problema:** No hay suficientes proxies para el número de PIDs configurados.

**Solución:**
- Agrega más proxies a `proxies.txt`, o
- Reduce el número de PIDs en `pids.txt`, o
- Cambia `localhost` a `true` en `settings.json`

### Error: "Product page not found"
**Problema:** El SKU del producto no es válido o el producto no existe.

**Solución:**
- Verifica que el SKU esté correcto
- Verifica que la talla esté en formato US correcto
- Visita manualmente https://bold.cl/p/[SKU+TALLA] para confirmar que existe

### Error: "Invalid proxy"
**Problema:** El formato del proxy es incorrecto.

**Solución:** Asegúrate de que cada proxy siga el formato `IP:PORT:USERNAME:PASSWORD`

### El monitor no detecta productos disponibles
**Problema:** Puede haber problemas de rate limiting o bloqueos.

**Solución:**
- Aumenta el delay entre requests modificando el `time.sleep(3)` en el código
- Usa proxies residenciales de mejor calidad
- Reduce el número de tareas simultáneas

### Los logs no se guardan
**Problema:** La carpeta `logs/` no existe o no hay permisos de escritura.

**Solución:**
- Crea la carpeta manualmente: `mkdir logs`
- Verifica los permisos de escritura en la carpeta

### Webhook de Discord no funciona
**Problema:** URL incorrecta o webhook deshabilitado.

**Solución:**
- Verifica que la URL del webhook sea correcta
- Prueba el webhook manualmente en https://discord.com/developers/docs/resources/webhook
- Asegúrate de que el canal de Discord aún existe

## Notas Adicionales

- El monitor vacía el carrito automáticamente después de detectar disponibilidad
- Cada tarea espera 2 segundos antes de iniciar para evitar sobrecarga
- El sistema de notificación tiene un cooldown de 30 segundos para evitar spam
- Los códigos de talla se convierten automáticamente (ejemplo: 9 → 090)

## Soporte

Para problemas o preguntas, contacta al equipo de Rebel Notify.
