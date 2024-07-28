class NoPageProtocoloManiobraException(Exception):
    def __init__(self):
        super().__init__('LA PÁGINA QUE ABRIÓ NO ES LA DE PROTOCOLOS DE MANIOBRA')

class NoProtocolosManiobrasException(Exception):
    def __init__(self):
        super().__init__('NO HAY PROTOCOLOS DE MANIOBRAS PARA ESTA SEMANA')


class NoDownloadProtManiException(Exception):
    def __init__(self):
        super().__init__('NO SE DESCARGÓ CORRECTAMENTE EL ARCHIVO DE PROTOCOLOS DE MANIOBRAS DE ESTA SEMANA')