from flask import Flask, render_template, url_for, redirect

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from forca import Jogo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donaMorte'
bootstrap = Bootstrap(app)


class FormularioDeChute(FlaskForm):
    chute = StringField('Qual é seu chute? Mas cuidado, ele pode ser o ultimo!', render_kw={"size": "1"},  validators=[
                        DataRequired(), Length(max=1, message='Chute apenas uma letra por vez'), ])
    chutar = SubmitField('Chutar')

# CRIAR A LISTA DE HTMLs DA FORCA

DESENHOS_DA_FORCA = open('desenho_da_forca.txt', 'r', encoding='utf-8')
MENSAGEM_DE_NAO_MORTE = open(
    'mensagem_de_nao_morte.txt', 'r', encoding='utf-8')

desenhos_da_forca = DESENHOS_DA_FORCA.read().split(';')
mensagem_de_nao_morte = MENSAGEM_DE_NAO_MORTE.read()

DESENHOS_DA_FORCA.close()
MENSAGEM_DE_NAO_MORTE.close()

jogo = Jogo(desenhos_da_forca)


@app.route('/', methods=['GET', 'POST'])
def index():

    formulario_de_chute = FormularioDeChute()

    if formulario_de_chute.validate_on_submit():
        jogo.chutar(formulario_de_chute.chute.data)
        formulario_de_chute.chute.data = ''

    if jogo.infelizmente_saiu_vivo():
        return redirect(url_for('nao_morreu'))
    elif jogo.enforcou():
        return redirect(url_for('morreu'))
    else:
        return render_template('index.html', forca=jogo.desenhar_forca(), palavra_secreta=jogo.palavra_secreta(), chutes=jogo.chutes(), formulario_de_chute=formulario_de_chute)


@app.route('/novo-jogo', methods=['GET', 'POST'])
def novo_jogo():
    jogo.nova_palavra()
    return redirect(url_for('index'))


@app.route('/infelizmente-voce-nao-morreu', methods=['GET', 'POST'])
def nao_morreu():
    return render_template('nao-morreu.html')


@app.route('/moreu')
def morreu():
    if jogo.enforcou():
        return render_template('morreu.html', forca=jogo.desenhar_forca())
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
