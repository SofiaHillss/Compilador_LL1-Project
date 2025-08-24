from ttoken import TOKEN
from typing import Dict, Tuple, List, Optional
from operacoes import Operacoes
import sys

class AnalisadorSemantico(Operacoes):
    def __init__(self, nomeAlvo: str) -> None:
        super().__init__()
        self.alvo = open(nomeAlvo, "wt")
        self.tabelaSimbolos: Dict[str, Tuple[Tuple[TOKEN, bool], List[Tuple[TOKEN, bool]], Dict[str, Tuple[TOKEN, bool]]]] = {}
        self.escopoAtual: Optional[Dict[str, Tuple[TOKEN, bool]]] = None

    def erroSemantico(self, token: Tuple[TOKEN, str, int, int], msg: str) -> None:
        print("Erro semântico: {} (linha {}, coluna {})".format(msg, token[2], token[3]))
        sys.exit(1)

    def modificaEscopo(self, lexema: str) -> None:
        if lexema not in self.tabelaSimbolos:
            raise KeyError(f"Função '{lexema}' não declarada.")
        
        (_ , listaParams, escopoFunc) = self.tabelaSimbolos[lexema]
        self.escopoAtual = escopoFunc

        if not listaParams:
            return
        
        for (token, tipo_parametro) in listaParams:
            self.declaraVar(token, tipo_parametro)

    def declaraVar(self, token: Tuple[TOKEN, str, int, int], tipo_par: Tuple[TOKEN, bool]) -> None:
        if self.escopoAtual is None:
            raise RuntimeError("Escopo atual não definido.")
        
        _, lexema, _, _ = token
        if lexema in self.escopoAtual:
            msg = f'Variável "{lexema}" redeclarada.'
            self.erroSemantico(token, msg)
        else:
            self.escopoAtual[lexema] = tipo_par

    def declaraFunc(self, tipo_retorno: Tuple[TOKEN, bool], ident_func: Tuple[TOKEN, str, int, int], listaParams: List[Tuple[TOKEN, bool]]) -> None:
        _, lexema, _, _ = ident_func
        if lexema in self.tabelaSimbolos:
            msg = f'Função "{lexema}" redeclarada.'
            self.erroSemantico(ident_func, msg)
        else:
            # Cada função tem seu próprio escopo de variáveis
            self.tabelaSimbolos[lexema] = (tipo_retorno, listaParams, {})

    def finaliza(self):
        self.alvo.close()

    def gera(self, nivel, codigo):
        identacao = ' ' * 4 * nivel
        linha = identacao + codigo
        self.alvo.write(linha)

    def isIdentVar(self, lexema: str) -> bool:
        return self.escopoAtual is not None and lexema in self.escopoAtual

    def isIdentFunc(self, lexema: str) -> bool:
        return lexema in self.tabelaSimbolos

    def pegaTipoIdent(self, token: Tuple[TOKEN, str, int, int]) -> Tuple[TOKEN, bool]:
        if self.escopoAtual is None or token[1] not in self.escopoAtual:
            msg = f'Identificador {token[1]} não declarado'
            self.erroSemantico(token, msg)
            return ("ERRO", False) 
        return self.escopoAtual[token[1]]

    def pegaInfoFunc(self, token:Tuple[TOKEN, str, int, int]) -> Tuple[Tuple[TOKEN, bool], List[Tuple[TOKEN, bool]], Dict[str, Tuple[TOKEN, bool]]]:
        if token[1] not in self.tabelaSimbolos:
            msg = f'Função {token[1]} não declarada'
            self.erroSemantico(token, msg)

        return self.tabelaSimbolos[token[1]]
    
    
    def getFuncInfo(self, nome_func: str) -> Tuple[Tuple[TOKEN, bool], List[Tuple[TOKEN, bool]]]:
        if nome_func not in self.tabelaSimbolos:
            raise KeyError(f"Função '{nome_func}' não declarada.")
        
        tipo_retorno, lista_parametros, _ = self.tabelaSimbolos[nome_func]
        return tipo_retorno, lista_parametros

    def operacao_unaria(self,operador: TOKEN, tipo: tuple[TOKEN, bool] , token:Tuple[TOKEN, str, int, int])->tuple[TOKEN, bool] :
        result_type =self.resolve_unario(operador,tipo)

        if not result_type[0] :
            self.erroSemantico(token,"Variavel do tipo invalido para operação {operador}")
        
        return result_type
    def operacao_binaria(self, 
                            token:Tuple[TOKEN, str, int, int],
                            operador: TOKEN, 
                            tipo_esq: tuple[TOKEN, bool],
                            tipo_dir: tuple[TOKEN, bool]
                        )->tuple[TOKEN, bool]:


        result_type =self.resolve_binario(operador,tipo_esq, tipo_dir)
        
        if not result_type[0] :
            self.erroSemantico(token,"Variavel do tipo invalido para operação {tipo_esq}{operador}{tipo_dir}")
        
        return result_type
