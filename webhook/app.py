import os
import hmac
import hashlib
import subprocess

from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Verify the webhook signature
    secret = os.environ.get('WEBHOOK_SECRET').encode('utf-8')
    signature = request.headers.get('X-Hub-Signature')
    if not verify_signature(secret, request.data, signature):
        abort(403)

    # Fetch Gists and repos and rebuild the Jekyll site
    subprocess.call(['./fetch-github-posts.sh'])
    subprocess.call(['docker-compose', 'up', '--build', '-d'])

    return 'OK'

def verify_signature(secret, payload, signature):
    digest = hmac.new(secret, payload, hashlib.sha1).hexdigest()
    expected_signature = 'sha1=' + digest
    return hmac.compare_digest(expected_signature, signature)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
