from enum import IntEnum
class TOKEN(IntEnum):

    erro = 1
    eof = 2
    ident = 3
    abreColchete=4
    fechaColchete=5
    doisPontos=6
    INT =7
    FLOAT =8
    STRING=9
    IF = 10
    ELSE =11
    WHILE = 12
    FOR = 13
    FOREACH = 14
    CONTINUE=15
    BREAK=16
    VOID=17
    RETURN = 18
    abrePar = 19
    fechaPar = 20
    virg = 21
    ptoVirg = 22
    igual = 23
    diferente = 24
    menor = 25
    menorIgual = 26
    maior = 27
    maiorIgual = 28
    AND = 29
    OR = 30
    NOT = 31
    mais = 32
    menos = 33
    multiplica = 34
    divide = 35
    MOD=36
    DIV=37
    READ = 38
    WRITE = 39
    abreChave = 40
    fechaChave = 41
    ELIF=42
    comentario=43
    atrib=44
    valint=45
    valfloat=46
    valstring=47
    func=48

    @classmethod
    def msg(cls, token):
        nomes = {
            1:'erro',
            2:'<eof>',
            3:'ident',
            4:'[',
            5:']',
            6:':',
            7:'int',
            8:'float',
            9:'string',
            10:'if',
            11:'else',
            12:'while',
            13:'for',
            14:'foreach',
            15:'continue',
            16:'break',
            17:'void',
            18:'return',
            19:'(',
            20:')',
            21:',',
            22:';',
            23:'==',
            24:'!=',
            25:'<',
            26:'<=',
            27:'>',
            28:'>=',
            29:'and',
            30:'or',
            31:'not',
            32:'+',
            33:'-',
            34:'*',
            35:'/',
            36:'mod',
            37:'div',
            38:'read',
            39:'write',
            40:'{',
            41:'}',
            42:'elif',
            43:'#',
            44: '=',
            45:'numero inteiro',
            46:'numero flutuante',
            47:'string',
            48:'função'
        }
        return nomes[token]
    
    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'int': TOKEN.INT,
            'float': TOKEN.FLOAT,
            'string': TOKEN.STRING,
            'if': TOKEN.IF,
            'else': TOKEN.ELSE,
            'elif': TOKEN.ELIF,
            'while': TOKEN.WHILE,
            'for': TOKEN.FOR,
            'foreach': TOKEN.FOREACH,
            'continue': TOKEN.CONTINUE,
            'read': TOKEN.READ,
            'write': TOKEN.WRITE,
            'break': TOKEN.BREAK,
            'void': TOKEN.VOID,
            'return': TOKEN.RETURN,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT,
            'mod':TOKEN.MOD,
            'div': TOKEN.DIV
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
