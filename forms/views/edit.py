import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _

from collections import OrderedDict

from ..models import Form, Opts

# Create your views here.
def all_forms(request):
    forms = Form.objects.all().order_by('created')

    template = "all_forms.html"
    template_vars = {'forms': forms}
    return render(request, template, template_vars)

def edit_form(request, uuid):
    form = get_object_or_404(Form, uuid=uuid)

    template = "edit_form.html"
    template_vars = {'form': form}
    return render(request, template, template_vars)

def edit_config(request, uuid):
    form = get_object_or_404(Form, uuid=uuid)
    msel = ['select', 'checkbox-group', 'radio-group']

    cats = Opts.objects.filter(category__isnull=True)
    clist = [[0, _('Country')]]
    for c in cats:
        clist.append([c.id, c.value])
    clist = sorted(clist, key=lambda x: x[1])

    if request.method == 'POST':
        conf = {}

        for k, v in request.POST.items():
            if 'field~' in k and request.POST.get(k):
                conf[k.split('~')[1]] = int(request.POST.get(k))

        form.configs = conf
        form.save()

        messages.success(request, _('Form options saved!'))
        return redirect('edit-config', uuid)

    template = "configs/form_configs.html"
    template_vars = {'form': form, 'msel':msel, 'clist':clist}
    return render(request, template, template_vars)

def edit_tips(request, uuid):
    form = get_object_or_404(Form, uuid=uuid)

    for itm in form.fields:
        itm['tip'] = form.tips.get(itm['name'])

    if request.method == 'POST':
        tips = {}

        for k, v in request.POST.items():
            if 'field~' in k and request.POST.get(k):
                tips[k.split('~')[1]] = request.POST.get(k)

        form.tips = tips
        form.save()

        messages.success(request, _('Form tips saved!'))
        return redirect('edit-tips', uuid)

    template = "configs/form_tips.html"
    template_vars = {'form': form}
    return render(request, template, template_vars)



def form_options(request):
    options = Opts.objects.filter(category__isnull=False).order_by('value')
    cats = Opts.objects.filter(category__isnull=True)

    odict = OrderedDict()

    for x in cats:
        odict[x.id] = {'value':x.value, 'opts': []}
    for x in options:
        odict[x.category_id]['opts'].append(x)

    if request.method == 'POST':
        rp = request.POST
        if rp.get('action'):
            cat_id = int(rp.get('cat'))
            ovals = rp.get('ovals')

            olist = []

            if ovals:
                for x in ovals.split('\r\n'):
                    if x:
                        opt = Opts(value=x, category_id=cat_id)
                        olist.append(opt)
                Opts.objects.bulk_create(olist)
            messages.success(request, _('Options set saved!'))

        else:
            opt = Opts.objects.create(value=request.POST.get('name'))
            messages.success(request, _('Options set saved!'))
        return redirect('form-options')

    template = "configs/form_options.html"
    template_vars = {'odict': odict}
    return render(request, template, template_vars)

def ajax_edit_form(request):
    if request.method == 'POST':
        pk = int(request.POST.get('pk'))
        name = request.POST.get('value')

        if pk != 0:
            obj = Form.objects.get(id=pk)
            obj.name = name
            obj.save()
        else:
            Form.objects.create(name=name)

    return JsonResponse({'success': True})

def ajax_save_form(request):
    if request.method == 'POST':
        fid = request.POST.get('fid')
        fields = request.POST.get('data')
        form = Form.objects.get(id=fid)
        form.fields = json.loads(fields)
        form.save()
        return JsonResponse({'success': True})

