class Jogo:
    def __init__(self, desenhos_da_forca):
        self._palavra_secreta = PalavraSecretra()
        self._chute = Chute(self._palavra_secreta)
        self._DESENHO_DA_FORCA = desenhos_da_forca
        self._maximo_de_erros = len(self._DESENHO_DA_FORCA) - 1

    def nova_palavra(self):
        self._palavra_secreta = PalavraSecretra()
        self._chute = Chute(self._palavra_secreta)

    def palavra_secreta(self):
        return self._palavra_secreta._oculta

    def infelizmente_saiu_vivo(self):
        return self._palavra_secreta.foi_revelada()

    def enforcou(self):
        return self._chute._erros >= self._maximo_de_erros

    def chutar(self, chute):
        self._chute.novo_chute(chute)

    def chutes(self):
        return self._chute._certos + self._chute._errados

    def desenhar_forca(self):
        return self._DESENHO_DA_FORCA[self._chute._erros]

    def adicionar_palavra(self, nova_palavra):
        self._palavra_secreta.salvar_nova(nova_palavra)




class PalavraSecretra():


    def obter_palavras(self):
        import shelve
        dados_do_jogo = shelve.open('dados_do_jogo.db')

        try:
            palavras = dados_do_jogo['palavras']
            dados_do_jogo.close()
        except:
            palavras = ['mortes']

        return palavras

    def salvar_nova(self, nova_palavra):
        import shelve
        dados_do_jogo = shelve.open('dados_do_jogo.db')
        palavras = dados_do_jogo['palavras']

        if len(nova_palavra) >= 5 and len(nova_palavra) <= 10 and nova_palavra not in palavras:
            palavras.append(nova_palavra)
            dados_do_jogo.close()

    def __init__(self):
        palavras = self.obter_palavras()
        from random import choice
        self._revelada = choice(palavras).lower()
        self._oculta = ['_' for letra in self._revelada]

    def foi_revelada(self):
        return '_' not in self._oculta

    def revela_chutes(self, chutes):
        def revela_ou_oculta(letra):
            return letra if letra in chutes else '_'
        self._oculta = [revela_ou_oculta(letra) for letra in self._revelada]


class Chute():

    def __init__(self, palalavra_secreta):
        self._atual = ''
        self._palalavra_secreta = palalavra_secreta
        self._certos = ''
        self._errados = ''
        self._erros = 0

    def novo_chute(self, chute):
        self._atual = chute
        if self.valido():
            if self.certo():
                self._certos += chute
                self._palalavra_secreta.revela_chutes(self._certos)
            else:
                self._errados += chute
                self._erros += 1

    def certo(self):
        return self._atual in self._palalavra_secreta._revelada

    def valido(self):
        return self._atual.isalpha() and len(self._atual) == 1 and not self.repetido()

    def repetido(self):
        return self._atual in self._certos + self._errados


if __name__ == "__main__":

    DESENHOS_DA_FORCA = open('desenho_da_forca.txt', 'r', encoding='utf-8')
    MENSAGEM_DE_NAO_MORTE = open(
        'mensagem_de_nao_morte.txt', 'r', encoding='utf-8')

    desenhos_da_forca = DESENHOS_DA_FORCA.read().split('#')
    mensagem_de_nao_morte = MENSAGEM_DE_NAO_MORTE.read()

    DESENHOS_DA_FORCA.close()
    MENSAGEM_DE_NAO_MORTE.close()


    jogo = Jogo(desenhos_da_forca)
    print(jogo.desenhar_forca())

    while not (jogo.infelizmente_saiu_vivo() or jogo.enforcou()):
        print(jogo.palavra_secreta())
        print('Chutes dados: ', jogo.chutes())
        jogo.chutar(input())
        print(jogo.desenhar_forca())

    if jogo.infelizmente_saiu_vivo():
        print(mensagem_de_nao_morte)

        while True:
            nova_palavra = input('Ajude Dona Morte, adicione mais uma palavra: ')
            jogo.adicionar_palavra(nova_palavra)
            break
