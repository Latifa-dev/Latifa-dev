import subprocess
import logging
import logging.handlers



##Ici toutes les foctions vont être exécutés via ssh aux postes distants



def run_command(cmd: str, shell=False, stdin=subprocess.PIPE):
    logging.debug("run_command:")
    if not shell:
        cmd = cmd.split()
    output = subprocess.check_output(cmd, shell=shell, stdin=stdin).decode("utf-8")
    logging.debug("   output: " + output)
    return output



#Connexion via ssh au poste distant


def ssh_to_server(host, port, username):
    remoteClient = f"{username}@{host}"
    logging.debug(f"ssh_to_server {remoteClient} port {port}")
    sshProcess = subprocess.Popen(
        ["ssh", "-tt", remoteClient, "-p", port],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=0,
    )
    return sshProcess



#Fonction scan du réseau à partir des deux plages d'adresses 192.168.100.0/24 et 192.168.0.101.0/24 en excluant l'adresse broadcast et récupération des adresses connectés

def scan():

    logging.debug("scan:")
    scanRes = run_command(
        "nmap -PR 192.168.100.0/24 192.168.101.0/24 --exclude 192.168.101.254,192.168.100.254| egrep \"scan report\" | awk '{print $5}'",
        shell=True,
        stdin=subprocess.PIPE,
    )
    logging.debug("   scan result: " + scanRes)
    return scanRes





#Fonction supression d'utilisateurs stagiares et ses fichiers


def delete_user(sshProcess: subprocess.Popen, user="stagiaire"):
    logging.debug("delete_user")
    print("Suppression utilisateur")
    cmd = f"sudo userdel -rf {user}\n"
    sshProcess.stdin.write(cmd)




#Ajout d'un nouveau utilisateur stagiaire


def add_user(sshProcess: subprocess.Popen, user="stagiaire"):
    logging.debug("add_user")
    print("Création utilisateur stagiaire")
    pwd = "stagiaire123"
    commands = [
        f'sudo useradd -p $(openssl passwd -1 stagiaire123) {user}',
        f"sudo mkdir -p /home/{user}",
        f"sudo chown -R {user} /home/{user}",
        f"sudo chown -R 755 /home/{user}",
    ]
    for cmd in commands:
        sshProcess.stdin.write(cmd + "\n")




#Création du hostname unique         


def hostname(sshProcess: subprocess.Popen):
    logging.debug("hostname")
    commands = [
        "ip=$(ip a |grep \"inet 192.168\" |cut -f 1 -d '/')",
        'lan=$(echo "$ip"|cut -d. -f3)',
        'pc=$(echo "$ip"|cut -d. -f4)',
        'if [ "$lan" = "101" ]; then hostname=(baobab-"$pc"); elif [ "$lan" = "100" ]; then hostname=(abeille-"$pc"); fi',
        "sudo hostname $hostname",
        'echo "le hostname est" $hostname',
    ]
    for cmd in commands:
        logging.debug("   cmd: " + cmd)
        sshProcess.stdin.write(cmd + "\n")



#Création d'un dossier partagé pour les stagiaires appelé Formation

def nfs(sshProcess: subprocess.Popen):
    logging.debug("nfs")
    sshProcess.stdin.write(
        'if [ ! -d "/home/Formation" ]; then sudo mkdir /home/Formation; fi\n'
    )



#Reboot la machine distante



def reboot(sshProcess: subprocess.Popen):
    logging.debug("reboot")
    sshProcess.stdin.write("sudo reboot\n")