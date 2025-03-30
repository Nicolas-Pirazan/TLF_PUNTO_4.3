from flask import Flask, render_template, request, jsonify
import random
import json
from queue import Queue

app = Flask(__name__)

class Grammar:
    """
    Clase que representa una gramática formal.
    
    Atributos:
        terminals (set): Conjunto de símbolos terminales.
        non_terminals (set): Conjunto de símbolos no terminales.
        start_symbol (str): Símbolo inicial de la gramática.
        productions (dict): Diccionario con producciones, donde la llave es un no terminal y 
                            el valor es una lista de producciones.
    """
    
    def __init__(self):
        """Inicializa una nueva instancia de la gramática."""
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = ""
        self.productions = {}
        
    def add_terminal(self, terminal):
        """
        Agrega un símbolo terminal a la gramática.
        
        Parámetros:
            terminal (str): Símbolo terminal a agregar.
        """
        self.terminals.add(terminal)
        
    def add_non_terminal(self, non_terminal):
        """
        Agrega un símbolo no terminal a la gramática.
        
        Parámetros:
            non_terminal (str): Símbolo no terminal a agregar.
        """
        self.non_terminals.add(non_terminal)
        
    def set_start_symbol(self, start_symbol):
        """
        Establece el símbolo inicial de la gramática.
        
        Parámetros:
            start_symbol (str): Símbolo que se establecerá como inicial.
            
        Lanza:
            ValueError: Si el símbolo proporcionado no es un no terminal.
        """
        if start_symbol in self.non_terminals:
            self.start_symbol = start_symbol
        else:
            raise ValueError(f"El símbolo inicial '{start_symbol}' debe ser un no terminal")
        
    def add_production(self, non_terminal, production):
        """
        Agrega una producción a la gramática.
        
        Parámetros:
            non_terminal (str): El no terminal al que pertenece la producción.
            production (str): La producción a agregar.
            
        Lanza:
            ValueError: Si el no terminal no está definido o si algún símbolo de la producción
                        no está definido como terminal o no terminal.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(f"'{non_terminal}' no es un símbolo no terminal")
        
        # Validar símbolos en la producción
        for symbol in production:
            if symbol not in self.terminals and symbol not in self.non_terminals:
                raise ValueError(f"Símbolo '{symbol}' no está definido")
            
        if non_terminal not in self.productions:
            self.productions[non_terminal] = []
            
        self.productions[non_terminal].append(production)
        
    def validate(self):
        """
        Valida la gramática para verificar que cumpla ciertos requisitos mínimos.
        
        Retorna:
            (bool, str): Tupla que indica si la gramática es válida y un mensaje descriptivo.
        """
        if len(self.terminals) < 2:
            return False, "Se requieren al menos 2 símbolos terminales"
            
        if len(self.non_terminals) < 3:
            return False, "Se requieren al menos 3 símbolos no terminales"
            
        total_productions = sum(len(prods) for prods in self.productions.values())
        if total_productions < 3:
            return False, "Se requieren al menos 3 producciones"
            
        if not self.start_symbol:
            return False, "Se requiere un símbolo inicial"
            
        if self.start_symbol not in self.productions or not self.productions[self.start_symbol]:
            return False, "El símbolo inicial debe tener al menos una producción"
            
        return True, "Gramática válida"
        
    def belongs_to_language(self, word, max_depth=15):
        """
        Verifica si una palabra pertenece al lenguaje generado por la gramática
        utilizando búsqueda BFS.
        
        Parámetros:
            word (str): La palabra a validar.
            max_depth (int): Profundidad máxima para la búsqueda.
            
        Retorna:
            (bool, list): Tupla que indica si la palabra pertenece al lenguaje y la derivación
                          realizada en forma de lista de pasos.
        """
        queue = Queue()
        queue.put((self.start_symbol, []))
        visited = set()

        while not queue.empty():
            current, path = queue.get()
            
            # Condición de éxito: cadena igual a la palabra y solo terminales
            if current == word and all(symbol in self.terminals for symbol in current):
                return True, path
            
            if len(path) >= max_depth:
                continue
                
            if current in visited:
                continue
            visited.add(current)
            
            # Solo derivar si hay no terminales
            for pos in range(len(current)):
                symbol = current[pos]
                if symbol in self.non_terminals and symbol in self.productions:
                    for production in self.productions[symbol]:
                        new_current = current[:pos] + production + current[pos+1:]
                        new_step = {
                            "from": current,
                            "to": new_current,
                            "rule": f"{symbol} -> {production}"
                        }
                        queue.put((new_current, path + [new_step]))
                        
        return False, []
    
        """parametro max_depth=5 es para el numero de niveles a generar"""
    
    def generate_general_tree(self, max_depth=5):
        """
        Genera el árbol general de derivación en formato diccionario.
        
        Parámetros:
            max_depth (int): Profundidad máxima del árbol.
            
        Retorna:
            dict: Representación del árbol de derivación.
        """
        tree = {
            "name": self.start_symbol,
            "accumulated": self.start_symbol,
            "children": []
        }
        self._generate_tree_recursive(
            symbol=self.start_symbol,
            parent_node=tree,
            current_depth=0,
            max_depth=max_depth,
            visited=set(),
            accumulated=self.start_symbol
        )
        return tree

    def _generate_tree_recursive(self, symbol, parent_node, current_depth, max_depth, visited, accumulated):
        """
        Método recursivo para generar el árbol de derivación.
        
        Parámetros:
            symbol (str): Símbolo actual a expandir.
            parent_node (dict): Nodo actual del árbol.
            current_depth (int): Profundidad actual en la recursión.
            max_depth (int): Profundidad máxima permitida.
            visited (set): Conjunto de claves ya visitadas para evitar ciclos.
            accumulated (str): Cadena acumulada hasta el momento.
        """
        if current_depth >= max_depth:
            return

        # Evitar ciclos usando el accumulated como parte de la clave
        key = (symbol, current_depth, accumulated)
        if key in visited:
            return
        visited.add(key)

        if symbol in self.productions:
            for production in self.productions[symbol]:
                # Calcular nuevo accumulated reemplazando el símbolo actual
                new_accumulated = accumulated.replace(symbol, production, 1)

                # Crear nodo hijo con el accumulated actualizado
                child_node = {
                    "name": production,
                    "accumulated": new_accumulated,
                    "children": []
                }
                parent_node["children"].append(child_node)

                # Expandir cada símbolo de la producción
                for char in production:
                    if char in self.non_terminals:
                        self._generate_tree_recursive(
                            symbol=char,
                            parent_node=child_node,
                            current_depth=current_depth + 1,
                            max_depth=max_depth,
                            visited=visited.copy(),
                            accumulated=new_accumulated
                        )
                                 
    def to_dict(self):
        """
        Convierte la gramática en un diccionario.
        
        Retorna:
            dict: Diccionario representativo de la gramática.
        """
        return {
            "terminals": list(self.terminals),
            "non_terminals": list(self.non_terminals),
            "start_symbol": self.start_symbol,
            "productions": {k: v for k, v in self.productions.items()}
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Grammar a partir de un diccionario.
        
        Parámetros:
            data (dict): Diccionario con los datos de la gramática.
            
        Retorna:
            Grammar: Instancia de la gramática creada.
        """
        grammar = cls()
        for terminal in data.get("terminals", []):
            grammar.add_terminal(terminal)
        for non_terminal in data.get("non_terminals", []):
            grammar.add_non_terminal(non_terminal)
        grammar.set_start_symbol(data.get("start_symbol", ""))
        for nt, prods in data.get("productions", {}).items():
            for prod in prods:
                grammar.add_production(nt, prod)
        return grammar

# Almacén de gramáticas
grammars = {}

@app.route('/')
def index():
    """
    Endpoint para renderizar la página principal.
    
    Retorna:
        Renderización de 'index.html'.
    """
    return render_template('index.html')

@app.route('/create_grammar', methods=['POST'])
def create_grammar():
    """
    Endpoint para crear una nueva gramática a partir de datos JSON.
    
    Retorna:
        JSON con el resultado de la operación, el id de la gramática en caso de éxito y la gramática creada.
    """
    try:
        data = request.json
        grammar_id = str(random.randint(1000, 9999))
        grammar = Grammar()
        
        # Añadir elementos
        for t in data.get('terminals', []):
            grammar.add_terminal(t)
        for nt in data.get('non_terminals', []):
            grammar.add_non_terminal(nt)
        grammar.set_start_symbol(data.get('start_symbol', ''))
        
        # Añadir producciones
        for prod in data.get('productions', []):
            grammar.add_production(prod['left'], prod['right'])
            
        # Validar
        is_valid, msg = grammar.validate()
        if not is_valid:
            return jsonify({"success": False, "message": msg})
            
        grammars[grammar_id] = grammar
        return jsonify({
            "success": True, 
            "grammar_id": grammar_id,
            "grammar": grammar.to_dict()
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/check_word', methods=['POST'])
def check_word():
    """
    Endpoint para verificar si una palabra pertenece al lenguaje generado por una gramática.
    
    Retorna:
        JSON con el resultado de la validación, la palabra, el árbol de derivación y el árbol general.
    """
    try:
        data = request.json
        grammar_id = data['grammar_id']
        word = data['word']
        
        grammar = grammars.get(grammar_id)
        if not grammar:
            return jsonify({"success": False, "message": "Gramática no encontrada"})
            
        belongs, derivation_tree = grammar.belongs_to_language(word)
        general_tree = grammar.generate_general_tree()
        
        return jsonify({
            "success": True,
            "belongs": belongs,
            "word": word,
            "derivation_tree": derivation_tree,
            "general_tree": general_tree
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/get_grammar/<grammar_id>', methods=['GET'])
def get_grammar(grammar_id):
    """
    Endpoint para obtener una gramática en base a su id.
    
    Parámetros:
        grammar_id (str): Identificador de la gramática.
        
    Retorna:
        JSON con la gramática si es encontrada, o un mensaje de error en caso contrario.
    """
    if grammar_id not in grammars:
        return jsonify({"success": False, "message": "Gramática no encontrada"})
    return jsonify({"success": True, "grammar": grammars[grammar_id].to_dict()})

@app.route('/list_grammars', methods=['GET'])
def list_grammars():
    """
    Endpoint para listar todas las gramáticas almacenadas.
    
    Retorna:
        JSON con la lista de gramáticas.
    """
    return jsonify({
        "success": True,
        "grammars": [{"id": k, "grammar": v.to_dict()} for k, v in grammars.items()]
    })

if __name__ == '__main__':
    """
    Punto de entrada de la aplicación. Inicia el servidor Flask en modo debug.
    """
    app.run(debug=True)
