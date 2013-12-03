from flask import Flask, request, render_template, flash
# from flask_mail import Mail, Message
from algorithm import generate_pairs
from itertools import groupby
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

def send_third_party_email(email_address, pairs, names):
	string_pairs = ''
	for pair in pairs:
		string_pairs = string_pairs + '%s (%s) is getting a gift for %s (%s)\n' % (names[pair[1]], pair[1], names[pair[0]], pair[0])
	with mail.connect() as conn:
		msg = '''Hi there!
You have been selected as third party in a secret santa in case anyone forgets who has who. Below is a list of the pairs.
%s

Thanks & Merry Christmas!

Father Christmas''' % (string_pairs)
		email = Message('Santa\'s naughty & nice list of children! (Secret Santa Verification)',recipients=[email_address],sender=SENDER_EMAIL,body=msg)
		conn.send(email)

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		third_party = request.form['third_email'] if len(request.form['third_email']) else None
		names = [(key.split('_')[-1],name) for key, name in request.form.items() if key.startswith('name') and len(name)]
		emails = [(key.split('_')[-1],name) for key, name in request.form.items() if key.startswith('email') and len(name)]
		participants = dict(zip(dict(emails).values(),dict(names).values()))
		pairs = [(key.split('_')[-1],name) for key, name in request.form.items() if key.startswith('pair1') or key.startswith('pair2') and len(name)]
		restricted_pairs = [tuple(x[1] for x in v) for k,v in groupby(sorted(pairs), lambda x: x[0])]
		if len(participants) >= 4:
			pairs = calculate_names(participants.keys(), restricted_pairs)
			flash('Pairs generated')
			#send_emails(pairs,participants)
			flash('Emails sent to participants')
			send_third_party_email(third_party, pairs, participants)
		else:
			flash('Error: Not enough participants; please enter 4 or more names')
	return render_template("index.html",min_people=4)

if __name__ == '__main__':
	app.run(debug=True)


