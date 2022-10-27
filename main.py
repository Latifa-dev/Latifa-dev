from utils import *

PORT = "22"
USERNAME = "latifa"


def main():
    scanRes = scan()
    ips = set([ip.strip() for ip in scanRes.split("\n")])
    for ip in ips:
        logging.debug("IP: " + ip)
        if not ip:
            logging.debug("skipping empty IP address")
            continue
        sshProcess = ssh_to_server(str(ip), PORT, USERNAME)
        delete_user(sshProcess)
        add_user(sshProcess)
        hostname(sshProcess)
        nfs(sshProcess)
        reboot(sshProcess)
        sshProcess.stdin.close()
        returnCode = sshProcess.wait()
        logging.debug(f"return code for ip {ip} : {str(returnCode)}")
        logging.debug('STDOUT:')
        for line in sshProcess.stdout:
            logging.debug(line)


if __name__ == "__main__":
    main()
