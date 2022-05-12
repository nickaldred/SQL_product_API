



class Product:
    """
    Creates a object of a product.
    
    """

    def __init__(self, code, name, supplier, cost, rrp, pcsl, prsl) -> None:
        self.code = code
        self.name = name
        self.supplier = supplier
        self.cost = cost
        self.rrp = rrp
        self.pcsl = pcsl
        self.prsl = prsl
        