from django.db.models import Sum
from django.utils.formats import number_format
from products.models import Product
from outflows.models import Outflow


def __format_monetary_number(value):
    return number_format(value, decimal_pos=2, force_grouping=True)


def get_product_metrics():
    products = Product.objects.all()
    
    total_cost_price = sum(product.cost_price * product.quantity for product in products)
    total_selling_price = sum(product.selling_price * product.quantity for product in products)
    total_quantity = sum(product.quantity for product in products)
    total_profit = total_selling_price - total_cost_price
    
    return dict(
        total_cost_price=__format_monetary_number(total_cost_price),
        total_selling_price=__format_monetary_number(total_selling_price),
        total_quantity=total_quantity,
        total_profit=__format_monetary_number(total_profit),
    )
    
    
def get_sales_metrics():
    
    total_sales = Outflow.objects.count()
    total_products_sold = Outflow.objects.aggregate(total_products_sold=Sum('quantity'))['total_products_sold'] or 0
    total_sales_value = sum(outflow.quantity * outflow.product.selling_price for outflow in Outflow.objects.all())
    total_sales_cost = sum(outflow.quantity * outflow.product.cost_price for outflow in Outflow.objects.all())
    total_sales_profit = total_sales_value - total_sales_cost
    
    return dict(
        total_sales=total_sales,
        total_products_sold=total_products_sold,
        total_sales_value=__format_monetary_number(total_sales_value),
        total_sales_profit=__format_monetary_number(total_sales_profit),
    )