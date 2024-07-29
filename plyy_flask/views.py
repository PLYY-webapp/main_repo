# views.py
from flask import Blueprint, request, session, render_template, redirect, url_for, jsonify
from models import curator_info, curatorlike_status, curator_like, curator_unlike, plyy_like, plyy_unlike, plyylike_status, cu_plyy
from utils import extract_user_uuid

main = Blueprint('main', __name__)
logout = Blueprint('logout', __name__)
mypage = Blueprint('mypage', __name__)
login = Blueprint('login', __name__)
curator = Blueprint('curator', __name__)
api_curator = Blueprint('api_curator', __name__)
like_curator = Blueprint('like_curator', __name__)
unlike_curator = Blueprint('unlike_curator', __name__)
like_plyy = Blueprint('like_plyy', __name__)
unlike_plyy = Blueprint('unlike_plyy', __name__)

@main.route('/main', methods=['GET', 'POST'])
def main_view():
    return render_template('main.html')

@logout.route('/logout', methods=['POST'])
def logout_view():
    session.pop('id', None)
    return redirect(url_for('main.main_view'))

@mypage.route('/mypage')
def mypage_view():
    return render_template('mypage.html')

@login.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        id = request.form['userid']
        pw = request.form['userpw']
        from models import connect_db
        conn, cur = connect_db()
        cur.execute('SELECT u_email, u_pw FROM USER WHERE u_email = ? and u_pw = ?', (id, pw))
        user = cur.fetchone()
        conn.close()
        if user:
            session['id'] = id
            return redirect(url_for('main.main_view'))
        else:
            session['id'] = None
    return render_template('login.html')

@curator.route('/curator/<c_uuid>')
def curator_view(c_uuid):
    return render_template('test6.html')

@api_curator.route('/plyy/api/curator/<c_uuid>', methods=['GET'])
def api_curator_view(c_uuid):
    play_lists = []
    c_info = curator_info(c_uuid)
    c_plyy = cu_plyy(c_uuid)
    c_isliked = None

    for plyy in c_plyy:
        plyy_data = {
            'pid': plyy[0],
            'ptitle': plyy[1],
            'pimg': plyy[2],
            'pgen': plyy[3],
            'pupdate': plyy[4],
            'pcmt': plyy[5],
            'ptag': plyy[8],
            'pliked': None
        }
        play_lists.append(plyy_data)

    pidlist = [play_lists[i]['pid'] for i in range(len(play_lists))]

    if 'id' in session and session['id']:
        u_uuid = extract_user_uuid(session['id'])
        if u_uuid:
            c_isliked = curatorlike_status(c_uuid, u_uuid)
            p_isliked = plyylike_status(pidlist, u_uuid)

            for plyy in play_lists:
                plyy['pliked'] = p_isliked.get(plyy['pid'], False)

    return jsonify({
        'curator': {
            'c_info': {
                'c_id': c_info[0],
                'c_name': c_info[1],
                'c_img': c_info[2],
                'c_intro': c_info[3],
                'c_tags': c_info[4],
                'c_liked': c_isliked
            },
            'plyy': play_lists
        }
    })

@like_curator.route('/plyy/api/like/<u_id>/<c_uuid>', methods=['POST'])
def like_curator_view(u_id, c_uuid):
    u_uuid = extract_user_uuid(u_id)
    success = curator_like(c_uuid, u_uuid)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@unlike_curator.route('/plyy/api/unlike/<u_id>/<c_uuid>', methods=['DELETE'])
def unlike_curator_view(u_id, c_uuid):
    u_uuid = extract_user_uuid(u_id)
    success = curator_unlike(c_uuid, u_uuid)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@like_plyy.route('/plyy/api/plyylike/<u_id>/<plyy_uuid>', methods=['POST'])
def like_plyy_view(u_id, plyy_uuid):
    u_uuid = extract_user_uuid(u_id)
    success = plyy_like(plyy_uuid, u_uuid)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@unlike_plyy.route('/plyy/api/plyyunlike/<u_id>/<plyy_uuid>', methods=['DELETE'])
def unlike_plyy_view(u_id, plyy_uuid):
    u_uuid = extract_user_uuid(u_id)
    success = plyy_unlike(plyy_uuid, u_uuid)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500
