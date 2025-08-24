
from lexico import TOKEN
from semantico import AnalisadorSemantico

class Sintatico:

    def __init__(self, lexico):
        self.lexico = lexico
        self.nomeAlvo = 'alvo.out'
        self.arquivo_alvo = open("result.py", "w+") 
        self.indentacao_atual= 1
        self.semantico = AnalisadorSemantico(self.nomeAlvo)

    def traduz(self):
        self.tokenLido = self.lexico.getToken()
        try:
            self.prog()
            print('Traduzido com sucesso.')
        except:
            pass
        self.semantico.finaliza()

    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token:
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f'Era esperado {msgTokenAtual} mas veio {msg}')
            raise Exception

    def testaLexico(self):
        self.tokenLido = self.lexico.getToken()
        (token, lexema, linha, coluna) = self.tokenLido
        while token != TOKEN.eof:
            self.lexico.imprimeToken(self.tokenLido)
            self.tokenLido = self.lexico.getToken()
            (token, lexema, linha, coluna) = self.tokenLido


#-------- segue a gramatica -----------------------------------------
    #Prog --> lambda | Func Prog
    def prog (self):
        if self.tokenLido[0] == TOKEN.eof:
            if self.semantico.getFuncInfo("main"):
                self.arquivo_alvo.write("\n\nmain()")

            return
        
        self.func()
        self.prog()
  

    #Func --> TipoRet ident ( ListParam ) Corpo
    def func(self):
        tipo_retorno= self.tipo_ret()
        ident_func= self.tokenLido
        self.consome(TOKEN.ident)
        self.consome(TOKEN.abrePar)
        lista_parametro=self.list_param()
        self.consome(TOKEN.fechaPar)
        self.semantico.declaraFunc(tipo_retorno, ident_func,lista_parametro)
        _, lexema, _, _ =ident_func
        self.semantico.modificaEscopo(lexema) 
        parametros_str = [param[0][1] for param in lista_parametro]
        self.indentacao_atual=1

        if  parametros_str:
            codigo_function ="\n"+ "def " + ident_func[1] + "(" + ", ".join(parametros_str) + "):"
            if lista_parametro :
                for param in lista_parametro:
                    (_, nome_ident, _, _), (_, eh_lista) = param
                    if eh_lista:
                        codigo_function += "\n" + (" " * 4) + f"{nome_ident} = {nome_ident}.copy()"
        else:
            codigo_function ="\n"+ "def " + ident_func[1] + "():"
            
        self.arquivo_alvo.write(codigo_function)
        self.corpo(tipo_retorno)

    #TipoRet --> void | Tipo
    def tipo_ret(self)-> tuple[TOKEN, bool]:
        if self.tokenLido[0] == TOKEN.VOID:
            self.consome(TOKEN.VOID)
            return (TOKEN.VOID, False)
        
        return self.tipo()
        
    #ListaParam --> lambda | Param OpcParams
    def list_param(self) -> list[tuple[tuple[TOKEN, str, int, int], tuple[TOKEN, bool]]]:
        if self.tokenLido[0] == TOKEN.fechaPar:
            return []

        primeiro_param = self.param()
        return self.opc_params([primeiro_param])
    
    #Param --> Tipo ident
    def param(self) -> tuple[tuple[TOKEN, str, int, int], tuple[TOKEN, bool]]:
        tipo_parametro: tuple[TOKEN, bool] = self.tipo()
        ident_token: tuple[TOKEN, str, int, int] = self.tokenLido
        self.consome(TOKEN.ident)
        return (ident_token, tipo_parametro)
    
    #OpcParams --> lambda | ,Param OpcParams
    def opc_params(self, parametro_list: list[tuple[tuple[TOKEN, str, int, int], tuple[TOKEN, bool]]]) -> list[tuple[tuple[TOKEN, str, int, int], tuple[TOKEN, bool]]]:
        if self.tokenLido[0] != TOKEN.virg:
            return parametro_list

        self.consome(TOKEN.virg)
        parametro_list.append(self.param())
        return self.opc_params(parametro_list)

    #Corpo --> { ListaDeclara ListaComando }
    def corpo(self, type_retorno_func: tuple[TOKEN, bool]):
        self.consome(TOKEN.abreChave)
        self.lista_declara()

        self.lista_comando(type_retorno_func)
        self.consome(TOKEN.fechaChave)

    #ListaDeclara --> lambda | Declara ListaDeclara
    def lista_declara(self):
        if self.tokenLido[0] not in {TOKEN.STRING , TOKEN.INT , TOKEN.FLOAT, TOKEN.abreColchete}:
            return
        
        self.declara()
        self.lista_declara()

    #ListaComando -> LAMBDA | Comando ListaComando
    def lista_comando(self, type_retorno_func: tuple[TOKEN,bool]):
        while self.tokenLido[0] != TOKEN.fechaChave:
            self.comando(type_retorno_func)

    #Declara --> Tipo ListaVar ;
    def declara(self):
        tipo =self.tipo()
        codigo_atual= self.lista_var(tipo)
        self.consome(TOKEN.ptoVirg)
        self.arquivo_alvo.write((" "*4)+codigo_atual)


    def lista_var(self, tipo_ident_declara: tuple[TOKEN, bool]) -> str:
        codigo_atual = self.var(tipo_ident_declara)
        return self.resto_listvar(tipo_ident_declara, codigo_atual)

    # RestoListaVar --> lambda | , ListaVar 
    def resto_listvar(self, tipo_ident_declara: tuple[TOKEN, bool], codigo_atual: str) -> str:
        while self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            codigo_mais = self.var(tipo_ident_declara)
            codigo_atual += "\n" + codigo_mais
        return codigo_atual

    #Tipo --> Primitivo | [ Primitivo ]
    def tipo(self)-> tuple[TOKEN, bool]:
        if self.tokenLido[0] != TOKEN.abreColchete:
            return (self.primitivo(), False)
   
        self.consome(TOKEN.abreColchete)
        token =self.primitivo()
        self.consome(TOKEN.fechaColchete)
        return (token, True)

    #Primitivo --> int | float | string
    def  primitivo(self)->  TOKEN.INT | TOKEN.FLOAT | TOKEN.STRING:
        if self.tokenLido[0] == TOKEN.INT:
            self.consome(TOKEN.INT) 
            return TOKEN.INT     
        if self.tokenLido[0] == TOKEN.FLOAT:
            self.consome(TOKEN.FLOAT)
            return TOKEN.FLOAT
        
        self.consome(TOKEN.STRING)
        return TOKEN.STRING
            
    #Var --> ident OpcValor
    def var(self, tipo_ident_declara: tuple[TOKEN,bool]) ->str:
        info_ident= self.tokenLido
        self.consome(TOKEN.ident)
        self.semantico.declaraVar(info_ident,tipo_ident_declara)
        atribuicao =self.opc_val(tipo_ident_declara)
        if  not atribuicao:
            if info_ident[0]== TOKEN.ident:
                type_ident=self.semantico.pegaTipoIdent(info_ident)
                if type_ident[0] == TOKEN.INT:
                    atribuicao= "=0"
                elif type_ident[0]== TOKEN.FLOAT:
                    atribuicao= "= 0.0"
                else:
                    atribuicao= "= \"\""
            else:
                if info_ident[0] == TOKEN.INT:
                    atribuicao= "=0"
                elif info_ident[0]== TOKEN.FLOAT:
                    atribuicao= "= 0.0"
                else:
                    atribuicao= "= \"\""

        return   "\n"+(" "*4)+info_ident[1] + atribuicao

    #OpcValor -> LAMBDA | = Exp
    def opc_val(self, type_ident: tuple[TOKEN,bool])-> str :
        if self.tokenLido[0] != TOKEN.atrib:
            return  ""
        
        token =self.tokenLido
        self.consome(TOKEN.atrib)
        type_opc= self.exp()
        if type_opc[0][0] != TOKEN.VOID   and type_opc[0][0] != type_ident[0]:
            self.semantico.erroSemantico(token , "Artibuição de tipos incompatível")

        return " = "+ type_opc[1]
    
    #ValPrim --> valint | valfloat | valstring
    def val_prim(self)-> tuple[tuple[TOKEN,bool],str]:
        lexema = self.tokenLido[1]
        if self.tokenLido[0] == TOKEN.valint:
            self.consome(TOKEN.valint) 
            return((TOKEN.INT, False),lexema)     
        elif self.tokenLido[0] == TOKEN.valfloat:
            self.consome(TOKEN.valfloat)
            return ((TOKEN.FLOAT, False),lexema)
        else :
            self.consome(TOKEN.valstring)
            return ((TOKEN.STRING, False), lexema)
            
       #  Comando -->  ComAtrib  | ComIf | ComFor | ComWhile 
       #             | ComReturn | ComContinue | ComBreak 
       #             | ComEntrada| ComSaida | ComBloco

    def  comando(self, type_retorno_func: tuple[TOKEN,bool]):
        if self.tokenLido[0] == TOKEN.ident:
            self.comando_atrib()
        elif self.tokenLido[0] == TOKEN.IF:
            self.comando_if(type_retorno_func)
        elif self.tokenLido[0] == TOKEN.FOR :
            self.comando_for(type_retorno_func)
        elif self.tokenLido[0] == TOKEN.FOREACH:
            self.comando_foreach(type_retorno_func)
        elif self.tokenLido[0] == TOKEN.WHILE:
            self.comando_while(type_retorno_func)
        elif self.tokenLido[0] == TOKEN.RETURN:
            self.comando_return(type_retorno_func)
        elif self.tokenLido[0]== TOKEN.CONTINUE:
            self.comando_continue()
        elif self.tokenLido[0] == TOKEN.BREAK:
            self.comando_break()
        elif self.tokenLido[0] == TOKEN.READ:
            self.comando_read()
        elif self.tokenLido[0] == TOKEN.WRITE:
            self.comando_write()
        else:
            self.bloco(type_retorno_func)
    
    # ComAtrib -> ident PosicaoOpc = Exp ;
    def comando_atrib(self):
        token=self.tokenLido
        self.consome(TOKEN.ident)
        type_ident=self.semantico.pegaTipoIdent(token)
        codigo_opc =self.posicao_opc(token)
        self.consome(TOKEN.atrib)
        type_exp=self.exp()
        if type_exp[0][0] != type_ident[0] :
            self.semantico.erroSemantico(token, "ERRO: :Atribuição de lista com tipos diferentes ")
        self.consome(TOKEN.ptoVirg)
        self.arquivo_alvo.write("\n"+((" "*4) * self.indentacao_atual)+token[1]+codigo_opc+"="+type_exp[1]+"\n")

    #PosicaoOpc -> LAMBDA | [ Exp ]
    def posicao_opc(self, token: tuple[TOKEN, str, int, int]) -> str:
        if self.tokenLido[0] != TOKEN.abreColchete:
            return ""
        
        self.consome(TOKEN.abreColchete)
        result_type_ident= self.semantico.pegaTipoIdent(token)
        if not result_type_ident[1] :
            self.semantico.erroSemantico(token,"Varivel não e do tipo lista")
        type_exp=self.exp()
        if  type_exp[0][0]  != TOKEN.VOID  and type_exp[0][0]  != TOKEN.INT:
            self.semantico.erroSemantico(token , "ERRO :Assigmentação errada de lista")
        self.consome(TOKEN.fechaColchete)
        return   "[("+type_exp[1]+"-1)]"

    #ComIf --> if ( Exp ) Comando OpcElse
    def comando_if(self, type_retorno_func: tuple[TOKEN,bool]):
        token = self.tokenLido
        self.consome(TOKEN.IF)
        self.consome(TOKEN.abrePar)
        type_exp=self.exp()
        if type_exp [0][0] != TOKEN.INT  or not type_exp[1]:
            self.semantico.erroSemantico(token , "ERRO : A codição não e do tipo booleano")
        self.consome(TOKEN.fechaPar)
        self.arquivo_alvo.write("\n" + (((" "*4)*self.indentacao_atual)+ "if "+ type_exp[1]+":"))
        self.indentacao_atual+=1
        self.comando(type_retorno_func)
        self.opc_else(type_retorno_func)

    #OpcElse -> LAMBDA | else Comando | elif ( Exp ) Comando OpcElse
    def opc_else(self, type_retorno_func: tuple[TOKEN,bool]):
        if self.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual)+"else:")
            self.indentacao_atual+=1
            self.comando(type_retorno_func)
        elif self.tokenLido[0] == TOKEN.ELIF:
            token = self.tokenLido
            self.consome(TOKEN.ELIF)
            self.consome(TOKEN.abrePar)
            type_exp=self.exp()
            if type_exp [0][0] != TOKEN.INT  or not type_exp[1] :
                self.semantico.erroSemantico(token , "ERRO : A codição não e do tipo booleano")
            self.consome(TOKEN.fechaPar)
            self.arquivo_alvo.write("\n"+((" " *4)*self.indentacao_atual)+"elif "+type_exp[1]+":")
            self.indentacao_atual+=1
            self.comando(type_retorno_func)
            self.opc_else(type_retorno_func)
        else:
            return

    #ComFor -> for ( ident = Exp ; Exp ; ident = Exp ) Comando
    def comando_for(self, type_retorno_func_func: tuple[TOKEN,bool]):
        self.consome(TOKEN.FOR)
        self.consome(TOKEN.abrePar)
        token_ident=self.tokenLido
        type_ident=self.semantico.pegaTipoIdent(token_ident)
        self.consome(TOKEN.ident)
        self.consome(TOKEN.atrib)
        token=self.tokenLido
        type_exp_1=self.exp()
        if type_exp_1[0][0] != type_ident[0]:
            self.semantico.erroSemantico(token,"Erro: atribuição de tipos não compativeis")
        self.consome(TOKEN.ptoVirg)
        token=self.tokenLido
        type_exp_2=self.exp()
        if type_exp_2[0][0] != TOKEN.INT  or not type_exp_2[1]:
            self.semantico.erroSemantico(token , "ERRO : A codição não e do tipo booleano")
        self.consome(TOKEN.ptoVirg)
        token=self.tokenLido
        type_ident=self.semantico.pegaTipoIdent(token)
        self.consome(TOKEN.ident)
        self.consome(TOKEN.atrib)
        type_exp_3=self.exp()
        if type_exp_3[0][0] != type_ident[0]:
            self.semantico.erroSemantico(token,"Erro: atribuição de tipos não compativeis")
        self.consome(TOKEN.fechaPar)
        self.arquivo_alvo.write("\n"+((" "*4) *self.indentacao_atual)+token_ident[1]+" = "+type_exp_1[1]+
                                "\n"+((" "*4)*self.indentacao_atual)+"while " + type_exp_2[1]+":" )
        self.indentacao_atual+=1
        self.comando(type_retorno_func_func)
        self.arquivo_alvo.write("\n"+((" "*4) *(self.indentacao_atual+1))+token[1]+" = "+type_exp_3[1])

    #ComForeach -> foreach ident = Exp : Comando
    def comando_foreach(self, type_retorno_func: tuple[TOKEN,bool], ):
        self.consome(TOKEN.FOREACH)
        token= self.tokenLido
        type_ident= self.semantico.pegaTipoIdent(token)
        self.consome(TOKEN.ident)
        self.consome(TOKEN.atrib)
        type_exp= self.exp()
        if not type_exp[0][1]:
            self.semantico.erroSemantico(token,"Erro a varivel não e do tipo lista")
        if type_exp[0][0] != type_ident[0]:
            self.semantico.erroSemantico(token,"Erro  atribuição de tipos não compativeis")
        
        if not type_exp[1]:
            self.semantico.erroSemantico(token,"Erro:  Não tem um objeto iterável")

        self.consome(TOKEN.doisPontos)

        self.arquivo_alvo.write("\n"+ (" "*4) *self.indentacao_atual +"for " +token[1]+ " in "+ type_exp[1]+":"  )
        self.indentacao_atual+=1
        self.comando(type_retorno_func)
    
    #  ComWhile -> while ( Exp ) Comando
    def comando_while(self, type_retorno_func: tuple[TOKEN,bool]):
        token =self.tokenLido
        self.consome(TOKEN.WHILE)
        self.consome(TOKEN.abrePar)
        type_exp=self.exp()
        if type_exp [0][0] != TOKEN.INT  or type_exp[0][1] :
            self.semantico.erroSemantico(token , "ERRO : A codição do while não e do tipo booleano")
        self.consome(TOKEN.fechaPar)

        self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual)+"while ( "+type_exp[1]+" ):")
        self.indentacao_atual+=1
        self.comando(type_retorno_func)
    
    #ComReturn -> return OpcRet ;
    def comando_return(self, type_retorno_func: tuple[TOKEN,bool]):
        self.consome(TOKEN.RETURN)
        codigo_opc=self.opc_ret(type_retorno_func)
        self.consome(TOKEN.ptoVirg)
        self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual)+"return "+ codigo_opc )

    #OpcRet -> LAMBDA | Exp
    def opc_ret(self, type_retorno_func: tuple[TOKEN,bool])->str:
        if self.tokenLido[0] == TOKEN.ptoVirg:
            return ""
        
        token =self.tokenLido
        type_exp =self.exp()
        if type_retorno_func != type_exp[0]:
            self.semantico.erroSemantico(token, f"retorno da função não é do tipo esperado ({type_exp}), encontrado {type_retorno_func}")
        
        return type_exp[1]
    
    #  ComContinue -> continue ;
    def comando_continue(self):
        self.consome(TOKEN.CONTINUE)
        self.consome(TOKEN.ptoVirg)
        self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual) + "continue")
    
    #ComBreak -> break ;
    def comando_break(self):
        self.consome(TOKEN.BREAK)
        self.consome(TOKEN.ptoVirg) 
        self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual) + "break")
    
    #   ComEntrada -> read ( ident ) ;
    def comando_read(self):
        self.consome(TOKEN.READ)
        self.consome(TOKEN.abrePar)
        token = self.tokenLido
        self.consome(TOKEN.ident)
        type_ident=self.semantico.pegaTipoIdent(token)
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
        if type_ident[1]:
            self.semantico.erroSemantico(token,"Erro :variavel e do tipo lista ")

        if type_ident[0]== TOKEN.INT:
            self.arquivo_alvo.write("\n"+ ((" "*4)*self.indentacao_atual) +token[1]+ "="+"int(input().strip())")
            return
        if type_ident[0] == TOKEN.FLOAT:
            self.arquivo_alvo.write("\n"+ ((" "*4)*self.indentacao_atual) +token[1]+ "="+"float(input().strip())")
            return

        self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual)+token[1]+"input().strip()")

    #  ComSaida -> write ( ListaOubt ) ;
    def comando_write(self):
        self.consome(TOKEN.WRITE)
        self.consome(TOKEN.abrePar)
        codigo_lista_out=self.lista_out()
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
        self.arquivo_alvo.write("\n"+((" "*4)*self.indentacao_atual)+"print("+codigo_lista_out+",end= \"\" )")

    def parse_saida_elemento(self) -> str:
        token = self.tokenLido
        info_exp = self.exp()
        if info_exp[0][1]:
            self.semantico.erroSemantico(token, "Erro: variável é do tipo lista")
        return info_exp[1]
    
    #ListaOut -> Exp RestoListaOut
    #RestoListaOut -> LAMBDA | , ListaOut 
    def lista_out(self) -> str:
        elementos: list[str] = []
        elementos.append(self.parse_saida_elemento())
        
        while self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            elementos.append(self.parse_saida_elemento())
    
        return ", ".join(elementos)
        
    #ComBloco -> { ListaComando }
    def bloco(self, type_retorno_func ):
        self.consome(TOKEN.abreChave)
        self.lista_comando(type_retorno_func)
        self.indentacao_atual-=1
        self.consome(TOKEN.fechaChave)

    # Folha -> ValPrim | ident Recorte | ident ( ListaArgs ) | ( Exp ) | [ ListaExp ]
    def folha(self) -> tuple [tuple[TOKEN,bool], str]:
        if self.tokenLido[0] == TOKEN.ident:
            token= self.tokenLido
            if self.semantico.isIdentFunc(token[1]):
                info=self.semantico.pegaInfoFunc(token)
                self.consome(TOKEN.ident)
                self.consome(TOKEN.abrePar)
                codigo =self.list_args(token[1] + "(",info[1])
                self.consome(TOKEN.fechaPar)
                return (info[0], codigo+")")
            
            self.consome(TOKEN.ident)

            tipo_ident=self.semantico.pegaTipoIdent(token)
            return self.recorte(tipo_ident, token[1])
        
        elif self.tokenLido[0] == TOKEN.abrePar:
            self.consome(TOKEN.abrePar)
            tipo =self.exp()
            self.consome(TOKEN.fechaPar) 
            return tipo
        elif self.tokenLido[0] == TOKEN.abreColchete:
            self.consome(TOKEN.abreColchete)
            tipo =self.lista_exp()
            self.consome(TOKEN.fechaColchete)
            return (tipo[0],"["+ tipo[1] +"]")
        else:
            return self.val_prim()
            
    #ListaExp -> LAMBDA | Exp OpcListaExp
    def lista_exp(self) ->tuple [tuple[TOKEN,bool], str]:
        if self.tokenLido[0] == TOKEN.fechaColchete:
            return ((TOKEN.VOID, True),"")
        
        token =self.tokenLido
        tipo_1=self.exp()
        if tipo_1[0][1] :
            self.semantico.erroSemantico(token,"Erro não e permitido lista de lista")

        return self.opc_lista_exp(((tipo_1[0][0],True),tipo_1[1]))
    
    #OpcListaExp -> LAMBDA | , Exp OpcListaExp
    def opc_lista_exp(self,tipo_1:  tuple [tuple[TOKEN,bool], str])-> tuple [tuple[TOKEN,bool], str]:
        if self.tokenLido[0] != TOKEN.virg:
            return  tipo_1
        
        self.consome(TOKEN.virg)
        token= self.tokenLido
        tipo_2=self.exp()
        if tipo_2[0][1] :
            self.semantico.erroSemantico(token,"Erro não e permitido lista de lista")
        if tipo_1[0][0] != tipo_2[0][0]:
            self.semantico.erroSemantico(token,"Lista  teve conter o mesmo tipo")

        return self.opc_lista_exp((tipo_1[0],tipo_1[1]+","+tipo_2[1]))
   
    #Recorte -> LAMBDA | [ Dentro ]
   # LISTA[2:5]  -> lista = lista[(2-1):(5-1)]
    #Lista[:5] -> lista= [:(5-1)]
    def recorte(self,  tipo_variavel:tuple[TOKEN,bool], codigo:str)-> tuple [tuple[TOKEN,bool], str]:
        if self.tokenLido[0] != TOKEN.abreColchete :
            return (tipo_variavel, codigo)
        
        if not tipo_variavel[1]:
            self.semantico.erroSemantico(self.tokenLido,"A variavel não é do tipo lista") 

        self.consome(TOKEN.abreColchete)
        type_dentro=self.dentro(codigo+"[(")
        self.consome(TOKEN.fechaColchete)
        return (type_dentro[0], type_dentro[1]+"-1)]")
        
    #Dentro -> Exp RestoDentro | : OpcInt
    def  dentro(self,codigo:str) ->  tuple [tuple[TOKEN,bool], str]:
        if self.tokenLido[0]==TOKEN.doisPontos:
            self.consome(TOKEN.doisPontos)
            if not codigo:
                result_codigo =self.opc_int(codigo+":")
            else:
                result_codigo =self.opc_int("("+codigo+"-1)"+":")
            return ((TOKEN.INT,True), result_codigo)
    
        token =self.tokenLido
        tipo_codigo =self.exp()
        if tipo_codigo[0][0] != TOKEN.INT:
            self.semantico.erroSemantico(token, "variavel do tipo errado")
        return self.resto_dentro( codigo+tipo_codigo[1])

    #RestoDentro -> LAMBDA | : OpcInt
    def resto_dentro(self, codigo_atual : str) ->  tuple [tuple[TOKEN,bool], str]:
        if self.tokenLido[0] != TOKEN.doisPontos:
            return ((TOKEN.INT,False), codigo_atual)
        
        self.consome(TOKEN.doisPontos)
        result=self.opc_int(codigo_atual+":")
        return ((TOKEN, True), result)
        
    #OpcInt -> LAMBDA | Exp
    def opc_int(self, codigo_atual : str)-> str:
        if self.tokenLido[0] == TOKEN.doisPontos  or self.tokenLido[0] == TOKEN.virg:
            return codigo_atual 
        
        tipo =self.exp()
        if tipo[0][0] != TOKEN.INT:
            self.semantico.erroSemantico(self.tokenLido, "variavel do tipo errado")
        return codigo_atual + tipo[1]
 
    # ListaArgs -> LAMBDA | Exp RestoListaArgs
    #lambda == ) e por causa da tabela predict 
    def  list_args(self,parameter_fuction:str, list_tipo_args: list[tuple[TOKEN, bool]]) ->  str:
        if  self.tokenLido[0] == TOKEN.fechaPar:
            return  parameter_fuction

        token= self.tokenLido
        info_codigo =self.exp() 
        if list_tipo_args[0][1] != info_codigo[0]:
            return self.semantico.erroSemantico(token,"Erro foi passado um tipo errado para função")

        return self.resto_lista_args(parameter_fuction + info_codigo[1],list_tipo_args.pop(0))

    # RestoListaArgs -> lambda | , Exp RestoListaArgs
    def resto_lista_args(self, parameter_fuction: str, list_tipo_args: list[tuple[TOKEN, bool]])-> str:
        if self.tokenLido[0] != TOKEN.virg:
            return parameter_fuction
        
        self.consome(TOKEN.virg)
        token= self.tokenLido
        info_codigo=self.exp()    
        if list_tipo_args[0] != info_codigo[0][0]:
            return self.semantico.erroSemantico(token,"Erro foi passado um tipo errado para função")

        self.resto_lista_args(parameter_fuction+ "," +info_codigo[1] ,list_tipo_args.pop(0))

    #Uno -> + Uno | - Uno | Folha 
    def uno(self) ->  tuple [tuple[TOKEN,bool], str]:
        operadores: list[TOKEN] = []
        tokens_info: list[tuple[TOKEN, str, int, int]] = []

        while self.tokenLido[0] in (TOKEN.mais, TOKEN.menos):
            operadores.append(self.tokenLido[0])
            tokens_info.append(self.tokenLido)
            self.consome(self.tokenLido[0])

        tipo, codigo = self.folha()  
        if tipo[0] == TOKEN.INT:
            try:
                number = int(codigo)
                for operador, info in reversed(list(zip(operadores, tokens_info))):
                    tipo = self.semantico.operacao_unaria(operador, tipo, info)
                    if operador == TOKEN.menos:
                        number = -number
                return tipo, str(number)
            except ValueError:
                # mesmo sendo tipo INT, o valor pode ser uma variável como "x"
                for operador in reversed(operadores):
                    op_str = "-" if operador == TOKEN.menos else "+"
                    codigo = f"({op_str}{codigo})"
                    tipo = self.semantico.operacao_unaria(operador, tipo, tokens_info[0])
                return tipo, codigo
        else:
            for operador in reversed(operadores):
                op_str = "-" if operador == TOKEN.menos else "+"
                codigo = f"({op_str}{codigo})"
                tipo = self.semantico.operacao_unaria(operador, tipo, tokens_info[0])
            return tipo, codigo
        
    # Mult -> Uno RestoMult
    def mult(self)-> tuple [tuple[TOKEN,bool], str]:
        type_atual= self.uno()
        return self.resto_mult(type_atual)

    # RestoMult -> LAMBDA | * Uno RestoMult | / Uno RestoMult
    # RestoMult -> mod Uno RestoMult | div Uno RestoMulT
    def resto_mult(self, type_esquerd: tuple[tuple[TOKEN, bool], str]) -> tuple[tuple[TOKEN, bool], str]:
        tipo_atual = type_esquerd[0]
        codigo_atual = type_esquerd[1]

        while self.tokenLido[0] in (TOKEN.multiplica, TOKEN.divide, TOKEN.MOD, TOKEN.DIV):
            operador = self.tokenLido[0]
            info_token = self.tokenLido
            self.consome(operador)
            tipo_direita, codigo_direita = self.uno()

            tipo_atual = self.semantico.operacao_binaria(info_token, operador, tipo_atual, tipo_direita)
            if operador == TOKEN.multiplica:
                codigo_atual += "*" + codigo_direita
            elif operador == TOKEN.divide:
                codigo_atual += "/" + codigo_direita
            elif operador == TOKEN.MOD:
                codigo_atual += "%" + codigo_direita
            elif operador == TOKEN.DIV:
                codigo_atual += "//" + codigo_direita
        return tipo_atual, codigo_atual
    
    # Soma -> Mult RestoSoma
    def soma(self)-> tuple [tuple[TOKEN,bool], str]:
        type_atual= self.mult()
        return self.resto_soma(type_atual)
    
    #RestoSoma -> LAMBDA | + Mult RestoSoma | - Mult RestoSoma
    def resto_soma(self,type_esquerd: tuple[tuple[TOKEN,bool], str]) -> tuple[tuple[TOKEN,bool], str]:
        tipo_atual = type_esquerd[0]
        codigo_atual = type_esquerd[1]

        while self.tokenLido[0] in (TOKEN.mais, TOKEN.menos):
            operador = self.tokenLido[0]
            info_token = self.tokenLido
            self.consome(operador)
            tipo_direita, codigo_direita = self.mult()

            tipo_atual = self.semantico.operacao_binaria(info_token, operador, tipo_atual, tipo_direita)

            if operador == TOKEN.mais:
                codigo_atual += "+" + codigo_direita
            else:
                codigo_atual += "-" + codigo_direita

        return tipo_atual, codigo_atual
        
    #Rel -> Soma RestoRel
    def rel(self)->  tuple [tuple[TOKEN,bool], str]:
        type_esq=self.soma()
        return self.resto_rel(type_esq)

    #RestoRel -> LAMBDA | == Soma | != Soma
    #RestoRel -> <= Soma | >= Soma | > Soma | < Soma
    def resto_rel(self, type_esquerd :tuple[tuple[TOKEN,bool], str]) ->tuple[tuple[TOKEN,bool], str]:

        if self.tokenLido[0] == TOKEN.igual:
            info_token= self.tokenLido
            self.consome(TOKEN.igual)
            type_dir=self.soma()
            return (self.semantico.operacao_binaria(info_token,TOKEN.igual, type_esquerd[0],type_dir[0]), type_esquerd[1] +"==" +type_dir[1] )
        if self.tokenLido[0] == TOKEN.diferente:
            info_token= self.tokenLido
            self.consome(TOKEN.diferente)
            type_dir=self.soma()
            return (self.semantico.operacao_binaria(info_token,TOKEN.diferente, type_esquerd[0],type_dir[0]), type_esquerd[1] +"!=" +type_dir[1])
        if self.tokenLido[0] ==TOKEN.menorIgual:
            info_token= self.tokenLido
            self.consome(TOKEN.menorIgual)
            type_dir=self.soma()
            return (self.semantico.operacao_binaria(info_token,TOKEN.menorIgual, type_esquerd[0],type_dir[0]), type_esquerd[1] +"<=" +type_dir[1] )
        if self.tokenLido[0] == TOKEN.maiorIgual:
            info_token= self.tokenLido
            self.consome(TOKEN.maiorIgual)
            type_dir=self.soma()
            return (self.semantico.operacao_binaria(info_token,TOKEN.maiorIgual, type_esquerd[0],type_dir[0]), type_esquerd[1] +">=" +type_dir[1] )
        if self.tokenLido[0] == TOKEN.maior:
            info_token= self.tokenLido
            self.consome(TOKEN.maior)
            type_dir=self.soma()
            return (self.semantico.operacao_binaria(info_token,TOKEN.maior, type_esquerd[0],type_dir[0]),  type_esquerd[1] +">" +type_dir[1] )
        if self.tokenLido[0] == TOKEN.menor:
            info_token= self.tokenLido
            self.consome(TOKEN.menor)
            type_dir=self.soma()
            return (self.semantico.operacao_binaria(info_token,TOKEN.menor, type_esquerd[0],type_dir[0]), type_esquerd[1] +"<" +type_dir[1] )
        
        return  type_esquerd

    # Nao -> not Nao | Rel
    def nao(self) -> tuple[tuple[TOKEN, bool], str]:
        operadores: list[TOKEN] = []
        tokens_info: list[tuple[TOKEN, str, int, int]] = []

        while self.tokenLido[0] == TOKEN.NOT:
            operadores.append(self.tokenLido[0])
            tokens_info.append(self.tokenLido)
            self.consome(TOKEN.NOT)

        tipo, codigo = self.rel() 
        for operador, info in reversed(list(zip(operadores, tokens_info))):
            tipo = self.semantico.operacao_unaria(operador, tipo, info)
            codigo = f" not {codigo}"

        return tipo, codigo

    # Junc -> Nao RestoJunc
    def junc(self) ->  tuple [tuple[TOKEN,bool], str]:
        type_esquerd=self.nao()
        return self.resto_junc(type_esquerd)

    #RestoJunc -> LAMBDA | and Nao RestoJunc
    def resto_junc(self, type_esquerd: tuple[tuple[TOKEN, bool], str]) -> tuple[tuple[TOKEN, bool], str]:
        tipo_atual = type_esquerd[0]
        codigo_atual = type_esquerd[1]

        while self.tokenLido[0] == TOKEN.AND:
            info_token = self.tokenLido
            self.consome(TOKEN.AND)
            tipo_direita, codigo_direita = self.nao()

            tipo_atual = self.semantico.operacao_binaria(info_token, TOKEN.AND, tipo_atual, tipo_direita)
            codigo_atual += " and " + codigo_direita

        return tipo_atual, codigo_atual

    #Exp -> Junc RestoExp
    def exp(self)-> tuple [tuple[TOKEN,bool], str]:
        type_esquerd =self.junc()
        return self.resto_exp(type_esquerd)
    
    #RestoExp -> LAMBDA | or Junc RestoExp
    def resto_exp(self, type_esquerda: tuple [tuple[TOKEN,bool], str])-> tuple [tuple[TOKEN,bool], str]:
        tipo_atual = type_esquerda[0]
        codigo_atual = type_esquerda[1]

        while self.tokenLido[0] == TOKEN.OR:
            info_token = self.tokenLido
            self.consome(TOKEN.OR)
            tipo_direita, codigo_direita = self.junc()

            tipo_atual = self.semantico.operacao_binaria(info_token, TOKEN.OR, tipo_atual, tipo_direita)
            codigo_atual += " or " + codigo_direita

        return tipo_atual, codigo_atual


