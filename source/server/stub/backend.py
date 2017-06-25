
def handle_page_login(args):

    if args['entry_type'] == 'signin':
        panel_title = 'SIGN IN'
    elif args['entry_type'] == 'signup':
        panel_title = 'SIGN UP'
    else:
        return None

    return {
            'page_title': 'Welcome to Doczone !',
            'panel_title': panel_title,
        }

def handle_action_login(args):

    print args
