from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from forca import Jogo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donaMorte'
bootstrap = Bootstrap(app)


with open('desenho_da_forca.txt', 'r') as forca_txt:
    desenho_da_forca = forca_txt.read().split(';')


jogo = Jogo(desenho_da_forca)


@app.route('/', methods=['GET', 'POST'])
def jogogando():

    class FormularioDeChute(FlaskForm):
        chute = StringField(
            'Qual é seu chute? Mas cuidado, ele pode ser o ultimo!', render_kw={"size": "1"})
        chutar = SubmitField('Chutar')

    formulario_de_chute = FormularioDeChute()

    if formulario_de_chute.validate_on_submit():
        jogo.chutar(formulario_de_chute.chute.data)
        formulario_de_chute.chute.data = ''

    if jogo.infelizmente_saiu_vivo():
        return redirect(url_for('nao_morreu'))
    elif jogo.enforcou():
        return redirect(url_for('morreu'))
    else:
        return render_template('jogo.html', forca=jogo.desenho_da_forca(), palavra_secreta=jogo.palavra_secreta(),
                                chutes=jogo.chutes(), formulario_de_chute=formulario_de_chute)


@app.route('/infelizmente-voce-nao-morreu')
def nao_morreu():
    with open('mensagem_de_nao_morte.txt') as mensagem_txt:
        mensagem_de_nao_morte = mensagem_txt.read()

    return render_template('nao-morreu.html', mensagem_de_nao_morte=mensagem_de_nao_morte)

@app.route('/fico-feliz-que-esteja-morto')
def morreu():
    return render_template('morreu.html', forca=jogo.desenho_da_forca())

if __name__ == "__main__":
    app.run(debug=True)