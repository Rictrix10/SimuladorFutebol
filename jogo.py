import csv
import random
import time

class Equipe:
    def __init__(self, nome, pais, rank):
        self.nome = nome
        self.pais = pais
        self.rank = rank
        self.pontos = 0

class Jogo:
    def __init__(self, equipe_casa, equipe_visitante):
        self.equipe_casa = equipe_casa
        self.equipe_visitante = equipe_visitante
        self.placar_casa = 0
        self.placar_visitante = 0
        self.resultado_final = ""

    def calcular_probabilidade_gol(self, equipe):
        # Quanto maior o rank, maior a probabilidade de marcar um gol
        return equipe.rank / 5000

    def jogar(self, mostrar_minutos):
        if mostrar_minutos:
            print(f"{self.equipe_casa.nome} vs {self.equipe_visitante.nome}")
            print("Minuto  |  Placar")
            print("-----------------")

        for minuto in range(90):
            probabilidade_casa = self.calcular_probabilidade_gol(self.equipe_casa)
            probabilidade_visitante = self.calcular_probabilidade_gol(self.equipe_visitante)

            if random.random() < probabilidade_casa:  # Probabilidade de gol da equipe da casa
                self.placar_casa += 1
            if random.random() < probabilidade_visitante:  # Probabilidade de gol da equipe visitante
                self.placar_visitante += 1

            if mostrar_minutos:
                print(f"{minuto+1:>6}  |  {self.placar_casa} - {self.placar_visitante}")

        if self.placar_casa > self.placar_visitante:
            self.equipe_casa.pontos += 3
            self.resultado_final = f"{self.equipe_casa.nome} {self.placar_casa} - {self.placar_visitante} {self.equipe_visitante.nome}"
        elif self.placar_casa < self.placar_visitante:
            self.equipe_visitante.pontos += 3
            self.resultado_final = f"{self.equipe_casa.nome} {self.placar_casa} - {self.placar_visitante} {self.equipe_visitante.nome}"
        else:
            self.equipe_casa.pontos += 1
            self.equipe_visitante.pontos += 1
            self.resultado_final = f"{self.equipe_casa.nome} {self.placar_casa} - {self.placar_visitante} {self.equipe_visitante.nome}"

    def exibir_resultado_final(self):
        print(self.resultado_final)

class Campeonato:
    def __init__(self, equipes):
        self.equipes = equipes

    def gerar_agendamento_jogos(self):
        agendamento_jogos = []
        for i in range(len(self.equipes)):
            for j in range(i + 1, len(self.equipes)):
                equipe_casa = self.equipes[i]
                equipe_visitante = self.equipes[j]
                agendamento_jogos.append((equipe_casa, equipe_visitante))
        return agendamento_jogos

    def jogar_rodada(self):
        agendamento_jogos = self.gerar_agendamento_jogos()
        random.shuffle(agendamento_jogos)  # Embaralhar a ordem dos jogos

        jogos_realizados = set()
        for equipe_casa, equipe_visitante in agendamento_jogos:
            if equipe_casa.nome in jogos_realizados or equipe_visitante.nome in jogos_realizados:
                continue  # Pula o jogo se alguma das equipes já jogou nessa rodada

            jogo = Jogo(equipe_casa, equipe_visitante)
            mostrar_minutos = obter_opcao_mostrar_minutos(equipe_casa, equipe_visitante)
            jogo.jogar(mostrar_minutos)
            jogos_realizados.add(equipe_casa.nome)
            jogos_realizados.add(equipe_visitante.nome)

            if mostrar_minutos:
                jogo.exibir_resultado_final()
            else:
                jogo.exibir_resultado_final()
                print()  # Pula uma linha entre os jogos

    def exibir_classificacao(self):
        classificacao = sorted(self.equipes, key=lambda equipe: equipe.pontos, reverse=True)
        for i, equipe in enumerate(classificacao):
            print(f"{i+1}. {equipe.nome} - {equipe.pontos} pontos")

    def salvar_classificacao(self, arquivo):
        classificacao = sorted(self.equipes, key=lambda equipe: equipe.pontos, reverse=True)
        with open(arquivo, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Posição', 'Nome', 'Pontos', 'País', 'Rank'])
            for i, equipe in enumerate(classificacao):
                writer.writerow([i+1, equipe.nome, equipe.pontos, equipe.pais, equipe.rank])

# Lendo as equipes do arquivo CSV
def ler_equipes(arquivo):
    equipes = []
    with open(arquivo, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for linha in reader:
            nome, pais, rank = linha
            equipe = Equipe(nome, pais, int(rank))
            equipes.append(equipe)
    return equipes

# Função para obter a opção de mostrar os minutos e os gols
def obter_opcao_mostrar_minutos(equipe_casa, equipe_visitante):
    while True:
        opcao = input(f"Deseja simular o jogo {equipe_casa.nome} vs {equipe_visitante.nome}? (s/n): ")
        if opcao.lower() in ['s', 'n']:
            return opcao.lower() == 's'
        print("Opção inválida. Por favor, digite 's' para sim ou 'n' para não.")

# Criando o campeonato
equipes = ler_equipes('champions.csv')
campeonato = Campeonato(equipes)

# Simulando as rodadas
for rodada in range(6):
    print(f"Rodada {rodada + 1}:")
    campeonato.jogar_rodada()

# Exibindo a classificação final
print("\nClassificação final:")
campeonato.exibir_classificacao()

# Salvando a classificação no arquivo CSV
campeonato.salvar_classificacao('classificacao.csv')




