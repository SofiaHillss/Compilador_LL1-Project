from ttoken import TOKEN
class Operacoes:
    def __init__(self):
       
        self.unario = {
            (TOKEN.mais, (TOKEN.INT,False)): (TOKEN.INT, False),
            (TOKEN.mais, (TOKEN.FLOAT,False)): (TOKEN.FLOAT, False),
            (TOKEN.menos, (TOKEN.FLOAT,False)): (TOKEN.FLOAT, False),
            (TOKEN.menos, (TOKEN.INT,False)): (TOKEN.INT, False),
            (TOKEN.NOT, (TOKEN.INT,False)): (TOKEN.INT, False),
        
        }
        
     
        self.binario = {

            # operações com lista 
            frozenset({TOKEN.mais, (TOKEN.INT, True),(TOKEN.INT, True)}): (TOKEN.INT, True),
            frozenset({TOKEN.mais, (TOKEN.FLOAT, True),(TOKEN.FLOAT, True)}): (TOKEN.FLOAT, True),
            frozenset({TOKEN.mais, (TOKEN.STRING, True),(TOKEN.STRING, True)}): (TOKEN.STRING, True),
            frozenset({TOKEN.menos, (TOKEN.FLOAT,True), (TOKEN.FLOAT,True)}): (TOKEN.FLOAT, True),
            frozenset({TOKEN.menos, (TOKEN.INT,True), (TOKEN.INT,True)}): (TOKEN.INT, True),

            # operções aritmética
            frozenset({TOKEN.mais, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.mais, (TOKEN.FLOAT, False),(TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.mais, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.menos, (TOKEN.FLOAT,False), (TOKEN.INT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.menos, (TOKEN.FLOAT,False), (TOKEN.FLOAT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.menos, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),
            frozenset({TOKEN.multiplica, (TOKEN.FLOAT,False), (TOKEN.INT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.multiplica, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),
            frozenset({TOKEN.multiplica, (TOKEN.FLOAT,False), (TOKEN.FLOAT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.divide, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.divide, (TOKEN.FLOAT,False), (TOKEN.INT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.divide, (TOKEN.FLOAT,False), (TOKEN.FLOAT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.MOD, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),
            frozenset({TOKEN.MOD, (TOKEN.FLOAT,False), (TOKEN.INT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.MOD, (TOKEN.FLOAT,False), (TOKEN.FLOAT,False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.DIV, (TOKEN.FLOAT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),
            frozenset({TOKEN.DIV, (TOKEN.FLOAT,False), (TOKEN.FLOAT,False)}): (TOKEN.INT, False),
            frozenset({TOKEN.DIV, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),

            #operações logicas 
            frozenset({TOKEN.AND, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),
            frozenset({TOKEN.OR, (TOKEN.INT,False), (TOKEN.INT,False)}): (TOKEN.INT, False),

            #operados de comparações  
            frozenset({TOKEN.igual, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.igual, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.igual, (TOKEN.STRING, False),(TOKEN.STRING, False)}): (TOKEN.INT, False),

            frozenset({TOKEN.diferente, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.diferente, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.diferente, (TOKEN.STRING, False),(TOKEN.STRING, False)}): (TOKEN.INT, False),

            frozenset({TOKEN.menor, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menor, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menor, (TOKEN.INT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menor, (TOKEN.STRING, False),(TOKEN.STRING, False)}): (TOKEN.INT, False),

            frozenset({TOKEN.menorIgual, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menorIgual, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menorIgual, (TOKEN.INT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menorIgual, (TOKEN.STRING, False),(TOKEN.STRING, False)}): (TOKEN.INT, False),

            frozenset({TOKEN.maior, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.maior, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.maior, (TOKEN.INT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.maior, (TOKEN.STRING, False),(TOKEN.STRING, False)}): (TOKEN.INT, False),

            frozenset({TOKEN.maiorIgual, (TOKEN.INT, False),(TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.maiorIgual, (TOKEN.FLOAT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.maiorIgual, (TOKEN.INT, False),(TOKEN.FLOAT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.maiorIgual, (TOKEN.STRING, False),(TOKEN.STRING, False)}): (TOKEN.INT, False),
            
        }


    def resolve_unario(self, operador: TOKEN, tipo: tuple[TOKEN, bool]) -> tuple[TOKEN, bool]:
        return self.unario.get((operador, tipo), (None, False))

    def resolve_binario(self, operador: TOKEN, tipo_esq: tuple[TOKEN, bool], tipo_dir: tuple[TOKEN, bool]) -> tuple[TOKEN, bool]:
        chave = frozenset({operador, tipo_esq, tipo_dir})
        return self.binario.get(chave, (None, False))
