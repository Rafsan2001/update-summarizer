import random

from flask import url_for


def password_reset_key_mail_body(id: int, token: str, expire_time: int):
    return f"""<h1>To reset the password please go to the following link.</h1>
<p><a style='text-decoration: none; color: #333; padding: 10px 25px; border: 1px solid #333; cursor: pointer;' href='{ url_for("auth.reset_password", id=id, token=token, _external=True) }' target='_blank'>Visit</a></p>
<p>This link will be expired in {int(expire_time/60)} minutes.</p>
"""

def email_verify_mail_body(id: int, token: str):
    return f"""<h1>To verify your email please go to the following link.</h1>
<p><a style='text-decoration: none; color: #333; padding: 10px 25px; border: 1px solid #333; cursor: pointer;' href='{ url_for("auth.verify_email", id=id, token=token, _external=True) }' target='_blank'>Verify</a></p>
<p>You will not be able to login to your account without verifing your email address.</p>
"""

def generate_token(size: int):
    sample_string = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    result = ''.join((random.choice(sample_string)) for x in range(size)) 
    return result