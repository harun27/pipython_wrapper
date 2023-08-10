from PI import devices, search

model = 'C-877'
sn = '0117034958'
stage = 'U-651.04H'

search.search_all()
turnt = devices.turntable()
turnt.connect_device(model, sn, stage)
turnt.print_vel()
turnt.set_vel(500)
turnt.print_vel()
print("number of stages are: " + str(turnt.get_numaxes()))
turnt.test_stages()
turnt.print_pos()
turnt.home()
turnt.print_pos()
turnt.move_absrot(500)
turnt.print_pos()
turnt.move_relrot(-300)
turnt.print_pos()
turnt.move_absrot(-300)
turnt.print_pos()