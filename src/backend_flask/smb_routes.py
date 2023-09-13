from app import app
from flask import request

import logging
from smbclient import register_session, listdir, scandir, delete_session, reset_connection_cache

#https://gist.github.com/jborean93/a3cb93fa6237012ebf587e1fbe8fc903
#https://github.com/jborean93/smbprotocol/blob/master/examples/low-level/directory-management.py

#reused during calls
smb_hostname = ""

@app.route('/conntest/api/smb')
def get_smb():
    logging.basicConfig(level=logging.INFO)
    #reset_connection_cache()
    global smb_hostname
    smb_hostname = request.args.get("h")
    smb_user = request.args.get("u")
    smb_pwd = request.args.get("p")
    try:
        session = register_session(server=smb_hostname, username=smb_user, password=smb_pwd)
        conn = session.connection
        response = f"connected to {conn.server_name}:{conn.port} with {session.username}:{session.password}"
        status = 1
    except Exception as ex:
        response = str(ex)
        status = 3
    return {"response": response, "status": status}

@app.route('/conntest/api/smb/browse')
def get_smb_browse():
    logging.basicConfig(level=logging.INFO)

    smb_share = request.args.get("share")
    smb_path = request.args.get("path")

    if smb_path == None:
        smb_path = ""

    try:
        fullpath =f"//{smb_hostname}/{smb_share}/{smb_path}"
        entries = listdir(fullpath)
        response = f"connected to share {fullpath} which contains {len(entries)} entries"
        status = 1
        return {"response": response, "status": status, "path": smb_path, "entries": entries}
    except Exception as ex:
        response = str(ex)
        status = 3
    return {"response": response, "status": status}

