# Instrucciones para realizar la instalacion de Jupyter Lab y sus distintas bilbiotecas

Hay dos formas de instalar lo necesario para poder usar Jupyter Books/Lab: la fácil y la "difícil".  
La primera de ellas consiste en descargar [Anaconda](https://www.anaconda.com/products/individual) e instalar las librerías que en la página de instrucciones queda bastante explícito el [cómo se hace](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html).    
La "difícil" consiste en solo instalar Jupyter Lab. Esta es la recomendada en caso de que se este familiarizado con el simbolo de sistema/terminal y con la infórmatica en general.
## Pasos para la instalación "difícil"
Dado que la librería que se usa para el proyecto (Traffic) tiene dependecias con librerías dinámicas se va a tener que instalar Miniconda. Una vez instalado Miniconda, se podrá crear el entorno virtual donde poder ejecutar y realizar todas las tareas pertientes.  
1. [Descargar Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Configurar el [entorno virtual](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)  
2.1  Se crea el entorno virtual:  ```conda create -n yourenvname```  
2.2 Se activa el entorno virtual : ```source activate yourenvname```  
2.3 Se instalan los paquetes : ```conda install yourpackege``` 

Dado que se va a tratar un caso particular, los paquetes que se instalaran( con el comando puesto) serán:  
* Jupyter Lab con el comando : ```conda install -c conda-forge jupyterlab```  

*  Las librerias dinámicas de las que depende Traffic : ```conda install cartopy shapely ```  
* Y Traffic : ```pip install traffic```  

Lo siguientes que se tiene que instalar son los "widgets" de Jupyter Lab. Los comandos en orden de instalación son:  
1. ```conda install -c conda-forge ipywidgets ```
2. ```conda install -c conda-forge nodejs ```
3. ``` jupyter labextension install @jupyter-widgets/jupyterlab-manager  ```
4. ```jupyter labextension install jupyter-leaflet ```  
5. ```jupyter labextension install keplergl-jupyter ```

Finalmente, para comprobar que la instalacion ha sido correcta se iniciará por el terminal el comando: ```jupyter lab```
## Configuración de Traffic
Para poder acceder al Impala Shell de OpenSky se necesita unas claves de acceso que previamente hay que solicitar. 