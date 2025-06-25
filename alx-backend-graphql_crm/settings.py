# alx_backend_graphql_crm/settings.py

INSTALLED_APPS = [
    ...,
    'graphene_django',
    'django_filters',
    'crm',
]

GRAPHENE = {
    'SCHEMA': 'alx_backend_graphql_crm.schema.schema',
}
