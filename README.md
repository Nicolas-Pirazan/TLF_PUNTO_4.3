# Analizador de Gramáticas

Este proyecto es una aplicación web desarrollada con Flask que permite definir gramáticas formales, generar árboles de derivación y verificar si una palabra pertenece al lenguaje generado por una gramática.

## Estructura del Proyecto

```
CODIGO FUENTE
├── app.py
├── static
│   └── css
│       └── styles.css
└── templates
    └── index.html
```

## Características

- **Definición de gramáticas:** Permite ingresar símbolos terminales, no terminales, seleccionar el símbolo inicial y agregar producciones.
- **Validación:** Verifica que la gramática contenga al menos 2 símbolos terminales, 3 no terminales, 3 producciones y un símbolo inicial con producciones asignadas.
- **Verificación de palabras:** Utiliza un algoritmo de búsqueda (BFS) para determinar si una palabra pertenece al lenguaje generado.
- **Generación de Árboles:** Crea un árbol general de derivación que se visualiza en la interfaz utilizando D3.js.
- **Interfaz de Usuario:** Diseño responsivo con Tailwind CSS y componentes interactivos con FontAwesome.

## Requisitos

- Python 3.x
- Flask (se puede instalar con `pip install Flask`)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone <URL-del-repositorio>
   ```

2. **Navegar a la carpeta del proyecto:**

   ```bash
   cd "c:\Users\nicol\OneDrive\Desktop\SEMESTRE VIII\FORMALES\CODIGOS\PUNTO_4.3_TALLER\CODIGO FUENTE"
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install Flask
   ```

## Ejecución

Para iniciar el servidor de Flask, ejecuta:

```bash
python app.py
```

Abre tu navegador y dirígete a [http://127.0.0.1:5000](http://127.0.0.1:5000) para usar la aplicación.

## Uso

1. **Definir la gramática:**  
   Ingresa los símbolos terminales y no terminales, selecciona el símbolo inicial y agrega las producciones.

2. **Crear la gramática:**  
   Al dar clic en "Crear Gramática", se valida la entrada y se almacena la gramática.

3. **Verificar palabras:**  
   Utiliza el módulo de verificación para comprobar si una palabra pertenece al lenguaje generado. Se visualizarán el árbol de derivación y el árbol general de la gramática.

## Contacto

Si tienes sugerencias o encuentras algún problema, puedes comunicarte con el autor o contribuir al repositorio.

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
