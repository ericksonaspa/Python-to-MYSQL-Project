import ipaddress
import tabulate
import pyfiglet
import sys
import csv
import re
import mysql.connector

def main():
    try:
        if len(sys.argv) == 1 and sys.argv[0] == "project.py":

            #Print ASCII Art
            result = pyfiglet.figlet_format(text = "IP Subnet Calculator")
            print(result)

            #Ask for an IP in CIDR Format
            ip = input("Enter your IPv4 Address (CIDR format): ")
            print(f"The network address is {get_netID(ip)}.\nThe broadcast address is {get_broadcastID(ip)}.\nTotal number of hosts is {get_numhosts(ip)}.\nIt's {ip_class(ip)}.\nAlso, it's a {public_or_private(ip)}.")

            con = mysql.connector.connect(host='localhost', database='subnetdb', user='awsuser', password='awspassword')
            query = "INSERT INTO subnet_table (NETWORK ID, BROADCAST ID, NUMBER OF HOSTS, CLASS, PUBLIC/PRIVATE) VALUES ('" + get_netID(ip) + "', '" + get_broadcastID(ip) + "', '" + get_numhosts(ip) + "', '" + ip_class(ip) + "', '" + public_or_private(ip) + "')"
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            cur.close()

            with open('project.csv', "r", newline='') as file:
                reader = csv.DictReader(file)
                with open('project.csv', 'a', newline='') as file: #create a CSV file and append outputs from user inputs
                    writer = csv.DictWriter(file, fieldnames=["NETWORK ID", "BROADCAST ID", "NUMBER OF HOSTS", "CLASS", "PUBLIC/PRIVATE"])
                    writer.writerow({"NETWORK ID": get_netID(ip), "BROADCAST ID": get_broadcastID(ip), "NUMBER OF HOSTS": get_numhosts(ip), "CLASS": ip_class(ip), "PUBLIC/PRIVATE": public_or_private(ip)})

        if len(sys.argv) == 2 and sys.argv[1][-4:] == ".csv":
            if sys.argv[1] == "project.csv":
                with open("project.csv", "r") as file:
                    reader = csv.DictReader(file)
                    print(tabulate.tabulate(reader, headers="keys", tablefmt="grid", stralign='center'))
            else:
                sys.exit("File does not exist")

        elif len(sys.argv) > 2:
            sys.exit("Too many command-line arguments")
        elif len(sys.argv) == 2 and not sys.argv[1].endswith(".csv"):
            sys.exit("Not a CSV file")

    except FileNotFoundError:
        sys.exit("File does not exist")
    except ValueError:
        sys.exit("Invalid! Format e.g. 192.168.1.16/24")

#Network Address
def get_netID(ip):
    #address, netmask = ip.split("/")
    network_ID = ipaddress.IPv4Network(ip, False)
    return str(network_ID)

#Broadcast Address
def get_broadcastID(ip):
    address, netmask = ip.split("/")
    network_ID = ipaddress.IPv4Network(address + "/" + netmask, False)
    broadcast_ID = str(network_ID.broadcast_address)
    return broadcast_ID

#Number of Hosts
def get_numhosts(network_ID):
    num_of_hosts = ipaddress.ip_network(get_netID(network_ID)).num_addresses
    return num_of_hosts

#IP Class using RegEx
def ip_class(ip):
    if matches := re.search(r"^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])/?([1-9]|1[0-9]|2[0-9]|3[0-2])?$", ip):

        #0-127
        if int(matches.group(1)) >= 0 and int(matches.group(1)) <= 127 and int(matches.group(5)) >= 8 or int(matches.group(5)) <= 15:
            return "Class A"
        elif int(matches.group(1)) >= 0 and int(matches.group(1)) <= 127 and int(matches.group(5)) >= 16 or int(matches.group(5)) <= 23:
            return "Class B"
        elif int(matches.group(1)) >= 0 and int(matches.group(1)) <= 127 and int(matches.group(5)) >= 24 or int(matches.group(5)) <= 32:
            return "Class C"

        #128-191
        elif int(matches.group(1)) >= 128 and int(matches.group(1)) <= 191 and int(matches.group(5)) >= 8 or int(matches.group(5)) <= 15:
            return "Class A"
        elif int(matches.group(1)) >= 128 and int(matches.group(1)) <= 191 and int(matches.group(5)) >= 16 or int(matches.group(5)) <= 23:
            return "Class B"
        elif int(matches.group(1)) >= 128 and int(matches.group(1)) <= 191 and int(matches.group(5)) >= 24 or int(matches.group(5)) <= 32:
            return "Class C"

        #192-223
        elif int(matches.group(1)) >= 192 and int(matches.group(1)) <= 223 and int(matches.group(5)) >= 8 or int(matches.group(5)) <= 15:
            return "Class A"
        elif int(matches.group(1)) >= 192 and int(matches.group(1)) <= 223 and int(matches.group(5)) >= 16 or int(matches.group(5)) <= 23:
            return "Class B"
        elif int(matches.group(1)) >= 192 and int(matches.group(1)) <= 223 and int(matches.group(5)) >= 24 or int(matches.group(5)) <= 32:
            return "Class C"

#IPv4 Public or Private
def public_or_private(ip):
    if matches := re.search(r"^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])/?([1-9]|1[0-9]|2[0-9]|3[0-2])?$", ip):
        #Class A
        if int(matches.group(1)) == 10:
            return "Private IP"
        #Class B
        if int(matches.group(1)) == 172 and int(matches.group(2)) >= 16 and int(matches.group(2)) <= 31:
            return "Private IP"
        #Class C
        if int(matches.group(1)) == 192 and int(matches.group(2)) == 168:
            return "Private IP"
        else:
            return "Public IP"

if __name__ == "__main__":
    main()
