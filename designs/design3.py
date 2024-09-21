from base_design import BaseDesign

class Design3(BaseDesign):
    def register_design(self):
        return "Design 3", self.draw_design

def register_design():
    return Design3().register_design()