from flask import Flask, render_template, request, flash, send_from_directory
from flask_bootstrap import Bootstrap
from forms import ContactForm
from flask_mail import Mail, Message

application = Flask(__name__)

# Initialize Bootstrap instance
bootstrap = Bootstrap(application)

# CSRF Protection Key
application.config['SECRET_KEY'] = 'secret-key'

# Mail Configuration
application.config['MAIL_SERVER']= 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'email'
application.config['MAIL_PASSWORD'] = 'password'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True

# Initialize Flask-Mail instance
mail = Mail(application)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/bio')
def bio():
    return render_template('bio.html')


@application.route('/current_projects')
def current_projects():
    return render_template('current-projects.html')


@application.route('/past_projects')
def past_projects():
    return render_template('past-projects.html')


@application.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender=form.email.data, recipients=['email'])
            msg.body = """
          Name: %s
          Email: %s
          Message: %s
          """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


@application.route('/error')
def error():
    return render_template('error.html')


@application.route('/download_cv')
def download_cv():
    try:
        return send_from_directory('static/cv', 'DanielAldermanCV.pdf')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    application.run()
