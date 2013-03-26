import handlers.index
import handlers.auth

handlers = [
    (r'/', 			handlers.index.Handler),
    (r'/login', 	handlers.auth.LoginHandler),
    (r'/logout', 	handlers.auth.LogoutHandler),

#            (r'/add_message', AddHandler),
#            (r'/chatsocket', ChatSocketHandler)
]
