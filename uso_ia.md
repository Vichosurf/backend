<p align="center">
	<img src="mi_proyecto_web/static/imagenes/Corporación_Instituto_Profesional_Inacap.svg.webp" alt="Logo INACAP" width="220">
</p>

# Uso de IA

## Parte 1: Registro de consultas

### Consulta 1: estructura Django y rutas
- **Prompt:** "Organiza un proyecto Django para un catálogo de ferretería sin base de datos: registra la aplicación, configura templates y static, conecta las URLs con `include`, crea rutas con `name` y agrega una vista de listado y otra de detalle por ID con respuesta 404."
- **Resumen de la respuesta:** Propuso organizar el proyecto, conectar las URLs y manejar productos inexistentes.
- **Uso y adaptación:** Usé la estructura para conectar las vistas y las rutas.

### Consulta 2: datos JSON y lógica de la vista
- **Prompt:** "Genera 40 productos de ferretería en JSON con `id`, `nombre`, `categoria`, `precio` y `stock`; incluye productos sin stock y muestra cómo cargarlos en una vista, calcular el total y contar los disponibles."
- **Resumen de la respuesta:** Entregó un listado JSON de productos y una forma de cargarlo en la vista.
- **Uso y adaptación:** Revisé los registros y agregué el resumen del catálogo.

### Consulta 3: templates, static e imágenes por producto
- **Prompt:** "¿Cómo puedo colocar imágenes de productos dentro de cards en templates de Django?"
- **Resumen de la respuesta:** Indicó cargar archivos estáticos y asociarlos a cada producto.
- **Uso y adaptación:** Coloqué las imágenes dentro de las cards del catálogo usando la carpeta `static/imagenes`.

### Consulta 4: revisión y trazabilidad de la entrega
- **Prompt:** "Revisa un proyecto Django de catálogo contra una rúbrica ES1: funcionamiento, requirements.txt, `.gitignore`, 40 productos, rutas, imágenes estáticas, `uso_ia.md` y cinco commits por etapa; indica errores y cómo validarlos."
- **Resumen de la respuesta:** Propuso comprobar Django, las rutas y el historial Git.
- **Uso y adaptación:** Ejecuté las comprobaciones principales del proyecto.

### Consulta 5: usuarios y pseudocompra
- **Prompt:** "¿Cómo puedo agregar usuarios y simular una compra solicitando la cantidad de productos?"
- **Resumen de la respuesta:** Propuso usar la autenticación de Django y validar el stock antes de descontarlo.
- **Uso y adaptación:** Incorporé el acceso de usuarios y la pseudocompra con validación de stock.

### Consulta 6: administración de productos
- **Prompt:** "Permite que un administrador modifique el stock y el precio de los productos desde Django Admin y personaliza el panel como FerroCasa (Admin)."
- **Resumen de la respuesta:** Indicó registrar el producto en Django Admin y permitir la edición de precio y stock.
- **Uso y adaptación:** Dejé ambos campos editables para el administrador.

## Parte 2: Explicación personal del proceso

Usé la IA como apoyo, pero revisé cada parte antes de incorporarla al proyecto.
Primero le pedí una estructura básica para entender cómo organizar Django.
Después le solicité un listado de 40 productos de ferretería en formato JSON.
Revisé los nombres, las categorías, los precios y el stock de esos productos.
También pedí una idea para diseñar los templates y adapté los colores y estilos.
La interfaz quedó separada en `base.html`, `inicio.html`, `lista.html` y `detalle.html`.
Para las imágenes, relacioné cada archivo con el ID del producto.
Agregué el resumen del catálogo y el aviso visual para los productos sin stock.
Después incorporé registro e inicio de sesión usando las herramientas de Django.
La pseudocompra pide una cantidad y comprueba que no supere el stock disponible.
También configuré el panel de administración para modificar precios y existencias.
Tuve que corregir algunas rutas de imágenes y probar el comportamiento de los botones.
Probé el detalle con un ID válido y con otro que no existe para revisar el error 404.
Ejecuté `manage.py check` y las pruebas automáticas del proyecto.
La IA me sirvió como orientación, pero tuve que leer, probar y adaptar el código.
Así entendí mejor cómo se conectan las vistas, los modelos, las URLs y los templates.