#!/usr/bin/env python3
import re, sys
from email import policy
from email.parser import Parser
URL_RE = re.compile(r'\bhttps?://[^\s"<>\]]+')
def parse_eml(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        msg = Parser(policy=policy.default).parse(f)
    iocs = { 'from': msg.get('from'), 'to': msg.get('to'),
             'subject': msg.get('subject'), 'date': msg.get('date'),
             'message_id': msg.get('message-id') }
    body_text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type().startswith("text/"):
                try: body_text += part.get_content()
                except: body_text += part.get_payload(decode=True) or ""
    else:
        try: body_text = msg.get_content()
        except: body_text = msg.get_payload(decode=True) or ""
    urls = URL_RE.findall(body_text or "")
    iocs['urls'] = sorted(set(urls))
    return iocs
def main():
    if len(sys.argv) < 2:
        print("Usage: parse_eml.py <file.eml>"); sys.exit(1)
    iocs = parse_eml(sys.argv[1])
    print("--- IOCs ---")
    for k,v in iocs.items():
        if isinstance(v,list):
            print(f"{k}:"); 
            [print("  -", i) for i in v]
        else:
            print(f"{k}: {v}")
if __name__=='__main__':
    main()
