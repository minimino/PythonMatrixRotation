# Importamos todas las funciones de Manim
from manim import *
# Importamos NumPy
import numpy as np

# https://pastebin.com/bTSF02RC
# Type of animations
# https://azarzadavila-manim.readthedocs.io/en/latest/animation.html
# Rate functions
# https://www.reddit.com/r/manim/comments/gzmnrp/manim_tip_rate_functions_when_playing_animation/
# All functions
# https://docs.manim.community/en/v0.2.0/genindex.html
# Exec args
# https://infograph.tistory.com/122

class RotationMatrix(Matrix):
    """
        Clase para implementar una matriz de rotación 2x2 con los senos y cosenos. Permite
        animar el cambio de ángulo y establecer el número de decimales de dicho ángulo.
        
        Parámetros
        ----------------
            matrix : lista de listas que contienen los ángulos de cada entrada de la matriz de rotación.
            is_number : booleano que indica si las entradas son ángulos o letras (como alfa, beta...). Las
                                  letras estarán dadas en formato LaTeX.
            num_decimal : int que indica el número de decimales que incluir en los ángulos.
            
        Métodos
        ------------
            sin_cosine : método auxiliar para crear la matriz de rotación que sustituye la función que se 
                                 utiliza en el código fuente de la clase Matrix de Manim.
            update_mob : este método debe ejecutarse después del método change_matrix_values para
                                     guardar los cambios realizados por este.
            change_matrix_values : permite cambiar las letras (alfa, beta...) por números
    """
        
    def __init__(self, matrix, is_number = True, num_decimal = 0,**kwargs):
        self.num_decimal = num_decimal
        self.is_number = is_number
        # Variable auxiliar para el método sin_cosine. 
        # Permite conocer en qué entrada de la matriz nos encontramos
        self.ind = 0
        # Lista que guarda los objetos que contienen los ángulos de cada entrada
        self.angles = []
        
        # Iniciamos la clase Matrix de Manim
        Matrix.__init__(self, matrix, element_to_mobject = self.sin_cosine, h_buff = 2.5, **kwargs)    
    
    def sin_cosine(self, angle):
        # Texto de la entrada actual (sin o cos)
        text1 = None
        if self.ind in [1, 4]:
            # Si nos encontramos en las posiciones 1 o 4 poner cos
            text1 =  MathTex(r"\cos")
        elif self.ind == 2:
            # Si nos encontramos en la posición 2 poner -sin
            text1 =  MathTex(r"-\sin")
        else:
            # Si nos encontramos en la posición 3 poner sin
            text1 =  MathTex(r"\sin")
        
        # Parámetro del sin o cos de la entrada actual
        text2 = None
        if self.is_number:
            text2 = DecimalNumber(angle, num_decimal)
        else:
            text2 = MathTex(angle)
        
        # Ponemos text2 a la derecha de text1
        text2.next_to(text1, direction = RIGHT)
        # Incluimos el objeto text2 en la lista self.angles
        self.angles.append(text2)
        # Pasamos a la siguiente posición
        self.ind += 1
        
        # Devolvemos un grupo formado por text1 y text2
        return VGroup(text1, text2)
    
    def update_mob(self):
        counter = 1
        # Para cada entrada de la matriz...
        for i in range(2):
            for j in range(2):
                # Eliminamos el valor anterior del ángulo en la posición (i, j) de la matriz
                self.mob_matrix[i][j] -= self.mob_matrix[i][j][1]
                # Añadimos el nuevo valor (self.mob_matrix[i][j] es un VGroup formado por
                # sin o cos + ángulo
                self.mob_matrix[i][j] += self.angles[counter]
                counter += 1
    
    def change_matrix_values(self, val):
        # Por algún motivo extraño self.angles tiene un elemento de más siempre
        # Por eso añadimos un elemento None al principio de angles_aux
        angles_aux = [None] + \
            [ DecimalNumber(val, self.num_decimal).move_to(angle.get_center()).scale(0.8) for angle in self.angles[1:] ]
        # Lista que contiene las animaciones para transformar los ángulos antiguos (alfas, betas...) por números nuevos,
        # dados por el parámetro val
        res = [ ReplacementTransform(self.angles[i], angles_aux[i]) for i in range(1, len(self.angles)) ]
        # Reemplazamos la variable self.angles por los nuevos objetos de ángulo
        self.angles = angles_aux
        
        # Devolvemos las animaciones (sin reproducir)
        return res
        
class Prueba(Scene):
    """
        Aquí están todas las animaciones. Orden:
            1. create_plane : se crea el plano, con el círculo y el vector con sus coordenadas
            2. create_matrix : se crea la matriz de rotación arriba la izquierda
            3. create_angle : creamos el ángulo alfa arriba a la izquierda y sustituye alfa por 0 en la
                matriz
            4. rotate_vector : enseña la multiplicación de matrices y rota el vector
    """
    def construct(self):
        self.angle = DecimalNumber(0, num_decimal_places = 0)
        self.create_plane()
        self.create_matrix()
        # Enlazamos el vector y sus coordenadas, de manera que la posición del vector afecte
        # a la posición del texto
        self.pos_text.add_updater(lambda obj : obj.next_to(self.vector, direction = UP))
        self.create_angle()
        self.rotate_vector(90)
        # Esperamos 2 segundos al terminar las animaciones antes de acabar el vídeo
        self.wait(2)
        
    def create_plane(self):
        # Creamos el plano y lo dibujamos
        plane = self.play(ShowCreation(NumberPlane()))
        # Posición inicial del vector
        self.pos = np.array([1, 0])
        # Creamos el vector en esa posición
        self.vector = Vector(self.pos)
        # Creamos el círculo discontinuo
        circle = DashedVMobject(Circle(color = BLUE))
        
        # Creamos el número que representa la posición X del vector
        self.x_val = DecimalNumber(self.pos[0])
        # Creamos el número que representa la posición Y del vector
        self.y_val = DecimalNumber(self.pos[1])
        # Creamos el paréntesis izquierdo de las coordenadas
        vec_text1 = Text("(")
        # Ponemos x_val a la derecha del paréntesis anterior
        self.x_val.next_to(vec_text1, direction = RIGHT*.5)
        # Creamos la coma que separa las coordenadas y lo ponemos abajo a la derecha de x_val
        vec_text2 = MathTex(",").next_to(self.x_val, direction = DOWN*.1 + RIGHT*.3)
        # Ponemos y_val a la derecha de la coma
        self.y_val.next_to(vec_text2, direction = UP*.1 + RIGHT*.5)
        # Creamos el paréntesis derecho de las coordenadas y lo ponemos a la derecha de y_val
        vec_text3 = Text(")").next_to(self.y_val, direction = RIGHT*.5)
        
        # Creamos un grupo con las todas las componentes de las coordenadas (números + ( + ) + ,)
        # y lo hacemos más pequeño (con scale)
        self.pos_text = VGroup(vec_text1, self.x_val, vec_text2, self.y_val, vec_text3).scale(0.7)
        # Ponemos el grupo encima de la flecha
        self.pos_text.next_to(self.vector, direction = UP)
        
        # Animamos la creación de los elementos creados anteriormente
        # Dibujamos el vector en 1 segundo (run_time = 1)
        self.play(Write(self.vector, run_time = 1))
        # Dibujamos las coordenadas
        self.play(Write(self.pos_text))
        # Dibujamos el círculo en 2 segundos
        self.play(ShowCreation(circle, run_time = 2))
        
    def create_matrix(self):
        # Creamos la matriz de rotación con \alpha como valor de ángulo
        self.mat_rot = RotationMatrix([[r"\alpha", r"\alpha"], [r"\alpha", r"\alpha"]], is_number = False)
        # Creamos la matriz columna que indica el vector inicial
        self.vec_orig = IntegerMatrix([[self.pos[0]], [self.pos[1]]])
        # Creamos el =
        self.equals = MathTex(r"=")
        # Creamos la matriz columna que indica el vector rotado (el producto de las matrices anteriores)
        self.vec_rot = IntegerMatrix([[0], [1]])
        
        # Ponemos el vector inicial a la derecha de la matriz de rotación
        self.vec_orig.next_to(self.mat_rot, direction = RIGHT)
        # Ponemos el = a la derecha del vector inicial
        self.equals.next_to(self.vec_orig, direction = RIGHT)
        # Ponemos el vector rotado a la derecha del =
        self.vec_rot.next_to(self.equals, direction = RIGHT)
        
        # Ocultamos los valores de los vectores inicial y rotado
        for el in self.vec_rot.elements: el.set_opacity(0)
        for el in self.vec_orig.elements: el.set_opacity(0)
        
        # Creamos un grupo con la matriz de rotación, vector original, = y vector rotado
        self.matriz_juntas = VGroup(self.mat_rot, self.vec_orig, self.equals, self.vec_rot)
        # Le ponemos un fondo negro con borde azul
        self.matriz_juntas.bg = SurroundingRectangle(self.matriz_juntas, color=BLUE, fill_color=BLACK, fill_opacity=1)
        # Creamos un grupo con el fondo y matriz_juntas y lo hacemos más pequeño
        self.label_group = VGroup(self.matriz_juntas.bg, self.matriz_juntas).scale(0.8)
        # Lo movemos a la esquina superior derecha
        self.label_group.to_corner(UP+RIGHT)
         
         # Animamos la creación de las matrices y su fondo
        self.play(Write(self.label_group, run_time = 3))
        # Mostramos las coordenadas de la matriz columna que representa el vector original
        self.vec_orig.elements.set_opacity(1)
        # Copiamos las coordenadas del vector que está encima de la flecha
        self.pos_copy = self.pos_text.copy()
        # Movemos la copia a donde está la matriz columna mientras animamos el cambio de opacidad (FadeIn)
        self.play(Transform(self.pos_copy, self.vec_orig), FadeIn(self.vec_orig.elements))
        # Ocultamos la copia (no sé cómo se borran elementos, jeje)
        self.pos_copy.set_opacity(0)
        
    def create_angle(self):
        # Creamos el \alpha que se pone en el recuadro superior izquierdo
        angle_text = MathTex(r"\alpha")
        # Creamos el =
        angle_eq = MathTex(r"=").next_to(angle_text, direction = RIGHT)
        # Creamos el número que los acompaña con 0 decimales
        self.angle = DecimalNumber(0, num_decimal_places = 0).next_to(angle_eq, direction = RIGHT)
        # Juntamos los 3 elementos anteriores
        self.angle_group = VGroup(angle_text, angle_eq, self.angle)
        # Creamos el fondo del grupo anterior. Esta vez le ponemos un margen (buff) de 0.45, para que no se salga 
        # el valor de \alpha al cambiar de 1 dígito (0) a 2 dígitos (90)
        bg = SurroundingRectangle(self.angle_group, color=BLUE, buff = 0.45, fill_color=BLACK, fill_opacity=1)
        # Juntamos el fondo y angle_group
        self.angle_group = VGroup(bg, self.angle_group)
        # Llevamos todo a la esquina superior izquierda
        self.angle_group.to_corner(UP+LEFT)
        
        # Copiamos todos los ángulos de la matriz de rotación para posteriormente animarlos y moverlos a la izquierda
        # Ponemos range(1, 5) porque hay un bug en la clase de la matriz de rotación en el que se crea un elemento 
        # adicional (no sé por qué es, pero de momento me suda los cojones)
        alphas = [ self.mat_rot.angles[i].copy() for i in range(1, 5) ]
        # Reproducimos la transición que mueve la copia de los alfas de la matriz de rotación a la izquierda mientras
        # aparece el grupo angle_group
        self.play(*[ Transform(alphas[i], angle_text) for i in range(4) ], FadeIn(self.angle_group, run_time = 3))
        
        # Hacemos 4 copias de angle para llevarlos a la matriz de rotación
        angles_text = [ self.angle.copy() for i in range(4) ]
        # Reproducimos la transición que mueve las copias anteriores a las entradas de la matriz de rotación
        # mientras cambiamos los valores de la matriz de rotación de alfa a 0
        self.play(
            *[ ReplacementTransform(angles_text[i], self.mat_rot.angles[i + 1]) for i in range(4) ], 
            *self.mat_rot.change_matrix_values(0)
        )
        # Actualizamos los valores internos de la matriz de rotación
        self.mat_rot.update_mob()
        
        # Ocultamos las copias angles_text (sigo sin saber borrar)
        for txt in angles_text: txt.set_opacity(0) 
        self.play(*[ FadeOut(txt) for txt in angles_text ])
        
    def rotate_vector(self, angle):
        # Creamos la matriz de rotación, pero esta vez no es una imagen sino que es una matriz 
        # de verdad
        sin_mat = np.array(
            [[np.cos(np.deg2rad(angle)), -np.sin(np.deg2rad(angle))], 
              [np.sin(np.deg2rad(angle)), np.cos(np.deg2rad(angle))]]
        )
        # Multiplicamos el vector original por la matriz de rotación, para saber el resultado
        result = np.matmul(sin_mat, np.array([[self.pos[0]], [self.pos[1]]]))
        
        # Animamos el recuadro superior izquierdo, haciéndolo grande y pequeño
        self.play(ScaleInPlace(self.angle_group, 1.2), rate_func = rush_into)
        self.play(ScaleInPlace(self.angle_group, 1/1.2), rate_func = rush_from)
        
        # Animamos el cambio del ángulo de alpha
        self.play(ChangeDecimalToValue(self.angle, angle))
        # Animamos el cambio del ángulo en la matriz de rotación
        self.play(*[ ChangeDecimalToValue(self.mat_rot.angles[i], angle) for i in range(1, 5) ])
        # Mostramos la multiplicación de matrices
        self.show_mul(sin_mat)
        
        # Duración de cada una de las siguientes animaciones
        duration = 1
        self.play(
            # Rotamos el vector PI/2
            Rotating(self.vector, radians = PI/2, about_point = ORIGIN, run_time=duration), 
            # Animamos el cambio de las coordenadas del vector
            ChangeDecimalToValue(self.x_val, result[0][0], run_time=duration), 
            ChangeDecimalToValue(self.y_val, result[1][0], run_time=duration)
        )
        
    def show_mul(self, sin_mat):
        # Movemos el recuadro superior derecho al centro mientras lo hacemos más grande
        self.play(self.label_group.animate.scale(1.5).move_to(ORIGIN))

        # Cambiamos cada una de las entradas por su valor numérico
        for i in range(2):
            for j in range(2):
                # Cogemos el elemento (i, j) de la matriz
                mat_el = self.mat_rot.mob_matrix[i][j]
                # Creamos el número
                aux_int = Integer(sin_mat[i][j]).move_to(mat_el.get_center()).scale(1.13)
                # Transformamos el elemento (i, j) por su valor numérico
                self.play(Transform(mat_el, aux_int))
                # Ocultamos el número
                aux_int.set_opacity(0)
        
        # Animamos hacer más ancho el recuadro mientras movemos el corchete del paréntesis a la izquierda
        self.play(
            self.matriz_juntas.bg.animate.set_width(self.matriz_juntas.bg.width + 2), 
            self.label_group[1].animate.shift(LEFT)
        )
        
        # Animamos muchas cosas (todas a la vez)
        self.play(
            # Movemos la columna derecha de la matriz de rotación hacia la izquierda
            self.mat_rot.mob_matrix[0][1].animate.shift(LEFT), 
            self.mat_rot.mob_matrix[1][1].animate.shift(LEFT), 
            # Movemos el ] de la matriz de rotación a la izquierda
            self.mat_rot[2].animate.shift(LEFT), 
            # Movemos el vector original a la izquierda
            self.vec_orig.animate.shift(LEFT), 
            # Movemos el vector rotado a la izquierda
            self.vec_rot.animate.shift(LEFT), 
            # Movemos el = a la izquierda
            self.equals.animate.shift(LEFT), 
            # Movemos el ] del vector rotado a la derecha
            self.vec_rot[2].animate.shift(RIGHT*2), 
            # Movemos los elementos del vector rotado a la derecha
            self.vec_rot[0].animate.shift(RIGHT*0.5)
        )
        
        # Hacemos una copia de los elementos de la matriz de rotación y del vector original
        mat_els_copies = [ self.mat_rot.mob_matrix[i][j].copy() for i in range(2) for j in range(2) ]
        vec_els_copies = [ self.vec_orig.mob_matrix[i][0].copy() for i in list(range(2))*2 ]
        
        # Por cada fila en la matriz de rotación...
        for i in range(2):
            # Cogemos la posición del centro del vector rotado
            center = self.vec_rot.mob_matrix[i][0].get_center() + 1.8*LEFT
            
            # Esta variable la usamos para saber qué elemento de las listas de copias coger
            j = 0
            if i == 0: 
                j = 0
            else:
                j = 2
            
            # Movemos una copia de una entrada de la matriz al vector rotado
            self.play(mat_els_copies[j].animate.move_to(center))
            # Creamos el · de multiplicación y lo ponemos a la derecha del elemento anterior
            mult_dot1 = MathTex(r"\cdot").next_to(mat_els_copies[j], direction = RIGHT)
            # Animamos la creación del ·
            self.play(FadeIn(mult_dot1))
            # Movemos una copia de una entrada del vector original al vector rotado y lo ponemos a 
            # la derecha del punto
            self.play(vec_els_copies[j].animate.next_to(mult_dot1, direction = RIGHT))
            # Creamos el + y lo ponemos a la derecha del elemento anterior
            sum_sign = MathTex(r"+").next_to(vec_els_copies[j], direction = RIGHT)
            # Animamos la creación del +
            self.play(FadeIn(sum_sign))
            
            
            # Movemos la copia de la entrada restante de la matriz al vector rotado
            self.play(mat_els_copies[j + 1].animate.next_to(sum_sign, direction = RIGHT))
            # Creamos el · de multiplicación y lo ponemos a la derecha del elemento anterior
            mult_dot2 = MathTex(r"\cdot").next_to(mat_els_copies[j + 1], direction = RIGHT)
            # Animamos la creación del ·
            self.play(FadeIn(mult_dot2))
            # Movemos una copia de una entrada del vector original al vector rotado y lo ponemos a 
            # la derecha del punto
            self.play(vec_els_copies[j + 1].animate.next_to(mult_dot2, direction = RIGHT))
                
            # Creamos un grupo con todos los elementos que componen la suma
            aux_group = VGroup(mat_els_copies[j], mult_dot1, vec_els_copies[j], sum_sign, mat_els_copies[j + 1], mult_dot2, vec_els_copies[j + 1])
            self.play(
                # Transformamos el grupo anterior por el valor numérico de la entrada del vector rotado
                ReplacementTransform(aux_group, self.vec_rot.elements[i]),
                # Mostramos el valor del vector rotado
                self.vec_rot.elements[i].animate.set_opacity(1)
            ) 
        
        # Movemos las matrices al centro mientras hacemos el recuadro más pequeño y el vector rotado más pequeño
        self.play(
                self.label_group[1].animate.move_to(self.label_group[0].get_center() + RIGHT*1.5), 
                self.label_group[0].animate.set_width(self.label_group[0].width - 2).shift(RIGHT*0.25),
                self.vec_rot[0].animate.move_to(RIGHT*3.8),
                self.vec_rot[2].animate.move_to(RIGHT*4.6))
        # Movemos todo arriba a la derecha
        self.play(self.label_group.animate.scale(1/1.7).to_corner(UP+RIGHT))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        