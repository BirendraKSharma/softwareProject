from flask import Flask, render_template

app = Flask("__name__")

DOC = [{
  'id': 1,
  'name': 'Birendra Sharma',
  'info': 'Heart Surgeon',
  'Email': 'birendrasha444@gmail.com'
}, {
  'id': 2,
  'name': 'Bishal Regmi',
  'info': ' Gynecologists',
  'Email': 'bishalregmi180@gmail.com'
}, {
  'id': 3,
  'name': 'Anuj Thapa',
  'info': 'Ophthalmologists',
  'Email': 'anujth345@gmail.com'
}, {
  'id': 4,
  'name': 'Biswas Kafle',
  'info': 'Otolaryngologists',
  'Email': 'birendrasha444@gmail.com'
}]


@app.route('/')
def hello_world():
  return render_template('home.html', jobs=DOC)


@app.route('/about')
def show_about():
  return render_template('about.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
