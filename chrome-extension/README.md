# Rebel Autofill - Chrome Extension (DEV VERSION)

Extensión de Chrome para automatización de checkout en Bold.cl y MoreDrops.cl. Incluye funcionalidades de auto-fill de información, selección automática de tallas, monitoreo de restocks, y notificaciones de sonido para alertas de carrito.

<img src="./extension.png" width="300" alt="Rebel Autofill Extension">

## Descripción

Esta extensión de Chrome está diseñada para facilitar y acelerar el proceso de compra en sitios de sneakers chilenos (Bold y MoreDrops). Automatiza tareas repetitivas como llenar formularios, seleccionar métodos de pago, y detectar cambios en la disponibilidad de productos.

## Características Principales

### 1. Autofill de Información Personal
- Email y contraseña de cuenta
- Nombre completo
- RUT
- Información de tarjeta (número, CVV, fecha de vencimiento, cuotas)

### 2. Automatización de Checkout
- Auto-login en páginas de checkout
- Selección automática de dirección de envío
- Llenado de formulario de pickup
- Selección automática de método de entrega
- Selección de método de pago (crédito/débito)
- Autofill de datos de tarjeta
- Navegación automática entre pasos del checkout

### 3. Monitoreo de Productos
- Detección de cambios en productos (restocks)
- Monitoreo automático de tallas específicas
- Add-to-cart automático cuando está disponible
- Notificaciones de sonido cuando se agrega al carrito

### 4. Configuración Flexible
- Panel de configuración completo
- Activar/desactivar funciones individuales
- Configuración de delays personalizados
- Selección de tallas específicas
- Enlaces directos a productos

## Requisitos

- Google Chrome (versión 88 o superior)
- Cuenta activa en Bold.cl y/o MoreDrops.cl
- Información de pago válida (para autofill)

## Instalación

### Método 1: Modo Desarrollador (Recomendado para DEV VERSION)

1. Abre Chrome y navega a `chrome://extensions/`

2. Activa el "Modo de desarrollador" (Developer mode) en la esquina superior derecha

3. Haz clic en "Cargar extensión sin empaquetar" (Load unpacked)

4. Selecciona la carpeta `chrome-extension`

5. La extensión aparecerá con el ícono de Rebel en la barra de herramientas

### Método 2: Desempaquetar (Para distribución)

1. Empaqueta la carpeta `chrome-extension` en un archivo .crx
2. Arrastra el archivo .crx a `chrome://extensions/`
3. Confirma la instalación

## Configuración Inicial

### 1. Abre la Extensión

Haz clic en el ícono de Rebel en la barra de herramientas de Chrome.

### 2. Configurar Información Personal

Ve a la pestaña de Settings (ícono de engranaje) y llena:

```
Account Information:
- Account Email: tu@email.com
- Account Password: tu_contraseña

Personal Information:
- Full Name: Juan Pérez
- RUT: 12345678-9

Card Information:
- Card Number: 1234567890123456
- Expiry Month: 01
- Expiry Year: 2025
- Cuotas: 3
- CVV: 123
```

Haz clic en "Save" para guardar.

### 3. Configurar Opciones de Monitor

En la pestaña principal, configura:

```
Product Link: [URL del producto que quieres monitorear]
Size: [Selecciona la talla deseada, o "default" para cualquiera]
Delay (ms): 1000 (recomendado para evitar rate limiting)
Payment Method: Credit o Debit
```

### 4. Activar/Desactivar Funciones

Usa los switches para controlar qué funciones están activas:

- **ATC (Add To Cart)**: Agregar automáticamente al carrito
- **Size Select**: Selección automática de talla en página de producto
- **Checkout**: Automatización de proceso de checkout
- **Restock**: Monitoreo de restocks en páginas de producto
- **Sounds**: Notificaciones de sonido cuando se agrega al carrito

Haz clic en "Save" para guardar cambios.

## Uso

### Modo Manual (Checkout Automation)

1. Navega manualmente al producto en Bold o MoreDrops
2. Agrega el producto al carrito
3. Procede al checkout
4. La extensión llenará automáticamente todos los formularios según tu configuración
5. Solo necesitas revisar y confirmar el pedido final

### Modo Automático (Restock Monitor)

1. Configura el "Product Link" con la URL del producto deseado
2. Selecciona la talla en "Size"
3. Activa "ATC", "Size Select", "Restock", y "Sounds"
4. Haz clic en "Start Task" para abrir el producto
5. La extensión monitoreará automáticamente y:
   - Detectará cuando la talla esté disponible
   - Agregará al carrito automáticamente
   - Reproducirá un sonido de alerta
   - Iniciará el checkout automáticamente si está activado

### Funciones de Un Clic

- **"All ON"**: Activa todas las funciones
- **"All OFF"**: Desactiva todas las funciones
- **"Start Task"**: Abre el producto configurado en Product Link

## Estructura de Archivos

```
chrome-extension/
├── manifest.json                 # Configuración de la extensión
├── index.html                    # UI del popup
├── index.css / second.css        # Estilos
├── index.js                      # Lógica del popup
├── background.js                 # Service worker
├── handler.js                    # Handler para MoreDrops
├── oauth.js                      # Autenticación OAuth (deshabilitado)
├── sound.mp3                     # Sonido de notificación
├── imgs/                         # Imágenes e íconos
└── scripts/                      # Content scripts
    ├── common.js                 # Funciones compartidas
    ├── detectChange.js           # Detector de cambios en Bold
    ├── item.js                   # Handler de página de producto (MoreDrops)
    ├── boldItem.js               # Handler de página de producto (Bold)
    ├── cart.js                   # Automatización de carrito
    ├── login.js                  # Auto-login
    └── checkout/
        ├── shipping.js           # Formulario de dirección
        ├── pickup.js             # Formulario de pickup
        ├── delivery.js           # Selección de método de entrega
        ├── payment.js            # Selección de método de pago
        ├── method.js             # Autofill de tarjeta
        └── summary.js            # Página de resumen final
```

## Content Scripts

La extensión inyecta scripts específicos en diferentes páginas:

### Bold.cl
- **Detector de Cambios**: `detectChange.js` + `common.js`
- **Páginas de Producto**: `boldItem.js`
- **Login**: `login.js` + `common.js`
- **Checkout**: Scripts específicos de checkout

### MoreDrops.cl
- **Handler General**: `handler.js`
- **Páginas de Producto**: `item.js`
- **Carrito**: `cart.js` + `common.js`
- **Login**: `login.js` + `common.js`
- **Checkout**: Scripts específicos de checkout

## Funcionalidades Detalladas

### Auto-Login (`login.js`)
```javascript
// Se activa en: /login/checkout
// Llena email y contraseña
// Hace clic en el botón de login
// Espera configuración antes de ejecutar
```

### Size Selection (`item.js` / `boldItem.js`)
```javascript
// Se activa en páginas de producto
// Espera a que la página cargue
// Busca el selector de talla configurado
// Hace clic automáticamente
// Intenta agregar al carrito si ATC está activado
```

### Add To Cart Automation
```javascript
// Encuentra el botón de agregar al carrito
// Hace clic automáticamente
// Reproduce sonido si está activado
// Redirige al checkout si está configurado
```

### Checkout Automation
- **Shipping**: Llena dirección de envío desde configuración
- **Pickup**: Llena datos de pickup si aplica
- **Delivery**: Selecciona método de entrega automáticamente
- **Payment**: Selecciona crédito o débito según configuración
- **Method**: Llena número de tarjeta, CVV, fecha, y cuotas
- **Summary**: Espera confirmación manual (no hace clic en "Comprar")

### Restock Detection (`detectChange.js`)
```javascript
// Monitorea cambios en el DOM de la página de producto
// Detecta cuando botones cambian de "Sin stock" a "Agregar"
// Ejecuta ATC automáticamente cuando detecta disponibilidad
// Usa MutationObserver para detección en tiempo real
```

## Almacenamiento de Datos

La extensión usa `chrome.storage.local` para guardar:

```javascript
{
  "info": {
    accountemail: String,
    accountpass: String,
    fullname: String,
    cardnumber: String,
    expirymonth: String,
    expiryyear: String,
    cuotas: String,
    cvv: String,
    rut: String
  },
  "data": {
    link: String,
    size: String,
    delay: Number,
    payment: 'credit' | 'debit',
    atc: 'on' | 'off',
    sizeselect: 'on' | 'off',
    checkoutselect: 'on' | 'off',
    restockselect: 'on' | 'off',
    soundselect: 'on' | 'off'
  },
  "lastProduct": String
}
```

## Troubleshooting

### La extensión no aparece en Chrome
**Problema:** Error al cargar la extensión.

**Solución:**
- Verifica que todos los archivos estén presentes
- Revisa que `manifest.json` sea válido
- Asegúrate de que el modo desarrollador esté activado
- Revisa la consola de extensiones para errores

### Autofill no funciona
**Problema:** Los campos no se llenan automáticamente.

**Solución:**
- Verifica que hayas guardado tu información en Settings
- Abre las DevTools y revisa la consola para errores
- Los selectores de HTML pueden haber cambiado - contacta soporte
- Asegúrate de que la función "Checkout" esté activada

### Size selection no funciona
**Problema:** No selecciona la talla automáticamente.

**Solución:**
- Verifica que "Size Select" esté activado
- Asegúrate de haber seleccionado una talla específica (no "default")
- El producto debe tener esa talla disponible
- Revisa la consola del navegador para errores

### Restock detection no funciona
**Problema:** No detecta cuando el producto vuelve a stock.

**Solución:**
- Verifica que "Restock" esté activado
- Asegúrate de estar en la página del producto (no en búsqueda)
- El delay puede ser muy alto - intenta reducirlo
- Algunos productos pueden no ser compatibles

### El sonido no se reproduce
**Problema:** No hay notificación de sonido.

**Solución:**
- Verifica que "Sounds" esté activado
- Asegúrate de que Chrome tenga permiso para reproducir audio
- Verifica que `sound.mp3` exista en la carpeta
- Revisa la configuración de audio del sistema

### OAuth/Discord no funciona
**Problema:** La autenticación de Discord falla.

**Solución:**
- **Esta función está DESHABILITADA** en el código actual
- Las líneas de OAuth están comentadas en `index.js`
- Para habilitar, necesitas configurar CLIENT_ID y CLIENT_SECRET
- Reemplaza los valores placeholder en el código

### La extensión es lenta
**Problema:** Hay delays significativos en la automatización.

**Solución:**
- Verifica el valor de "Delay" en la configuración
- Valores muy bajos (<500ms) pueden causar problemas
- 1000ms (1 segundo) es el valor recomendado
- Valores muy altos (>5000ms) harán todo más lento

### Error: "Cannot read property of undefined"
**Problema:** Selector de HTML no encontrado.

**Solución:**
- Bold/MoreDrops pueden haber cambiado su estructura HTML
- Inspecciona la página con DevTools para ver los cambios
- Los content scripts pueden necesitar actualización
- Contacta soporte con detalles del error

## Seguridad y Privacidad

### Almacenamiento Local
- **Todos los datos se guardan localmente** en `chrome.storage.local`
- **No se envía información a servidores externos**
- Los datos de tarjeta se guardan en texto plano (considera los riesgos)

### Permisos de la Extensión
```json
"permissions": [
  "storage",      // Para guardar configuración
  "background"    // Para service worker
]
```

### Advertencias de Seguridad
- **Información de Tarjeta**: Se guarda en texto plano en tu navegador
- **Contraseñas**: Se guardan sin encriptar en storage local
- **Uso en Computadoras Compartidas**: NO recomendado
- **Riesgo de Malware**: Solo instala desde fuentes confiables

## Limitaciones Conocidas

1. **Manifest V2**: Esta extensión usa Manifest V2 (será deprecado en 2024)
2. **Chrome Only**: No compatible con Firefox u otros navegadores
3. **Sitios Específicos**: Solo funciona en Bold.cl y MoreDrops.cl
4. **Sin Encriptación**: Los datos sensibles no están encriptados
5. **OAuth Deshabilitado**: La funcionalidad de Discord está comentada
6. **Captcha**: No puede resolver captchas automáticamente
7. **Queue-It**: No puede bypassear sistemas de cola
8. **Cambios de Sitio**: Vulnerable a cambios en HTML de Bold/MoreDrops

## Actualizaciones Futuras Sugeridas

- Migrar a Manifest V3
- Encriptación de datos sensibles
- Soporte para más sitios chilenos
- Sistema de configuración de perfiles múltiples
- Integración con Discord funcional
- Dashboard de estadísticas
- Modo incógnito mejorado
- Auto-actualización de selectores HTML

## Desarrollo

### Estructura de Content Scripts

Cada content script tiene acceso a:
- DOM de la página
- `chrome.storage` API
- `chrome.runtime` API para mensajería

### Añadir Soporte para Nueva Página

1. Crea un nuevo script en `/scripts/`
2. Agrega el match pattern en `manifest.json`:
```json
{
  "matches": ["https://sitio.cl/pagina/*"],
  "js": ["./scripts/tu-script.js"],
  "run_at": "document_start"
}
```

### Debugging

1. **Popup**: Click derecho en el ícono > Inspeccionar popup
2. **Content Scripts**: F12 en la página > Console tab
3. **Background**: `chrome://extensions/` > Inspeccionar > Background page
4. **Storage**: Chrome DevTools > Application > Storage > Local Storage

### Common.js Functions

El archivo `common.js` proporciona funciones útiles:
- Espera por configuración
- Helpers de storage
- Funciones de delay
- Envío de mensajes al background

## Términos de Uso

- Esta extensión es para **USO PERSONAL** únicamente
- NO la uses para reventas masivas o actividades comerciales
- Respeta los términos de servicio de Bold y MoreDrops
- El uso excesivo puede resultar en bloqueo de cuenta
- Los desarrolladores no se hacen responsables por mal uso

## Soporte

Para problemas o preguntas:
- Revisa la consola del navegador para errores
- Verifica que todos los archivos estén presentes
- Asegúrate de que la configuración esté guardada correctamente
- Los sitios pueden cambiar - la extensión puede requerir actualización

## ⚠️ Importante

Esta extensión ha sido **migrada a Manifest V3** para funcionar en Chrome moderno.

**Nota sobre funcionalidad:**
- La extensión ahora carga en Chrome actual
- Sin embargo, los sitios web (Bold.cl, MoreDrops.cl) probablemente cambiaron sus estructuras desde 2020-2023
- Los selectores CSS y flujos de checkout pueden estar desactualizados
- Úsala bajo tu propio riesgo para fines educativos

El código original fue creado entre 2020-2023 y se mantiene como referencia del proyecto Rebel Notify.

## Créditos

- **Desarrollado por**: srdanirz
- **Versión**: 3.1 (Manifest V3)
- **Período original**: 2020-2023
- **Sitios target**: Bold.cl, MoreDrops.cl

## Licencia

MIT License - Ver LICENSE en la raíz del repositorio.
