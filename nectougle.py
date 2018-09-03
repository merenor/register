from flask import Flask, request, flash, render_template
from wtforms import Form, StringField, SubmitField, validators


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class SearchForm(Form):
    suche = StringField("Suche: ", validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def show_search():
    form = SearchForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        suche = request.form.get('suche')
        print(suche)

        if form.validate():
            flash('Suche war: ' + suche)
        else:
            flash('Bitte etwas eingeben.')

    return render_template('search.html', form=form)


if __name__ == '__main__':
    app.run()
