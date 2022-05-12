


class DataHandler():
    """
    Handles the data gathered from a SQL search.

    Input:
    data_list = list of products.
    """

    def __init__(self, data_list) -> None:
        self.data_list = data_list


    def find_low_stock(self) -> list:
        """
        Tranvereses list and returns the stock which is at
        less than a quarter of required.

        Output:

        low_stock - List of produts which have low stock.
        
        """
        low_stock = []

        for product in self.data_list:
            if product[5] < (product[6] / 4):
                low_stock.append(product)

        return low_stock

    def json_converter():
        pass

    def json_translater():
        pass

            