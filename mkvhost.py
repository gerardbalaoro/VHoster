import ui, vhoster

if __name__ == "__main__":
    vhoster = vhoster.VHoster()

    ui.block('CREATE VIRTUAL HOST')
    HOST_NAME = input('Host Domain Name: ')
    HOST_PATH = input('Host Root Folder: ')
    HOST_PORT = input('Host Port [80]: ')
    
    vhoster.create(HOST_NAME, HOST_PATH, HOST_PORT if HOST_PORT else 80)     
    vhoster.restart_apache()

    ui.block('FINISHED')