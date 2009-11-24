from shared.packet import Packet

def require_login(func):
    def new_func(connection, pack):
        if connection.user is None:
            response = Packet("login_required")
            connection.out_queue.put(response)
        else:
            return func(connection, pack)
    return new_func

