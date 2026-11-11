"""Model scoped opaque credentials without persisting plaintext bearer tokens."""
import json

import hashlib, hmac, secrets
class CredentialVault:
    def __init__(self, key=None):
        self.key = key or secrets.token_bytes(32)
        self.records = {}
    def pseudonym(self, subject, audience):
        payload = json.dumps([subject,audience],separators=(',',':')).encode()
        return hmac.new(self.key,payload,hashlib.sha256).hexdigest()
    def issue(self, subject, audience, scopes, expires):
        token = secrets.token_urlsafe(32)
        self.records[hashlib.sha256(token.encode()).hexdigest()] = {
            'subject':self.pseudonym(subject,audience),'audience':audience,
            'scopes':set(scopes),'expires':expires,'revoked':False}
        return token
    def verify(self, token, audience, scope, now):
        record = self.records.get(hashlib.sha256(token.encode()).hexdigest())
        return bool(record and not record['revoked'] and record['expires'] > now
                    and record['audience'] == audience and scope in record['scopes'])
    def revoke(self, token):
        record = self.records.get(hashlib.sha256(token.encode()).hexdigest())
        if record: record['revoked'] = True
def analyze(data):
    vault, tokens, results = CredentialVault(), {}, []
    for event in data.get('events',[]):
        if event['op'] == 'issue':
            if event['id'] in tokens: raise ValueError('Duplicate credential id')
            tokens[event['id']] = vault.issue(event['subject'],event['audience'],event['scopes'],event['expires'])
            results.append({'id':event['id'],'issued':True})
        elif event['op'] == 'check':
            results.append({'id':event['id'],'allowed':vault.verify(tokens.get(event['id'],''),event['audience'],event['scope'],event['now'])})
        elif event['op'] == 'revoke':
            vault.revoke(tokens.get(event['id'],''))
        else: raise ValueError('Unknown operation')
    return {'results':results,'stored_plaintext_tokens':False}

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Path to a JSON scenario')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError('Input must be a JSON object')
        print(json.dumps(analyze(data), indent=2, sort_keys=True))
    except (ValueError, TypeError, KeyError, OSError) as error:
        print('Input error: '+str(error), file=sys.stderr)
        sys.exit(2)
