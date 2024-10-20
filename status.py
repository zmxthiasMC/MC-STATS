import socket
import json
import requests
from colorama import init, Fore, Style

init(autoreset=True)

def get_server_info(ip, port, edition):
    if edition.lower() == "java":
        return get_java_server_info(ip, port)
    elif edition.lower() == "bedrock":
        return get_bedrock_server_info(ip, port)
    else:
        return {"error": "Edición no soportada. Usa 'Java' o 'Bedrock'."}

def get_java_server_info(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, int(port)))
        sock.send(b'\xFE\x01')
        data = sock.recv(1024)
        sock.close()
        
        if data:
            data = data.split(b'\x00\x00\x00')
            motd = data[1].decode('utf-16be')
            players = data[4].decode('utf-16be')
            max_players = data[5].decode('utf-16be')
            return {
                "IP": ip,
                "Port": port,
                "MOTD": motd,
                "Players": players,
                "Max Players": max_players,
                "Edition": "Java"
            }
        else:
            return {"error": "No se pudo obtener información del servidor."}
    except Exception as e:
        return {"error": str(e)}

def get_bedrock_server_info(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        message = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00'
        sock.sendto(message, (ip, int(port)))
        data, _ = sock.recvfrom(1024)
        sock.close()
        
        if data:
            data = data.split(b';')
            motd = data[1].decode('utf-8')
            players = data[4].decode('utf-8')
            max_players = data[5].decode('utf-8')
            return {
                "IP": ip,
                "Port": port,
                "MOTD": motd,
                "Players": players,
                "Max Players": max_players,
                "Edition": "Bedrock"
            }
        else:
            return {"error": "No se pudo obtener información del servidor."}
    except Exception as e:
        return {"error": str(e)}

def get_additional_info(ip, port):
    try:
        response = requests.get(f"https://api.mcsrvstat.us/2/{ip}:{port}")
        if response.status_code == 200:
            data = response.json()
            return {
                "Host": data.get("hostname", "N/A"),
                "Protocol": data.get("protocol", "N/A"),
                "Plugins": data.get("plugins", {}).get("names", []),
                "Players": data.get("players", {}).get("list", []),
                "Online": data.get("online", False),
                "Version": data.get("version", "N/A"),
                "Software": data.get("software", "N/A"),
                "Ping": data.get("debug", {}).get("ping", "N/A"),
                "Worlds": data.get("worlds", []),
                "Lobby": data.get("lobby", "N/A"),
                "Protocol Version": data.get("protocol_version", "N/A"),
                "Server Type": data.get("server_type", "N/A"),
                "Uptime": data.get("uptime", "N/A"),
                "Player IPs": data.get("players", {}).get("sample", []),
                "Server Description": data.get("description", "N/A"),
                "Map": data.get("map", "N/A"),
                "Game Mode": data.get("gamemode", "N/A"),
                "Difficulty": data.get("difficulty", "N/A"),
                "Whitelist": data.get("whitelist", "N/A"),
                "Banned Players": data.get("banned_players", []),
                "Operators": data.get("operators", [])
            }
        else:
            return {"error": "No se pudo obtener información adicional del servidor."}
    except Exception as e:
        return {"error": str(e)}

def print_status_logo():
    logo = f"""
{Fore.LIGHTGREEN_EX}  
{Fore.LIGHTGREEN_EX}░██████╗████████╗░█████╗░████████╗██╗░░░██╗░██████╗
{Fore.LIGHTGREEN_EX}██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║░░░██║██╔════╝
{Fore.LIGHTGREEN_EX}╚█████╗░░░░██║░░░███████║░░░██║░░░██║░░░██║╚█████╗░
{Fore.LIGHTGREEN_EX}░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░██║░░░██║░╚═══██╗
{Fore.LIGHTGREEN_EX}██████╔╝░░░██║░░░██║░░██║░░░██║░░░╚██████╔╝██████╔╝
{Fore.LIGHTGREEN_EX}╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚═════╝░╚═════╝░
    """
    print(logo)

def main():
    print_status_logo()
    
    ip = input("IP Del Servidor: ")
    port = input("Puerto Del Servidor: ")
    edition = input("¿Java o Bedrock?: ")
    
    server_info = get_server_info(ip, port, edition)
    additional_info = get_additional_info(ip, port)
    
    if "error" in server_info:
        print(Fore.RED + server_info["error"])
    else:
        server_info.update(additional_info)
        # Asegúrate de que todos los valores sean cadenas antes de serializar a JSON
        for key, value in server_info.items():
            if isinstance(value, bytes):
                server_info[key] = value.decode('utf-8')
        print(Fore.LIGHTGREEN_EX + json.dumps(server_info, indent=4))

if __name__ == "__main__":
    main()
        
