from random import random
import matplotlib.pyplot as plt
import math

class Individuo():
    def __init__(self, num_bit, limite, geracao=0):
        self.limite = limite
        self.num_bit = num_bit
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.cromossomo = []
        for i in range(num_bit):
            if random() < 0.5:
                self.cromossomo.append("0")
            else: 
                self.cromossomo.append("1")
    def bin_to_dec(self, num):
        newList = list(reversed(num))
        soma = 0
        for i in range(len(newList)):
            soma += pow(2,i)*int(newList[i])
            
        return soma
    
    def avaliacao(self, functionX, functionY):
        nota = 0
        denominador = pow((1 + 0.001*(pow(functionX, 2) + pow(functionY, 2))), 2)
        nota = round(0.5 - (pow(math.sin(math.sqrt(pow(functionX, 2) + pow(functionY, 2))),2)-0.5)/denominador, 4)
        if nota > self.limite:
            nota = 0.0001
        self.nota_avaliacao = nota
        
            
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
            
        filhos = [Individuo(self.num_bit, self.limite, self.geracao+1), Individuo(self.num_bit, self.limite, self.geracao+1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else: 
                    self.cromossomo[i] = '1'
        return self
        
class AlgoritmoGenetico():
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializa_populacao(self, num_bit, limite):
        for i in range (self.pop_size):
            self.populacao.append(Individuo(num_bit, limite))
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao, reverse = True)
        
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai +=1
            i += 1
        return pai
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
        
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G: %s \nF6: %s" %(self.populacao[0].geracao, melhor.nota_avaliacao))
        
    def resolver(self, taxa_mutacao, num_ger, num_bit, limite):
        self.inicializa_populacao(num_bit, limite)
        particionar = num_bit//2
        for individuo in self.populacao:
            x = individuo.cromossomo[0:particionar]
            y = individuo.cromossomo[particionar::]
            numberX = individuo.bin_to_dec(x)
            numberY = individuo.bin_to_dec(y)
            functionX = round(numberX*200/(pow(2,22) - 1) - 100, 4)
            functionY = round(numberY*200/(pow(2,22) - 1) - 100, 4)
            individuo.avaliacao(functionX, functionY)
            
        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        for geracao in range(num_ger):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0,self.pop_size, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                numx = individuo.cromossomo[0:particionar]
                numy = individuo.cromossomo[particionar::]
                numberXX = individuo.bin_to_dec(numx)
                numberYY = individuo.bin_to_dec(numy)
                functionXX = round(numberXX*200/(pow(2,22) - 1) - 100, 4)
                functionYY = round(numberYY*200/(pow(2,22) - 1) - 100, 4)
                individuo.avaliacao(functionXX, functionYY)
                
            self.ordena_populacao()
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
            
        print("\nMelhor solucao -> G: %s F6: %s" % 
              (self.melhor_solucao.geracao, 
               self.melhor_solucao.nota_avaliacao))
        
        return self.melhor_solucao
            
    
if __name__ == '__main__':
    limite = 1.0001
    pop_size = 100
    num_ger = 40
    taxa_mutacao = 0.008
    num_bit = 44
    ag = AlgoritmoGenetico(pop_size)
    
    resultado = ag.resolver(taxa_mutacao, num_ger, num_bit, limite)
    
    
    plt.plot(ag.lista_solucoes)
    plt.title("Valores")
    plt.show()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        