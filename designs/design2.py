from base_design import BaseDesign

class Design2(BaseDesign):
    def register_design(self):
        return "Design 2", self.draw_design

def register_design():
    return Design2().register_design()