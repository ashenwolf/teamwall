from lib import RequestHandler
import ldap


def verify_credentials(server, login, password):
    ldap_url = "ldap://" + server
    print ldap_url
    ldap_dn = "%s@%s" % (login, server)
    ldap_secret = password
    ldap_un = login

    ldap_base = "dc=" + ",dc=".join(server.split("."))
    ldap_scope = ldap.SCOPE_SUBTREE
    ldap_filter = "(&(objectClass=user)(sAMAccountName=" + ldap_un + "))"
    ldap_attrs = ["displayName", "sAMAccountName"]

    l = ldap.initialize(ldap_url)
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.protocol_version = 3
    l.simple_bind_s(ldap_dn, ldap_secret)

    r = l.search(ldap_base, ldap_scope, ldap_filter, ldap_attrs)
    ldap_type, ldap_user = l.result(r, 60)
    ldap_name, ldap_attrs = ldap_user[0]
    print ldap_user[0]
    if 'displayName' in ldap_attrs and 'sAMAccountName' in ldap_attrs:
        return {
            "display_name": ldap_attrs['displayName'][0],
            "account_name": ldap_attrs['sAMAccountName'][0],
        }

    return None


class LoginHandler(RequestHandler):
    def get(self):
        params = {
            "error": None,
            "login": "",
        }
        self.render("login.html", **params)

    def post(self):
        login, password = self.get_argument("login"), self.get_argument("password")
        server = self.application.auth_settings["active_directory"]["domain"]

        try:
            userinfo = verify_credentials(server, login, password)
            self.application.sync_db.users.update(
                {"account_name": userinfo["account_name"]},
                {
                    "$set": {"display_name": userinfo["display_name"]}
                },
                upsert=True)

            new_user = self.application.sync_db.users.find_one({"account_name": userinfo["account_name"]})
            self.set_secure_cookie("user_id", str(new_user["_id"]))
            self.redirect("/")
            return
        except ldap.LDAPError, e:
            if type(e.message) == dict and 'desc' in e.message:
                error = e.message['desc']
            else:
                error = str(e)

        params = {
            "error": error,
            "login": login,
        }

        self.render("login.html", **params)


class LogoutHandler(RequestHandler):
    def post(self):
        self.clear_all_cookies()
        self.redirect("/")
