def menu():
    print('\nWelcome: Select Option: ')
    print('1) create vlan')
    print('2) update vlan')
    print('3) delete vlan')
    print('4) show vlans')
    print('5) sync')
    
    print('9) exit')

    option = input('option: ')
    while not option.isnumeric():
        print('Please, enter a digit!')
        option = input('option: ')

    return int(option)