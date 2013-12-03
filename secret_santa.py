from flask import Flask, request, render_template, flash
# from flask_mail import Mail, Message
from algorithm import generate_pairs
app = Flask(__name__)
# mail = Mail(app)
app.secret_key = '\x1eAc\xd6x\xce\xab\x99\xfb<\t\x89L\xc2\xb9\x88m\xa8\x0f\xfd\x10\x85\x8b\x13'

SENDER_EMAIL = "info@akmiller.com"

def calculate_names(names, restricted_pairs):
	return generate_pairs(names, restricted_pairs)

def send_emails(pairs,names):
	email_values = {}
	email_values['min_price'] = u"\xa310"
	email_values['max_price'] = u"\xa315"
	with mail.connect() as conn:
		for pair in pairs:
			email_values['giver_name'] = names[pair[1]]
			email_values['recipient_name'] = names[pair[0]]
			email_values['recipient_email'] = pair[0]
			email = '''Hi %(giver_name)s,

Santa here, as I don't have time to visit the older children this year, so it seems you have been entered into a secret santa!

You will be getting a gift in the range of %(min_price)s-%(max_price)s for %(recipient_name)s (%(recipient_email)s)!

Merry Christmas!
Ho Ho Ho!

Father Christmas
	''' % email_values
			msg = Message('Santa needs some help! (Secret Santa)',recipients=[pair[1]],sender=SENDER_EMAIL,body=email)
			conn.send(msg)	


@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		print request.form
		third_party = request.form['third_email'] if len(request.form['third_email']) else None
		names = [(key.split('_')[-1],name) for key, name in request.form.items() if key.startswith('name') and len(name)]
		emails = [(key.split('_')[-1],name) for key, name in request.form.items() if key.startswith('email') and len(name)]
		participants = dict(zip(dict(emails).values(),dict(names).values()))
		pairs = [(key.split('_')[-1],name) for key, name in request.form.items() if key.startswith('pair1') or key.startswith('pair2') and len(name)]
		restricted_pairs = []
		print restricted_pairs
		if len(participants) >= 4:
			pairs = calculate_names(participants.keys(), restricted_pairs)
			flash('Pairs generated')
			#send_emails(pairs,participants)
			flash('Emails sent to participants')
		else:
			flash('Error: Not enough participants; please enter 4 or more names')
	return render_template("index.html",min_people=4)

if __name__ == '__main__':
	app.run(debug=True)

for i in l:
    for k in l:
        w = zip(k,l)
        print w, w[0][0] == w[0][1]
        if w[0][0] == w[0][1]:
            if w[1][0] != w[1][1]:
                q.append(w[1])
                break


