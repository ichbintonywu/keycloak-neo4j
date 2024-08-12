from neo4j import GraphDatabase
from neo4j import bearer_auth
from keycloak import KeycloakOpenID

class HelloWorldExample:
    def __init__(self, uri, token):
        self.driver = GraphDatabase.driver(uri, auth=bearer_auth(token))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
        "SET a.message = $message "
        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

def get_token():
    keycloak_openid = KeycloakOpenID(server_url="http://127.0.0.1:8080",
                                 client_id="neo4j-client",
                                 realm_name="myCorp")

    token = keycloak_openid.token("admin", "Ne04j!")
    access_token = token.get('access_token')
    print(f"Access Token: {access_token}")
    return access_token

if __name__ == "__main__":
    token = get_token()
    print(token)
    greeter = HelloWorldExample("neo4j://localhost:7617", token)
    greeter.print_greeting("hello, world")
    greeter.close()