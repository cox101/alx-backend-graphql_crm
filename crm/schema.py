import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from crm.models import Customer, Product, Order
from crm.filters import CustomerFilter, ProductFilter, OrderFilter

# ========================
# Node Definitions
# ========================

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)

# ========================
# Mutations
# ========================

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerNode)

    def mutate(self, info, name, email, phone=None):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(graphene.JSONString)  # JSON input

    created_customers = graphene.List(CustomerNode)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created = []
        errors = []
        for data in customers:
            try:
                customer = Customer(**data)
                customer.full_clean()
                customer.save()
                created.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(created_customers=created, errors=errors)


class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.Boolean()
    updated_products = graphene.List(graphene.String)

    def mutate(self, info):
        updated = []
        for product in Product.objects.filter(stock__lt=10):
            product.stock += 10
            product.save()
            updated.append(f"{product.name} - {product.stock}")
        return UpdateLowStockProducts(success=True, updated_products=updated)


# ========================
# Main Mutation Class
# ========================

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()
    # Extend here with more: update_customer, delete_order, etc.

# ========================
# Query Definitions
# ========================

class Query(graphene.ObjectType):
    customer = graphene.relay.Node.Field(CustomerNode)
    product = graphene.relay.Node.Field(ProductNode)
    order = graphene.relay.Node.Field(OrderNode)

    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    all_orders = DjangoFilterConnectionField(OrderNode)

    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()

# ========================
# Final Schema
# ========================

schema = graphene.Schema(query=Query, mutation=Mutation)
