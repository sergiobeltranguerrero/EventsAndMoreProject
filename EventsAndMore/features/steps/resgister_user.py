from behave import *


@when(u'I register client')
def step_impl(context):
    for row in context.table:

        # Go to register page
        context.browser.visit(context.get_url('register_client'))

        # Get register form
        form = context.browser.find_by_tag('form').first

        for heading in row.headings:
            context.browser.fill(heading, row[heading])
        form.find_by_value('Register').first.click()


@then(u'I\'m viewing the login page')
def step_impl(context):
    assert context.browser.url == context.get_url('login')


@then(u'there\'s a new client with the previous data')
def step_impl(context):
    from main.models.accounts import Cliente
    from django.contrib.auth.models import User

    assert User.objects.filter(username='patata').exists()
    user = User.objects.get(username='patata')
    assert Cliente.objects.filter(user=user).exists()
    client = Cliente.objects.get(user=user)

    assert client.user.first_name == 'Marc'
    assert client.user.username == 'patata'
    assert client.user.email == 'm@hotmail.com'
    assert client.address == 'Carrer'
    assert client.telephone == '642897511'
    assert client.cardNumber == 'ES9121000418450200051332'
    assert client.DNI == '78101067J'


@when(u'I register a client with wrong information')
def step_impl(context):
    for row in context.table:

        # Go to register page
        context.browser.visit(context.get_url('register'))

        # Get register form
        form = context.browser.find_by_tag('form').first

        for heading in row.headings:
            context.browser.fill(heading, row[heading])
        form.find_by_value('Register').first.click()


@then(u'I\'m able to see an error message')
def step_impl(context):
    assert context.browser.is_text_present('is not valid')


@then(u'I can click a link that takes me back to the register page')
def step_impl(context):
    context.browser.click_link_by_id('register')
    assert context.browser.is_element_present_by_value('Register')  # Register button


