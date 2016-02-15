from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def render_mail(self, template_prefix, email, context):
        # Injecting the BASE_URL to the templates.
        context.update({
            'BASE_URL': settings.BASE_URL
        })
        return super(AccountAdapter, self).render_mail(template_prefix,
                                                       email,
                                                       context)
