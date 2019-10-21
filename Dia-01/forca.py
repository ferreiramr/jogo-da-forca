class Jogo:
    def __init__(self, desenho_da_forca):
        self._palavras = self._obter_palavras()
        self._palavra = Palavra(self._palavras)
        self._chutes = Chutes(self._palavra)
        self._desenho_da_forca = desenho_da_forca
        self._maximo_de_erros = len(self._desenho_da_forca) - 1

    def _obter_palavras(self):
        import json
        with open('dados_do_jogo.json') as dados_json:
            palavras = json.load(dados_json)['palavras']
        return tuple(palavras)

    def desenho_da_forca(self):
        return self._desenho_da_forca[self._chutes._erros]

    def palavra_secreta(self):
        return self._palavra._secreta

    def chutar(self, letra):
        self._chutes.novo(letra)

    def chutes(self):
        return self._chutes._certos + self._chutes._errados

    def enforcou(self):
        return self._chutes._erros >= self._maximo_de_erros

    def infelizmente_saiu_vivo(self):
        return self._palavra.secreta_foi_revelada()


class Palavra:

    def __init__(self, palavras):
        self._revelada = self._escolher_palavra(palavras)
        self._secreta = ['_' for letra in self._revelada]

    def _escolher_palavra(self, palavras):
        from random import choice
        return choice(palavras).upper()

    def revele_os_chutes(self, chutes):
        def revela_ou_oculta(letra):
            return letra if letra in chutes else '_'

        self._secreta = [revela_ou_oculta(letra) for letra in self._revelada]

    def secreta_foi_revelada(self):
        return '_' not in self._secreta


class Chutes:
    def __init__(self, palavra_secreta):
        self._palavra_secreta = palavra_secreta
        self._atual = ''
        self._certos = ''
        self._errados = ''
        self._erros = 0

    def novo(self, letra):
        self._atual = letra.upper()

        if self._eh_certo():
            self._certos += self._atual
            self._palavra_secreta.revele_os_chutes(self._certos)

        if self._eh_errado():
            self._errados += self._atual
            self._erros += 1

    def _eh_certo(self):
        return self._eh_valido() and self._atual in self._palavra_secreta._revelada

    def _eh_errado(self):
        return self._eh_valido() and not self._eh_certo()

    def _eh_valido(self):
        eh_uma_letra = self._atual.isalpha()
        eh_apenas_uma_letra = len(self._atual) == 1
        eh_repetido = self._atual in (self._certos + self._errados)

        if eh_uma_letra and eh_apenas_uma_letra and not eh_repetido:
            return True
        else:
            return False


if __name__ == "__main__":
    with open('desenho_da_forca.txt', 'r') as forca_txt:
        desenho_da_forca = forca_txt.read().split(';')

    jogo = Jogo(desenho_da_forca)

    while not (jogo.infelizmente_saiu_vivo() or jogo.enforcou()):
        print(jogo.desenho_da_forca())
        print(jogo.palavra_secreta())
        print('\nChutes dados:', jogo.chutes())
        jogo.chutar(input('\nQual é seu chute? Mas cuidado, ele pode ser o ultimo!: '))

    mensagem_de_morte = jogo.desenho_da_forca()

    with open('mensagem_de_nao_morte.txt') as mensagem_txt:
        mensagem_de_nao_morte = mensagem_txt.read()

    if jogo.enforcou():
        print(mensagem_de_morte)

    if jogo.infelizmente_saiu_vivo():
        print(mensagem_de_nao_morte)
