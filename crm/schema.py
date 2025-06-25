# graphql_crm/schema.py

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from graphene_django import DjangoObjectType

from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

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

class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    all_orders = DjangoFilterConnectionField(OrderNode)
    customer = graphene.relay.Node.Field(CustomerNode)
    product = graphene.relay.Node.Field(ProductNode)
    order = graphene.relay.Node.Field(OrderNode)
    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()
    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()
    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
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
        customers = graphene.List(graphene.NonNull(CustomerNode))

    created_customers = graphene.List(CustomerNode)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created = []
        errors = []
        for customer_data in customers:
            try:
                customer = Customer(name=customer_data.name, email=customer_data.email, phone=customer_data.phone)
                customer.full_clean()
                customer.save()
                created.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(created_customers=created, errors=errors)

