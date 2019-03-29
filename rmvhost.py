import ui, vhoster

if __name__ == "__main__":
    vhoster = vhoster.VHoster()
      
    ui.block('DELTE VIRTUAL HOST')
    HOST_NAME = input('Host Domain Name:\n >> ')

    vhoster.delete(HOST_NAME)    
    vhoster.restart_apache()
    
    ui.block('FINISHED')