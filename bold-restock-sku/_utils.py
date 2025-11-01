def proxy_config(proxy):
    parsed_proxy = None
    try:
        (IPv4, Port, username, password) = proxy.split(':')
        ip = IPv4 + ':' + Port
        parsed_proxy = {
            "http": "http://" + username + ":" + password + "@" + ip,
            "https": "http://" + username + ":" + password + "@" + ip,
        }
    except ValueError:
        print("Invalid proxy.", "f")
        exit(1)
    return parsed_proxy
