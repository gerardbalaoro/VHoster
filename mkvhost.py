import ui, vhoster

if __name__ == "__main__":
    vhoster = vhoster.VHoster()

    ui.block('CREATE VIRTUAL HOST')
    HOST_NAME = input('Host Domain Name: ')
    HOST_PATH = input('Host Root Folder: ')
    HOST_PORT = input('Host Port [80]: ') or 80
    
    create_host(HOST_NAME, HOST_PATH, HOST_PORT)     
    restart_apache(CONFIG)

    ui.block('FINISHED')