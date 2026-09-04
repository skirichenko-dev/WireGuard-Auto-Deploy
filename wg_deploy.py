import argparse
import os
from datetime import datetime

def generate_keys():
    """Эмуляция генерации ключей (в проде используется subprocess и вызов wg genkey)"""
    # Для демонстрации логики работы скрипта возвращаем заглушки
    return "priv_mock_key_8xO=", "pub_mock_key_9yP="

def create_client_config(client_name, ip_address, server_pub_key, endpoint):
    priv_key, pub_key = generate_keys()
    config = f"""[Interface]
PrivateKey = {priv_key}
Address = {ip_address}/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = {server_pub_key}
Endpoint = {endpoint}:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
    os.makedirs("configs", exist_ok=True)
    filename = f"configs/{client_name}_{datetime.now().strftime('%Y%m%d')}.conf"
    
    with open(filename, "w") as f:
        f.write(config)
        
    return filename, pub_key

def main():
    parser = argparse.ArgumentParser(description="WireGuard VPN Auto-Deploy & Config Manager")
    parser.add_argument("--add", help="Имя нового клиента (например, user_macbook)", type=str)
    parser.add_argument("--ip", help="Внутренний IP-адрес клиента (например, 10.8.0.2)", type=str)
    parser.add_argument("--endpoint", help="Внешний IP-адрес сервера", default="192.168.1.100")
    
    args = parser.parse_args()

    if args.add and args.ip:
        print(f"[*] Начало генерации конфигурации для пира: {args.add}")
        server_pub = "SERVER_PUBLIC_KEY_PLACEHOLDER"
        
        filepath, pub_key = create_client_config(args.add, args.ip, server_pub, args.endpoint)
        
        print(f"[+] Успешно! Файл конфигурации сохранен: {filepath}")
        print(f"[i] Публичный ключ клиента для добавления на сервер: {pub_key}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
