


class departamento:    
    def __init__(self,name, hashtag, type):
        self.name = name
        self.hashtag = hashtag
        self.type = type

class departamentos:
    set_of_departamentos = []
    def __init__(self):
        self.departamentos = []
        self.departamentos.append(departamento('alta verapaz','#AltaVerapaz',2))
        self.departamentos.append(departamento('baja verapaz','#BajaVerapaz',2))
        self.departamentos.append(departamento('chimaltenango','#Chimaltenango',1))
        self.departamentos.append(departamento('chiquimula','#Chiquimula',1))
        self.departamentos.append(departamento('escuintla','#Escuintla',1))
        self.departamentos.append(departamento('guatemala','#Guatemala',1))
        self.departamentos.append(departamento('huehuetenango','#Huehuetenango',1))
        self.departamentos.append(departamento('izabal','#Izabal',1))
        self.departamentos.append(departamento('jalapa','#Jalapa',1))
        self.departamentos.append(departamento('jutiapa','#Jutiapa',1))
        self.departamentos.append(departamento('petén','#Petén',1))
        self.departamentos.append(departamento('el progreso','#ElProgreso',2))
        self.departamentos.append(departamento('quetzaltenango','#Quetzaltenango',1))
        self.departamentos.append(departamento('quiché','#Quiché',1))
        self.departamentos.append(departamento('retalhuleu','#Retalhuleu',1))
        self.departamentos.append(departamento('sacatepéquez','#Sacatepéquez',1))
        self.departamentos.append(departamento('san marcos','#SanMarcos',2))
        self.departamentos.append(departamento('santa rosa','#SantaRosa',2))
        self.departamentos.append(departamento('sololá','#Sololá',1))
        self.departamentos.append(departamento('suchitepéquez','#Suchitepéquez',1))
        self.departamentos.append(departamento('totonicapán','#Totonicapán',1))
        self.departamentos.append(departamento('zacapa','#Zacapa',1))
    def getDepartamentos(self):
        return self.departamentos
    def getDepartamentosBy(self, parameter):
        return list(filter(lambda c:c.type == parameter, self.departamentos))