# Manual

En este documento se detalla paso a paso todo lo necesario para la **instalación y uso** del software desarrollado.

## Instalación

Requisitos:

| Software | Versión |
|--|--|
| Python | 3.6 en adelante |
| LlamaIndex | 0.10.18 |

Instalación de **Python**: [Descargar](https://www.python.org/downloads/)

Instalación de **LlamaIndex**: `pip install llama-index==0.10.18` 

> **Nota**: El comando `pip install llama-index==0.10.18` debe instalar todos los paquetes adicionales implicados en el uso de LlamaIndex para este proyecto, por ejemplo, el de **OpenAI**. Si existiese algún conflicto con los `imports`, resolver según las sugerencias del IDE.

## Uso

1. [Descargar](https://github.com/akalombi/BuroSimple/archive/refs/heads/main.zip) todo el contenido del directorio y crear una carpeta con el mismo, manteniendo la estructura de directorios y ficheros.

2. Abrir la carpeta con el IDE deseado.

3. Abrir `config.ini` y ajustar todos los parámetros necesarios. Por defecto, solo deberá introducirse la clave para la API de OpenAI y la consulta que quiera hacerse.

4. Ejecutar `Software_BuroSimple.py`. Los resultados serán mostrados por pantalla.

> **IMPORTANTE**: Este script recoge el proceso del RAG al completo, permitiendo también adaptarlo a un uso propio con cualquier base de conocimiento. Esto implica que puede ser lento, dado que lleva a cabo instrucciones semipesadas cuya ejecución no es necesaria para el lanzamiento de cada una de las consultas. Para aumentar la eficiencia, se recomienda la serialización del objeto `query_engine` a través de bibliotecas como **`Pickle`**, para así cargarlo y deserializarlo al principio de la tarea que quiera llevarse a cabo, estando de esta manera listo para responder consultas.
---

#### Pablo Lombardo Toledano, 2024.
