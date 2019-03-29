import ui, vhoster

if __name__ == "__main__":
    vhoster = vhoster.VHoster()
      
    ui.block('DELTE VIRTUAL HOST')
    HOST_NAME = input('Host Domain Name:\n >> ')

    delete_host(HOST_NAME)    
    restart_apache(CONFIG)
    
    ui.block('FINISHED')