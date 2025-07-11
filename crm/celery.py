#!/usr/bin/env python3
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
from crm.schema import Mutation as CRMMutation
from crm.mutations import UpdateLowStockProducts
class Mutation(CRMMutation):
    update_low_stock_products = UpdateLowStockProducts.Field()
app.register_mutation(Mutation)
app.conf.beat_schedule = {
    'update-low-stock-every-12-hours': {
        'task': 'crm.cron.update_low_stock',
        'schedule': 43200.0,  # 12 hours in seconds
    },
}
# crm/celery.py
from django.conf import settings
from celery.schedules import crontab
from crm.cron import update_low_stock
# Register the periodic task
app.conf.beat_schedule = {
    'update-low-stock-every-12-hours': {
        'task': 'crm.cron.update_low_stock',
        'schedule': crontab(hour='*/12'),  # Every 12 hours
    },
}
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from crm.models import Customer, Product, Order
from crm.schema import CustomerNode, ProductNode, OrderNode
# ========================
# Mutation Definitions
# ========================

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    customer = graphene.Field(CustomerNode)

    def mutate(self, info, name, email):
        customer = Customer(name=name, email=email)
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
class Query(graphene.ObjectType):
    customer = graphene.relay.Node.Field(CustomerNode)
    product = graphene.relay.Node.Field(ProductNode)
    order = graphene.relay.Node.Field(OrderNode)

    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    all_orders = DjangoFilterConnectionField(OrderNode)
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
# ========================
# Schema Definition
# ========================
schema = graphene.Schema(query=Query, mutation=Mutation)
from crm.schema import Mutation as CRMMutation
from crm.mutations import UpdateLowStockProducts
class Mutation(CRMMutation):
    update_low_stock_products = UpdateLowStockProducts.Field()
app.register_mutation(Mutation)
app.conf.beat_schedule = {
    'update-low-stock-every-12-hours': {
        'task': 'crm.cron.update_low_stock',
        'schedule': 43200.0,  # 12 hours in seconds
    },
}
