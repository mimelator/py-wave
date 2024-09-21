from base_design import BaseDesign

class Design2(BaseDesign):
    pass

def register_design():
    return "Design2", Design2()