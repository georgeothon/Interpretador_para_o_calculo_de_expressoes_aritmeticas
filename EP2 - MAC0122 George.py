
"""
@author: georgeothon
"""

def TraduzPosFixa(exp):
    
    operadores = ['=','-','+','/','*','**','_','#']
    StrAuxiliar = ''
    pos = []
    pilha = []

    
    #Transforma em lista
    for k in range(len(exp)):
        if exp[k] in operadores or exp[k] in ['(',')']:
            aux = ' '+str(exp[k])+' '
            StrAuxiliar += aux
        else:
            StrAuxiliar += str(exp[k])
    ListaAuxiliar = StrAuxiliar.split()
    
    #Trata operadores unario e multiplicacao 
    i = 0
    while i <= ListaAuxiliar.index(ListaAuxiliar[-1]):
        
        if i == 0 :
            #Substitui operadores na primeira string
            if ListaAuxiliar[0] == '+': ListaAuxiliar[0] = '#'
            elif ListaAuxiliar[0] == '-': ListaAuxiliar[0] = '_'
                
        #Substitui o operador caso o elemnto anterior seja operador
        elif ListaAuxiliar[i] == '+' and ( ListaAuxiliar[ i - 1 ] in operadores or ListaAuxiliar[ i - 1 ] == '(' ): 
            ListaAuxiliar[i] = '#'

        elif ListaAuxiliar[i] == '-' and ( ListaAuxiliar[ i - 1 ] in operadores or ListaAuxiliar[ i - 1 ] == '(' ): 
            ListaAuxiliar[i] = '_'                                  
        
        #Encontra operadores exponenciais
        if i != 0 and ListaAuxiliar[i] == '*':
            if ListaAuxiliar[ i + 1 ] == '*':
                ListaAuxiliar[i] = '**'
                ListaAuxiliar.pop( i + 1 )
            
        i += 1
    
    #Traducao
    while ListaAuxiliar != []:
        
        #Altera prioridade
        if ListaAuxiliar[0] == '(':
            pilha.append(ListaAuxiliar[0])
            ListaAuxiliar.pop(0)
            
        elif ListaAuxiliar[0] == ')':
            while pilha[-1] != '(':
                pos.append(pilha[-1])
                pilha.pop()
            pilha.pop()
            ListaAuxiliar.pop(0)       
        
        #Verifica se é operando
        elif ListaAuxiliar[0] not in operadores:
            pos.append(ListaAuxiliar[0])
            
            #Verifica se a lista possui apenas um elemento
            if len(ListaAuxiliar) > 1 : ListaAuxiliar.pop(0)
            else: ListaAuxiliar = []
            
        #Encontra operadores
        elif ListaAuxiliar[0] in operadores:
            
            if pilha == []:
                pilha.append(ListaAuxiliar[0])
                ListaAuxiliar.pop(0)
            else:
                pilha,pos = EmpilhaOperadores(pilha,ListaAuxiliar[0],pos)
                ListaAuxiliar.pop(0)
    
    while pilha != [] :
        pos.append(pilha[-1])
        pilha.pop()
        
    return pos


def EmpilhaOperadores(pilha,e,pos):
    
    operadores = ['=','-','+','/','*','**','_','#']
    prioridade = [ 0,  1,  1,  2,  2,  3,   4,  4 ]
    
    if pilha != [] and pilha[-1] != '(':
        
        #Encontra o indice do topo da pilha e do elemento a ser adicionado
        indice_e = operadores.index(e)
        indice_topo = operadores.index(pilha[-1])

        #Verifica qual tem a maior prioridade
        if prioridade[indice_e] > prioridade[indice_topo]:
            pilha.append(e)
    
        #Desempilha casa prioridade do topo seja menor que a do elemento
        else:
            pos.append(pilha[-1])
            pilha.pop()
            EmpilhaOperadores(pilha,e,pos)
        
    #Testa se a pilha esta vazia
    elif pilha == [] or pilha[-1] == '(': 
        pilha.append(e)
    
    return pilha, pos


def CalcPosFixa(listaexp):
    
    operadores = ['=','-','+','/','*','**','_','#']
    pilha = []
    
    #Percorre a lista para encontrar os operadores
    for i in listaexp:
        if i in operadores:
            #Verifica se e unario:
            if i == '_':
                pilha[-1] = - pilha[-1]
                
            #Realiza as operacoes
            elif i == '+':
                operando_b = float(pilha.pop())
                operando_a = float(pilha.pop())
                pilha.append( operando_a + operando_b )
                
            elif i == '-':
                operando_b = float(pilha.pop())
                operando_a = float(pilha.pop())
                pilha.append( operando_a - operando_b )
                
            elif i == '/':
                operando_b = float(pilha.pop())
                operando_a = float(pilha.pop())
                pilha.append( operando_a / operando_b )
                
            elif i == '*':
                operando_b = float(pilha.pop())
                operando_a = float(pilha.pop())
                pilha.append( operando_a * operando_b )
                
            elif i == '**':
                operando_b = float(pilha.pop())
                operando_a = float(pilha.pop())
                pilha.append( operando_a ** operando_b )
                
            elif i == '_':
                operando = float(pilha.pop())
                pilha.append( - operando )
                
            elif i == '#':
                pilha.pop()
                
        else:
            pilha.append(i)
        
                
    return pilha[0]

def main():
    
    operadores = ['=','-','+','/','*','**','_','#']
    TabVar = []
    TabVal = []
    
    Validacao = 0
    
    while True :
        
        entrada  = input('>>> ')
        
        PosFixa = TraduzPosFixa(entrada)
        
        #Verifica se uma variavel recebe o resultado
        if '=' in PosFixa:
            #Separa a expressao para calcular
            expressao = PosFixa[1:-1]
        else:
            expressao = PosFixa
            
            
        #Atribui valor para as variaveis
        for k in expressao:
            if k in TabVar:
                expressao[expressao.index(k)] = TabVal[TabVar.index(k)]
        
        #Verifica se todas as variaveis est]ao definidas
        for l in expressao:
            if l not in operadores and l not in TabVal:
                try:
                    float(l)
                    Validacao = 1
                    break
                
                except:
                    print('NameError: name ',l,' is not defined')
                    
            else:
                Validacao = 1
        
        if Validacao == 1:
            
            #Calcula pos fixa
            resultado = CalcPosFixa(expressao)            
                
            #Verifica se o elemento ja esta na tabela de variaveis
            if PosFixa[0] not in TabVar and PosFixa != expressao:
                TabVar.append(PosFixa[0])
                TabVal.append(resultado)
                    
            #Muda o valor da variavel caso ela ja esteja na TabVar   
            elif PosFixa[0] in TabVar and PosFixa != expressao:
                indice_resposta = TabVar.index(PosFixa[0])
                TabVal[indice_resposta] = resultado
                
            if '=' not in PosFixa:
                
                count = 0
                for i in operadores:
                    if i in PosFixa:
                        count = 1
                        
                        try:
                            print(resultado)
                        except:
                            print(TabVal[TabVar.index(resultado)])
                        break
                try:    
                    if count == 0 :
                        
                        indice_variavel = TabVar.index(PosFixa[0])
                        saida = TabVal[indice_variavel]
                        print(saida)
                except:
                    try:
                        print(float(resultado))
                    except:    
                        print('NameError: name ',resultado,' is not defined')
                
        Validacao = 0
            
                
main()
