



class Product:
    """
    Creates a object of a product.

    Input:
    code: String - Code for product - Primary key.
    name: String - Name/description of product.
    supplier: String - Name of supplier.
    cost: Float - Cost of product (ex-VAT).
    rrp: Float - Retail price of product (ex-VAT).
    pcsl: Int - Current stock level of product.
    prsl: Int - Required stock level of product. 


    
    """

    def __init__(self, code, name, supplier, cost, rrp, pcsl, prsl) -> None:
        self.code = code
        self.name = name
        self.supplier = supplier
        self.cost = cost
        self.rrp = rrp
        self.pcsl = pcsl
        self.prsl = prsl
        