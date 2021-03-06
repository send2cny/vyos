from flask import Flask, jsonify, abort, make_response, request, session
from flask.ext.httpauth import HTTPBasicAuth
import vymgmt
import subprocess

app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
	"henry": "password",
	"nothenry": "password"
}

vyos = vymgmt.Router('192.168.1.1', 'vyos', password='password', port=22)

@auth.get_password
def get_password(username):
	if username in users:
		return users.get(username)
	return None

@app.route('/readethdesc', methods=['POST'])
@auth.login_required
def readethdesc():
	if not request.json or not 'ethname' in request.json:
		abort(400)
        query = "show interface ethernet " + request.json['ethname'] + " description"
        vyos.login()
	vyos.configure()
	out = vyos.run_conf_mode_command(query)
	vyos.exit()
	vyos.logout()
	outstr = str(out)
	namelen = len(request.json['ethname'])
	checkstart = 48 + namelen
	checkend = 59 + namelen
	checkdesc = outstr[checkstart:checkend]
	outstart = 60 + namelen
	if checkdesc == "description":
		desc = outstr[outstart:-34]
		return jsonify({'description': desc})
	else:
		abort(404)

@app.route('/ethdesc', methods=['POST'])
@auth.login_required
def createethdesc():
	if not request.json or not 'ethname' in request.json or not 'ethdesc' in request.json:
		abort(400)
        query = "interface ethernet " + request.json['ethname'] + " description '" + request.json['ethdesc'] + "'"
	checkquery = "show interface ethernet " + request.json['ethname'] + " description"
	vyos.login()
	vyos.configure()
	out = vyos.run_conf_mode_command(checkquery)
	vyos.exit()
	vyos.logout()
	outstr = str(out)
	namelen = len(request.json['ethname'])
	checkstart = 48 + namelen
	checkend = 59 + namelen
	checkdesc = outstr[checkstart:checkend]
	if checkdesc == "description":
		return jsonify({'error': 'description already exist' })
	elif checkdesc == "onfiguratio":
	        vyos.login()
		vyos.configure()
		vyos.set(query)
		vyos.commit()
		vyos.save()
		vyos.exit()
		vyos.logout()
		return jsonify({'success': 'description have been created'})
	else:
		abort(404)

@app.route('/ethdesc', methods=['DELETE'])
@auth.login_required
def deleteethdesc():
	if not request.json or not 'ethname' in request.json:
		abort(400)
        query = "interface ethernet " + request.json['ethname'] + " description"
	checkquery = "show interface ethernet " + request.json['ethname'] + " description"
	vyos.login()
	vyos.configure()
	out = vyos.run_conf_mode_command(checkquery)
	vyos.exit()
	vyos.logout()
	outstr = str(out)
	namelen = len(request.json['ethname'])
	checkstart = 48 + namelen
	checkend = 59 + namelen
	checkdesc = outstr[checkstart:checkend]
	if checkdesc == "description":
	        vyos.login()
		vyos.configure()
		vyos.delete(query)
		vyos.commit()
		vyos.save()
		vyos.exit()
		vyos.logout()
		return jsonify({'success': 'description have been deleted'})	
	elif checkdesc == "onfiguratio":
		return jsonify({'error': 'description does not exist' })
	else:
		abort(404)

@app.route('/ethdesc', methods=['PUT'])
@auth.login_required
def updateethdesc():
	if not request.json or not 'ethname' in request.json or not 'ethdesc' in request.json:
		abort(400)
        delquery = "interface ethernet " + request.json['ethname'] + " description"
	upquery = "interface ethernet " + request.json['ethname'] + " description '" + request.json['ethdesc'] + "'"
	checkquery = "show interface ethernet " + request.json['ethname'] + " description"
	vyos.login()
	vyos.configure()
	out = vyos.run_conf_mode_command(checkquery)
	vyos.exit()
	vyos.logout()
	outstr = str(out)
	namelen = len(request.json['ethname'])
	checkstart = 48 + namelen
	checkend = 59 + namelen
	checkdesc = outstr[checkstart:checkend]
	if checkdesc == "description":
	        vyos.login()
		vyos.configure()
		vyos.delete(delquery)
		vyos.set(upquery)
		vyos.commit()
		vyos.save()
		vyos.exit()
		vyos.logout()
		return jsonify({'success': 'description have been updated'})	
	elif checkdesc == "onfiguratio":
		return jsonify({'error': 'description does not exist' })
	else:
		abort(404)

@app.route('/readruledefault', methods=['POST'])
@auth.login_required
def readruledefault():
	if not request.json or not 'firename' in request.json:
		abort(400)
        query = "show firewall name " + request.json['firename'] + " default-action"
        vyos.login()
	vyos.configure()
	out = vyos.run_conf_mode_command(query)
	vyos.exit()
	vyos.logout()
	outstr = str(out)
	namelen = len(request.json['firename'])
	checkstart = 46 + namelen
	checkend = 60 + namelen
	check = outstr[checkstart:checkend]
	outstart = 61 + namelen
	if check == "default-action":
		default = outstr[outstart:-34]
		return jsonify({'default-action': default})
	else:
		abort(404)

@app.route('/ruledefault', methods=['POST'])
@auth.login_required
def createruledefault():
	if not request.json or not 'firename' in request.json or not 'fireact' in request.json:
		abort(400)
	if request.json['fireact'] == "drop" or request.json['fireact'] == "reject" or request.json['fireact'] == "accept":
	        query = "firewall name " + request.json['firename'] + " default-action " + request.json['fireact']
		checkquery = "show firewall name " + request.json['firename'] + " default-action"
		vyos.login()
		vyos.configure()
		out = vyos.run_conf_mode_command(checkquery)
		vyos.exit()
		vyos.logout()
		outstr = str(out)
		namelen = len(request.json['firename'])
		checkstart = 46 + namelen
		checkend = 60 + namelen
		check = outstr[checkstart:checkend]
		if check == "default-action":
			return jsonify({'error': 'firewall default-action already exist'})
		elif check == "onfiguration u":
		        vyos.login()
			vyos.configure()
			vyos.set(query)
			vyos.commit()
			vyos.save()
			vyos.exit()
			vyos.logout()
			return jsonify({'success': 'firewall default-action have been created'})
		else:
			abort(400)
	else:
		abort(400)

@app.route('/ruledefault', methods=['DELETE'])
@auth.login_required
def deleteruledefault():
	if not request.json or not 'firename' in request.json:
		abort(400)
	query = "firewall name " + request.json['firename'] + " default-action"
	checkquery = "show firewall name " + request.json['firename'] + " default-action"
	vyos.login()
	vyos.configure()
	out = vyos.run_conf_mode_command(checkquery)
	vyos.exit()
	vyos.logout()
	outstr = str(out)
	namelen = len(request.json['firename'])
	checkstart = 46 + namelen
	checkend = 60 + namelen
	check = outstr[checkstart:checkend]
	if check == "default-action":
		vyos.login()
		vyos.configure()
		vyos.delete(query)
		vyos.commit()
		vyos.save()
		vyos.exit()
		vyos.logout()
		return jsonify({'success': 'firewall default-action have been deleted'})
	elif check == "onfiguration u":
		return jsonify({'error': 'firewall default-action does not exist'})
	else:
		abort(400)

@app.route('/ruledefault', methods=['PUT'])
@auth.login_required
def updateruledefault():
	if not request.json or not 'firename' in request.json or not 'fireact' in request.json:
		abort(400)
	if request.json['fireact'] == "drop" or request.json['fireact'] == "reject" or request.json['fireact'] == "accept":
	        query = "firewall name " + request.json['firename'] + " default-action " + request.json['fireact']
		checkquery = "show firewall name " + request.json['firename'] + " default-action"
		deletequery = "firewall name " + request.json['firename'] + " default-action"
		vyos.login()
		vyos.configure()
		out = vyos.run_conf_mode_command(checkquery)
		vyos.exit()
		vyos.logout()
		outstr = str(out)
		namelen = len(request.json['firename'])
		checkstart = 46 + namelen
		checkend = 60 + namelen
		check = outstr[checkstart:checkend]
		if check == "default-action":
			vyos.login()
			vyos.configure()
			vyos.delete(deletequery)
			vyos.set(query)
			vyos.commit()
			vyos.save()
			vyos.exit()
			vyos.logout()
			return jsonify({'success': 'firewall default-action have been updated'})
		elif check == "onfiguration u":
		        return jsonify({'error': 'firewall default-action does not exist'})
		else:
			abort(400)
	else:
		abort(400)
@app.route('/readethfire', methods=['POST'])
@auth.login_required
def readethfire():
	if not request.json or not 'ethname' in request.json or not 'conntype' in request.json:
		abort(400)
	if request.json['conntype'] == "in" or request.json['conntype'] == "out" or request.json['conntype'] == "local":
	        query = "show interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype']
        	vyos.login()
		vyos.configure()
		out = vyos.run_conf_mode_command(query)
		vyos.exit()
		vyos.logout()
		outstr = str(out)
		namelen = len(request.json['ethname'])
		connlen = len(request.json['conntype'])
		checkstart = 46 + namelen + connlen
		checkend = 50 + namelen + connlen
		checkname = outstr[checkstart:checkend]
		outstart = 51 + namelen + connlen
		if checkname == "name":
			outname = outstr[outstart:-34]
			return jsonify({'rule-sets name': outname})
		else:
			abort(400)
	else:
		abort(400)

@app.route('/ethfire', methods=['POST'])
@auth.login_required
def createethfire():
	if not request.json or not 'ethname' in request.json or not 'conntype' in request.json or not 'firename' in request.json:
		abort(400)
	if request.json['conntype'] == "in" or request.json['conntype'] == "out" or request.json['conntype'] == "local":
	        query = "interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype'] + " name " + request.json['firename']
		firequery = "show firewall name " + request.json['firename'] + " default-action"
		checkquery = "show interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype']
		vyos.login()
		vyos.configure()
		out = vyos.run_conf_mode_command(firequery)
		vyos.exit()
		vyos.logout()
		outstr = str(out)
		namelen = len(request.json['firename'])
		checkstart = 46 + namelen
		checkend = 60 + namelen
		check = outstr[checkstart:checkend]
		if check == "default-action":
			vyos.login()
			vyos.configure()
			out = vyos.run_conf_mode_command(checkquery)
			vyos.exit()
			vyos.logout()
			outstr = str(out)
			namelen = len(request.json['ethname'])
			connlen = len(request.json['conntype'])
			checkstart = 46 + namelen + connlen
			checkend = 50 + namelen + connlen
			checkname = outstr[checkstart:checkend]
			outstart = 51 + namelen + connlen
			if checkname == "name":
				return jsonify({'error': 'firewall rule-sets already exist on this interface'})
			elif checkname == "onfi":
		        	vyos.login()
				vyos.configure()
				vyos.set(query)
				vyos.commit()
				vyos.save()
				vyos.exit()
				vyos.logout()
				return jsonify({'success': 'firewall rule-sets has been successfully created'})
			else:
				abort(400)
		elif check == "onfiguration u":
			return jsonify({'error': 'firewall default-action does not exist'})
		else:
			abort(400)
	else:
		abort(400)

@app.route('/ethfire', methods=['DELETE'])
@auth.login_required
def deleteethfire():
	if not request.json or not 'ethname' in request.json or not 'conntype' in request.json:
		abort(400)
	if request.json['conntype'] == "in" or request.json['conntype'] == "out" or request.json['conntype'] == "local":
	        query = "interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype']
		checkquery = "show interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype']
		vyos.login()
		vyos.configure()
		out = vyos.run_conf_mode_command(checkquery)
		vyos.exit()
		vyos.logout()
		outstr = str(out)
		namelen = len(request.json['ethname'])
		connlen = len(request.json['conntype'])
		checkstart = 46 + namelen + connlen
		checkend = 50 + namelen + connlen
		checkname = outstr[checkstart:checkend]
		outstart = 51 + namelen + connlen
		if checkname == "name":
	        	vyos.login()
			vyos.configure()
			vyos.delete(query)
			vyos.commit()
			vyos.save()
			vyos.exit()
			vyos.logout()
			return jsonify({'success': 'firewall rule-sets has been successfully deleted'})
		elif checkname == "onfi":
			return jsonify({'error': 'firewall rule-sets does not exist on this interface'})
		else:
			abort(400)
	else:
		abort(400)

@app.route('/ethfire', methods=['PUT'])
@auth.login_required
def updateethfire():
	if not request.json or not 'ethname' in request.json or not 'conntype' in request.json or not 'firename' in request.json:
		abort(400)
	if request.json['conntype'] == "in" or request.json['conntype'] == "out" or request.json['conntype'] == "local":
	        query = "interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype'] + " name " + request.json['firename']
		deletequery = "interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype']
		firequery = "show firewall name " + request.json['firename'] + " default-action"
		checkquery = "show interface ethernet " + request.json['ethname'] + " firewall " + request.json['conntype']
		vyos.login()
		vyos.configure()
		out = vyos.run_conf_mode_command(firequery)
		vyos.exit()
		vyos.logout()
		outstr = str(out)
		namelen = len(request.json['firename'])
		checkstart = 46 + namelen
		checkend = 60 + namelen
		check = outstr[checkstart:checkend]
		if check == "default-action":
			vyos.login()
			vyos.configure()
			out = vyos.run_conf_mode_command(checkquery)
			vyos.exit()
			vyos.logout()
			outstr = str(out)
			namelen = len(request.json['ethname'])
			connlen = len(request.json['conntype'])
			checkstart = 46 + namelen + connlen
			checkend = 50 + namelen + connlen
			checkname = outstr[checkstart:checkend]
			outstart = 51 + namelen + connlen
			if checkname == "name":
		        	vyos.login()
				vyos.configure()
				vyos.delete(deletequery)
				vyos.set(query)
				vyos.commit()
				vyos.save()
				vyos.exit()
				vyos.logout()
				return jsonify({'success': 'firewall rule-sets has been successfully updated'})
			elif checkname == "onfi":
				return jsonify({'error': 'firewall rule-sets does not exist on this interface'})
			else:
				abort(400)
		elif check == "onfiguration u":
			return jsonify({'error': 'firewall default-action does not exist'})
		else:
			abort(400)
	else:
		abort(400)
		
@auth.error_handler
def auth_error():
	return make_response(jsonify({'error': '401 Unauthorised Access'}), 401)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': '400 Bad Request'}), 400)
       		
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': '404 Not Found'}), 404)

@app.errorhandler(500)
def internal_error(error):
	return make_response(jsonify({'error': '500 Internal Server Error'}), 500)


if __name__ == '__main__':
	app.run(debug=True)
