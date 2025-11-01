# Nike SKU Monitor (nike.cl)

Monitor avanzado de disponibilidad de productos para Nike Chile (nike.cl) basado en SKUs específicos. Este monitor utiliza tecnología Helheim/Bifrost para bypasear protecciones anti-bot y detectar cuando productos vuelven a estar disponibles.

## Descripción

Este es un monitor especializado para Nike Chile que utiliza cloudflare bypass (Helheim) y técnicas avanzadas de request handling para monitorear SKUs específicos. A diferencia de los monitores de Bold/MoreDrops, este monitor trabaja directamente con la API de VTEX de Nike y puede detectar disponibilidad incluso con protecciones activas.

## Cómo Funciona

1. **Inicialización Avanzada**:
   - Configura cloudscraper con Helheim para bypass de protecciones
   - Establece fingerprinting de navegador realista
   - Configura Bifrost para TLS fingerprinting

2. **Sistema de Sesiones**:
   - Crea sesiones persistentes con headers realistas
   - Maneja cookies y tokens automáticamente
   - Implementa retry logic con backoff exponencial

3. **Monitoreo de Productos**:
   - Intenta agregar el producto al carrito vía API de VTEX
   - Parsea respuesta XML para verificar disponibilidad
   - Detecta tanto productos cargados como no cargados

4. **Detección de Stock**:
   - Verifica el campo `availability` en la respuesta
   - Distingue entre "available", "unavailable", y producto no cargado

5. **Notificación Inteligente**:
   - Envía webhook a Discord con información detallada
   - Incluye enlace directo ATC (Add To Cart)
   - Previene notificaciones duplicadas con sistema de cooldown

6. **Manejo de Errores**:
   - Rotación automática de proxies en caso de bloqueo
   - Reinicio de sesión en caso de timeout
   - Manejo de errores de Bifrost y Helheim

## Requisitos

### Software
- Python 3.9 (requerido por Helheim)
- Windows x86_64 (requerido por Bifrost DLL)
- Dependencias listadas en archivos locales

### Archivos Especiales
- `helheim-0.8.5-py39-windows.x86_64.tar.gz` - Biblioteca de bypass
- `bifrost-0.0.4.1-windows.x86_64.dll` - TLS fingerprinting DLL

### Servicios
- Helheim API Key (incluida en el código: `e9efa3e3-d06f-4bbf-a7d6-e98e6fbdd2b3`)
- Webhook de Discord
- Proxies de alta calidad (residenciales recomendados)

## Instalación

1. **Requisitos de Sistema**:
```bash
# Verifica que tienes Python 3.9
python --version  # Debe ser 3.9.x
```

2. **Instala Helheim**:
```bash
cd nike-sku
pip install helheim-0.8.5-py39-windows.x86_64.tar.gz
```

3. **Instala otras dependencias**:
```bash
pip install cloudscraper
pip install xmltodict
pip install discord-webhook
pip install bcolors
pip install termcolor
```

4. **Verifica que Bifrost DLL esté presente**:
```bash
ls bifrost-0.0.4.1-windows.x86_64.dll
```

5. **Configura los archivos necesarios** (ver sección de Configuración)

## Configuración

### settings.json

Crea el archivo `settings.json` con la siguiente estructura:

```json
{
  "webhook_url": [
    "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
  ],
  "fail_webhook_url": "https://discord.com/api/webhooks/YOUR_FAIL_WEBHOOK_ID/YOUR_FAIL_WEBHOOK_TOKEN",
  "delay": 3000
}
```

**Parámetros:**
- `webhook_url`: Array de webhooks de Discord para notificaciones de stock (puedes tener múltiples)
- `fail_webhook_url`: Webhook para notificar errores críticos (sin proxies, etc.)
- `delay`: Delay entre requests en milisegundos (3000 = 3 segundos, recomendado para evitar rate limits)

### skus.txt

Lista de SKUs de Nike a monitorear, uno por línea:

```
13557734
13557735
13557736
```

**Cómo obtener SKUs:**
1. Ve al producto en nike.cl
2. Abre DevTools (F12) > Network
3. Busca el request a `/checkout/cart/add`
4. El parámetro `sku` es lo que necesitas

**Ejemplo:** Para `https://www.nike.cl/dunk-low-retro/p`, inspecciona la talla que quieres y captura el SKU.

### proxies.txt

Lista de proxies en formato `IP:PORT:USERNAME:PASSWORD`, uno por línea:

```
192.168.1.1:8080:username:password
192.168.1.2:8080:username:password
```

**IMPORTANTE:**
- Debes tener AL MENOS tantos proxies como SKUs
- Se recomienda usar proxies residenciales para Nike
- Proxies datacenter pueden ser bloqueados rápidamente
- La calidad del proxy es CRÍTICA para este monitor

### Actualizar ruta de Bifrost

**CRÍTICO:** Edita la línea 313 en `sku_monitor.py` con la ruta correcta de la DLL:

```python
helheim.bifrost(self.s, 'C:\\ruta\\completa\\a\\bifrost-0.0.4.1-windows.x86_64.dll')
```

Reemplaza con la ruta absoluta donde está tu DLL.

## Uso

1. **Configura todos los archivos**:
   - `settings.json` con tus webhooks y delay
   - `skus.txt` con los SKUs a monitorear
   - `proxies.txt` con proxies de calidad
   - Actualiza la ruta de Bifrost en el código

2. **Ejecuta el monitor**:
```bash
python sku_monitor.py
```

3. **Logs esperados**:
```
[11-01-2025 14:30:45] - [1] - Checking for valid alert...
[11-01-2025 14:30:46] - [1] - No stock (unloaded).
[11-01-2025 14:30:49] - [1] - No stock (loaded).
```

4. **Cuando encuentra stock**:
```
[11-01-2025 14:35:22] - [1] - Found product for 13557734!
[11-01-2025 14:35:22] - Payload delivered successfully, code 200.
```

5. **Notificación de Discord incluye**:
   - Nombre del producto
   - Imagen del producto
   - SKU específico
   - Precio
   - Talla
   - Enlace directo ATC (Add To Cart)
   - Estado de stock

## Estructura de Archivos

```
nike-sku/
├── sku_monitor.py                              # Script principal
├── _utils.py                                   # Utilidades (si existe)
├── settings.json                               # Configuración
├── skus.txt                                    # Lista de SKUs
├── proxies.txt                                 # Lista de proxies
├── helheim-0.8.5-py39-windows.x86_64.tar.gz   # Biblioteca Helheim
├── bifrost-0.0.4.1-windows.x86_64.dll         # DLL de Bifrost
└── README.md                                   # Esta documentación
```

## Troubleshooting

### Error: "No proxies to rotate to!"
**Problema:** Se quedaron sin proxies disponibles.

**Solución:**
- Agrega más proxies de alta calidad a `proxies.txt`
- Reduce el número de SKUs en `skus.txt`
- Usa proxies residenciales en lugar de datacenter
- Aumenta el delay en `settings.json`

### Error: "Request got timed out"
**Problema:** Bifrost/Helheim no puede completar el request.

**Solución:**
- Verifica que la ruta de Bifrost DLL sea correcta
- Prueba con un proxy diferente
- Aumenta el timeout en el código
- Verifica tu conexión a internet

### Error: "HelheimBifrost exception"
**Problema:** El sistema de bypass falló.

**Solución:**
- Verifica que Helheim esté instalado correctamente
- Asegúrate de que la API key de Helheim sea válida
- Rota a un proxy diferente
- Reinicia el monitor

### Error: "Access Denied (403/428)"
**Problema:** Nike bloqueó el request.

**Solución:**
- Usa mejores proxies (residenciales)
- Aumenta el delay entre requests
- Verifica que los headers sean correctos
- El proxy puede estar quemado - rótalo

### "No stock" constantemente pero el producto está disponible
**Problema:** Detección incorrecta o SKU incorrecto.

**Solución:**
- Verifica que el SKU sea correcto
- Verifica manualmente agregando al carrito
- El producto puede estar disponible pero el SKU específico no
- Captura el SKU nuevamente desde el sitio web

### Payload no se entrega a Discord
**Problema:** Webhook incorrecto o rate limit.

**Solución:**
- Verifica la URL del webhook
- Discord tiene límite de 30 webhooks/minuto
- Prueba el webhook manualmente
- Verifica que el canal exista

### DLL no encontrada o error al cargar
**Problema:** Ruta incorrecta de Bifrost o arquitectura incompatible.

**Solución:**
- Verifica que la ruta sea absoluta y correcta
- Asegúrate de estar en Windows x86_64
- Verifica que el archivo DLL no esté corrupto
- Reemplaza con una copia fresca de la DLL

## Notas Técnicas

### Helheim y Bifrost
- **Helheim**: Resuelve challenges de Cloudflare y otros anti-bots
- **Bifrost**: Proporciona TLS fingerprinting realista
- Ambos son CRÍTICOS para que el monitor funcione

### Sistema de Sesiones
- Cada tarea tiene su propia sesión independiente
- Las sesiones incluyen retry logic automático
- Los headers imitan Chrome 101 en Windows 10

### Multi-threading
- Cada SKU se monitorea en un thread separado
- Los threads comparten un lock para prevenir race conditions
- Sistema de notificación global previene duplicados

### API de Nike (VTEX)
- Nike Chile usa VTEX como backend
- Las respuestas son en formato XML
- El campo `availability` determina stock
- El sistema ATC (Add To Cart) usa parámetros específicos

### Delay y Rate Limiting
- Nike tiene rate limiting agresivo
- Se recomienda mínimo 3000ms (3 segundos) de delay
- Delays muy bajos pueden resultar en bloqueos permanentes

## Seguridad y Ética

- Este monitor es para USO EDUCACIONAL y PERSONAL
- NO uses este monitor para reventas masivas
- Respeta los términos de servicio de Nike
- NO compartas la API key de Helheim públicamente
- Usa delays razonables para no sobrecargar el servidor

## Limitaciones Conocidas

1. **Solo Windows**: Bifrost requiere Windows x86_64
2. **Python 3.9**: Helheim requiere específicamente Python 3.9
3. **Proxies Requeridos**: Nike bloqueará IPs rápidamente sin proxies
4. **Rate Limiting**: Delays muy bajos resultan en bloqueos
5. **SKUs Específicos**: Debes conocer el SKU exacto de la talla que quieres

## Soporte

Para problemas o preguntas sobre este monitor específico:
- Verifica que todos los requisitos estén instalados
- Revisa los logs para mensajes de error específicos
- Asegúrate de que Helheim y Bifrost estén configurados correctamente
- Contacta al equipo de Rebel Notify para soporte adicional

## Diferencias con Otros Monitores

- **vs Bold/MoreDrops**: Usa Helheim/Bifrost, más complejo pero más poderoso
- **vs SNKRS**: Monitor de SKUs específicos vs monitor general de releases
- **API**: VTEX (Nike) vs Hybris (Bold/MoreDrops)
- **Protecciones**: Nike tiene protecciones más fuertes que requieren bypass
