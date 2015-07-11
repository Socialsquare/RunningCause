from django.core.urlresolvers import reverse


def get_admin_url(inst):
    return reverse('admin:%s_%s_change' % (inst._meta.app_label,
                                           inst._meta.model_name),
                   args=[inst.pk])
