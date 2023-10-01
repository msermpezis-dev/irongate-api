from flask import Flask, jsonify, request
from encryption.keys import Keys
from encryption.encryptor import Encryptor
from encryption.decryptor import Decryptor
from encryption.generator import Generator
from database.db import Database
from email_plus.email import Email

# h@h.he, h@h.he, diesel frost future face dad goddess flee today tail version bullet miracle


app = Flask(__name__)


# 200: success, 301: missing parameter,
# -1: Wrong Combination of E-mail/Password
# -2: Email doesn't exist

@app.route('/')
def index():
    return "Hello from Flask"


def PWCheck(user_id, pw):
    db = Database()
    values = db.get_decryption_values_pwcheck(user_id)
    k = Keys()
    gen = Generator()
    dec = Decryptor()
    salt = gen.stringToBinary(values[0])
    iv = gen.stringToBinary(values[1])
    cipher = k.getCipher(pw, salt, iv)
    cvalue = gen.stringToBinary(values[2])
    decr_cvalue = dec.decrypt(cvalue, cipher)
    if decr_cvalue == b"{xpz_^2LJ6[W8m]_":
        return True
    else:
        return False


def MPCheck(user_id, mp):
    gen = Generator()
    # user_id, salt, iv, cvalue, emk, mcvalue
    values = Database().get_decryption_values_mpcheck(user_id)
    salt = gen.stringToBinary(values[0])
    iv = gen.stringToBinary(values[1])
    mcvalue = gen.stringToBinary(values[2])
    k = Keys()
    dec = Decryptor()
    cipher = k.getCipher(mp, salt, iv)
    decr_mp_value = dec.decrypt(mcvalue, cipher)
    if decr_mp_value == b"f.d4T*4cF-)2dFg/":
        return True
    else:
        return False


def RegMCValue(mnemonic):
    gen = Generator()
    k = Keys()
    enc = Encryptor()
    salt = gen.getNewSalt()
    iv = gen.getNewIv()
    masterkey = k.getMasterKey(mnemonic, salt)
    mastercipher = k.getMasterCipher(masterkey, iv)
    mcvalue = enc.get_mpcheckvalue(mastercipher)
    mcvalue = gen.binaryToString(mcvalue)
    salt = gen.binaryToString(salt)
    iv = gen.binaryToString(iv)
    return {'mcvalue': mcvalue, 'salt': salt, 'iv': iv}


def MPRegisterCheck(salt, iv, mcvalue, mp):
    k = Keys()
    dec = Decryptor()
    cipher = k.getCipher(mp, salt, iv)
    decr_mp_value = dec.decrypt(mcvalue, cipher)
    if decr_mp_value == b"f.d4T*4cF-)2dFg/":
        return True
    else:
        return False


@app.route('/check', methods=['POST'])
def Check():
    db = Database()
    postedData = request.get_json()
    return dict(exists=db.check_if_email_exists(postedData['email']))


@app.route('/login', methods=['POST'])
def Login():
    # Get posted data
    postedData = request.get_json()
    # Verify valildity of posted data
    if "email" not in postedData or "password" not in postedData or len(postedData) != 2:
        return {'Status Code': -1}
    elif isinstance(postedData['email'], str) and isinstance(postedData['password'], str):
        db = Database()
        email = postedData["email"]
        if db.check_if_email_exists(email):
            pw = postedData["password"]
            user_id = db.get_user_id(email)
            if PWCheck(user_id, pw):
                values = db.get_decryption_values(user_id)
                retMap = {
                    'user_id': values[0],
                    'salt_string': values[1],
                    'iv_string': values[2],
                    'enc_masterkey_string': values[4],
                    'Status Code': 200
                }
                return retMap
            else:
                return {'Status Code': -1}
        else:
            return {'Status Code': -2}
    else:
        return {'Status Code': -3}


@app.route('/register', methods=['POST'])
def Register():
    # Get posted data
    postedData = request.get_json()
    if "email" not in postedData or "salt" not in postedData or "iv" not in postedData or \
            "mcvalue" not in postedData or "mp" not in postedData or "password" not in postedData \
            or len(postedData) != 6:
        return {'Status Code': -1}
    elif isinstance(postedData['email'], str) and isinstance(postedData['salt'], str) and \
            isinstance(postedData['iv'], str) and isinstance(postedData['mcvalue'], str) and \
            isinstance(postedData['mp'], str) and isinstance(postedData['password'], str) and \
            not Database().check_if_email_exists(postedData['email']):
        gen = Generator()
        salt = gen.stringToBinary(postedData["salt"])
        iv = gen.stringToBinary(postedData["iv"])
        mcvalue = gen.stringToBinary(postedData["mcvalue"])
        mp = postedData["mp"]
        if MPRegisterCheck(salt, iv, mcvalue, mp):
            gen = Generator()
            k = Keys()
            masterkey = k.getMasterKey(mp, salt)
            ready_masterkey = gen.binaryToString(masterkey)
            # b'/xca/xas/xax' > b'readable_letters' > "readable_letters"
            mastercipher = k.getCipher(postedData["password"], salt, iv)
            # ready_masterkey = base64.urlsafe_b64decode(mastercipher) reverse
            enc = Encryptor()
            cvalue = gen.binaryToString(enc.get_checkvalue(mastercipher))
            emk = gen.binaryToString(enc.encrypt_mk(ready_masterkey, mastercipher))

            Database().data_entry_userdata(postedData["email"], postedData["salt"], postedData["iv"],
                                           postedData["mcvalue"], cvalue, emk)
            return {'Status Code': 200}
        else:
            return {'Status Code': -1}
    else:
        return {'Status Code': -1}


@app.route('/entities', methods=['POST'])
def Entities():
    # Get posted data
    postedData = request.get_json()
    if "user_id" not in postedData or "pw" not in postedData or len(postedData) != 2:
        return {'Status Code': -1}
    elif isinstance(postedData['user_id'], int) and isinstance(postedData['pw'], str):
        user_id = postedData['user_id']
        if PWCheck(user_id, postedData['pw']):
            entities = Database().check_if_entities_exist(user_id)
            retMap = []
            if entities:
                for i in range(len(entities)):
                    ent = {'id': entities[i][0], 'en': entities[i][1], 'eun': entities[i][2],
                           'epw': entities[i][3], 'enotes': entities[i][4]}
                    retMap.append(ent)
                return jsonify(retMap)
            else:
                return jsonify(retMap)
        else:
            return {'Status Code': -1}
    else:
        return {'Status Code': -1}


@app.route('/addentity', methods=['POST'])
def AddEntity():
    # Get posted data
    postedData = request.get_json()
    if "name" not in postedData or "username" not in postedData or "password" not in postedData \
            or "notes" not in postedData or "user_id" not in postedData or "pw" not in postedData \
            or len(postedData) != 6:
        return {}
    elif isinstance(postedData['name'], str) and isinstance(postedData['username'], str) and \
            isinstance(postedData['password'], str) and isinstance(postedData['notes'], str) and \
            isinstance(postedData['user_id'], int) and isinstance(postedData['pw'], str):
        name = postedData['name']
        username = postedData['username']
        password = postedData['password']
        notes = postedData['notes']
        user_id = postedData['user_id']
        pw = postedData['pw']
        if PWCheck(user_id, pw) and 0 < len(name) < 51 and 0 < len(username) < 33 and 0 < len(password) < 33:
            db = Database()
            # user_id, salt, iv, cvalue, emk
            values = db.get_decryption_values(user_id)
            k = Keys()
            gen = Generator()
            enc = Encryptor()
            salt = gen.stringToBinary(values[1])
            iv = gen.stringToBinary(values[2])
            cipher = k.getCipher(pw, salt, iv)
            enc_masterkey = gen.stringToBinary(values[4])
            masterkey = Decryptor().decrypt_mk(enc_masterkey, cipher)
            readymasterkey = gen.stringToBinary(masterkey[:44])
            mastercipher = k.getMasterCipher(readymasterkey, iv)
            eun = gen.binaryToString(enc.encrypt(username, mastercipher))
            epw = gen.binaryToString(enc.encrypt(password, mastercipher))
            db.data_entry_entity(user_id, name, eun, epw, notes)
            return {'Status Code': 200}
        else:
            return {'Status Code': -1}
    else:
        return {'Status Code': -1}


@app.route('/remove', methods=['POST'])
def Remove():
    # Get posted data
    postedData = request.get_json()
    if "user_id" not in postedData or "pw" not in postedData or "e_id" not in postedData \
            or len(postedData) != 3:
        return {}
    elif isinstance(postedData['user_id'], int) and isinstance(postedData['pw'], str) and \
            isinstance(postedData['e_id'], list):
        ids_are_ints = False
        for id in postedData['e_id']:
            if isinstance(id, int):
                ids_are_ints = True
            else:
                ids_are_ints = False
                break
        if ids_are_ints:
            user_id = postedData['user_id']
            pw = postedData['pw']
            if PWCheck(user_id, pw):
                entities_ids = Database().get_entities_ids(user_id)
                n_entities_ids = []
                for i in range(len(entities_ids)):
                    n_entities_ids.append(entities_ids[i][0])
                del entities_ids
                for i in postedData['e_id']:
                    if i in n_entities_ids:
                        Database().remove_entity(i)
                return {'Status Code': 200}
            else:
                return {'Status Code': -1}
        else:
            return {'Status Code': -1}
    else:
        return {'Status Code': -1}


@app.route('/unlock', methods=['POST'])
def UnlockChangePW():
    # Get posted data
    postedData = request.get_json()
    if "email" not in postedData or "mp" not in postedData or len(postedData) != 2:
        return {'success': False}
    elif isinstance(postedData['email'], str) and isinstance(postedData['mp'], str) \
            and Database().check_if_email_exists(postedData["email"]):
        user_id = Database().get_user_id(postedData["email"])
        if MPCheck(user_id, postedData["mp"]):
            return {'success': True}
        else:
            return {'success': False}
    else:
        return {'success': False}


@app.route('/changepw', methods=['POST'])
def ChangePW():
    # Get posted data
    postedData = request.get_json()
    if "email" not in postedData or "pw" not in postedData or "mp" not in postedData or len(postedData) != 3:
        return {'success': False}
    elif isinstance(postedData['email'], str) and isinstance(postedData['pw'], str) and \
            isinstance(postedData['mp'], str) and Database().check_if_email_exists(postedData['email']):
        user_id = Database().get_user_id(postedData["email"])
        if MPCheck(user_id, postedData["mp"]):
            db = Database()
            gen = Generator()
            k = Keys()
            enc = Encryptor()

            values = db.get_decryption_values_only(user_id)
            salt = gen.stringToBinary(values[0])
            iv = gen.stringToBinary(values[1])

            masterkey = k.getMasterKey(postedData["mp"], salt)
            ready_masterkey = gen.binaryToString(masterkey)
            # b'/xca/xas/xax' > b'readable_letters' > "readable_letters"
            cipher = k.getCipher(postedData['pw'], salt, iv)
            # ready_masterkey = base64.urlsafe_b64decode(mastercipher) reverse

            emk = gen.binaryToString(enc.encrypt_mk(ready_masterkey, cipher))
            cvalue = gen.binaryToString(enc.get_checkvalue(cipher))
            db.change_pw(user_id, cvalue, emk)
            return {'success': True}
        else:
            return {'success': False}
    else:
        return {'success': False}


@app.route('/checkmail', methods=['POST'])
def CheckMail():
    # Get posted data
    postedData = request.get_json()
    if "email" not in postedData or len(postedData) != 1:
        return {'Status Code': -1}
    elif isinstance(postedData['email'], str) and Email().check_email(postedData["email"]):
        email = postedData["email"]
        return {'isEmail': Database().check_if_email_exists(email)}
    else:
        return {'Status Code': -1}


@app.route('/sendmail', methods=['POST'])
def SendEmail():
    postedData = request.get_json()
    if "email" not in postedData or len(postedData) != 1:
        return {'Status Code': -1}
    elif isinstance(postedData['email'], str) and Email().check_email(postedData["email"]):
        mnenomic = Generator().getNewMnemonic()
        Email().send_email(postedData['email'], mnenomic)
        return RegMCValue(mnenomic)
    else:
        return {'Status Code': -1}


if __name__ == "__main__":
    context = ('keys/cert.pem', 'keys/key.pem')
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=context)
