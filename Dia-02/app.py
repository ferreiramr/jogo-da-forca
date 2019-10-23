from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from forca import Jogo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donaMorte'
bootstrap = Bootstrap(app)


with open('desenho_da_forca.txt', 'r', encoding='utf-8) as forca_txt:
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


if __name__ == "__main__":
    app.run(debug=True)
