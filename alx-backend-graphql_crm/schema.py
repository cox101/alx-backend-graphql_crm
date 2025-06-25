import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import datetime
import re


# === Type Definitions ===
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order


# === Input Definitions ===
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


# === CreateCustomer Mutation ===
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise graphene.GraphQLError("Email already exists.")
        if input.phone and not re.match(r'^(\+?\d{10,15}|(\d{3}-\d{3}-\d{4}))$', input.phone):
            raise graphene.GraphQLError("Invalid phone format.")
        customer = Customer.objects.create(**input)
        return CreateCustomer(customer=customer, message="Customer created successfully.")


# === BulkCreateCustomers Mutation ===
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []

        for idx, data in enumerate(input):
            try:
                if Customer.objects.filter(email=data.email).exists():
                    raise ValueError(f"Customer {idx + 1}: Email '{data.email}' already exists.")
                if data.phone and not re.match(r'^(\+?\d{10,15}|(\d{3}-\d{3}-\d{4}))$', data.phone):
                    raise ValueError(f"Customer {idx + 1}: Invalid phone format.")
                customer = Customer(name=data.name, email=data.email, phone=data.phone)
                customer.full_clean()
                customer.save()
                created.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=created, errors=errors)


# === CreateProduct Mutation ===
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock):
        if price <= 0:
            raise graphene.GraphQLError("Price must be a positive value.")
        if stock < 0:
            raise graphene.GraphQLError("Stock cannot be negative.")
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


# === CreateOrder Mutation ===
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise graphene.GraphQLError("Customer not found.")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise graphene.GraphQLError("One or more product IDs are invalid.")
        if not product_ids:
            raise graphene.GraphQLError("You must provide at least one product.")

        total = sum(p.price for p in products)
        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            order_date=order_date or datetime.now()
        )
        order.products.set(products)
        return CreateOrder(order=order)
