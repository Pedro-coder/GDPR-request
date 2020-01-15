import json

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from forms.models import Form, FormResponse, Opts

def form_responses(request, uuid):
    form = get_object_or_404(Form, uuid=uuid)
    responses = FormResponse.objects.filter(form=form.id)

    fields = form.get_fields().get('fields')
    fdict = OrderedDict()
    for k, v in fields.items():
        if v['tag'] in ['input', 'textarea', 'select'] and v['attrs'].get('type') != 'file':
            fdict[k] = v['config']['label']

    rdict = {}
    for obj in responses:
        for k in fdict.keys():
            if type(obj.response.get(k)).__name__ == 'list':
                txt_str = ''
                for i, item in enumerate(obj.response[k]):
                    if i == 0:
                        txt_str += item
                    else:
                        txt_str += ', ' + item
                rdict.setdefault(obj.uuid, []).append(txt_str)
            else:
                rdict.setdefault(obj.uuid, []).append(obj.response.get(k))

    template = "form_responses.html"
    template_vars = {'form': form, 'fdict': fdict, 'rdict': rdict}
    return render(request, template, template_vars)


def edit_response(request, uuid):
    response = get_object_or_404(FormResponse, uuid=uuid)
    form = Form.objects.get(id=response.form)

    fields = form.get_fields().get('fields')
    ldict = load_fields(fields)
    fdict = {k: {'type': v['attrs'].get('type'), 'tag': v['tag']} for k, v in fields.items() if v['tag'] in ['input', 'textarea', 'select'] and v['attrs'].get('type') != 'file'}

    res = response.response
    load_data = ''

    if form.configs:
        options = Opts.objects.all()
        categories = options.filter(category__isnull=True)
        opts = options.filter(category__isnull=False)
        cat_dict = {str(obj.id): [] for obj in categories}
        for opt in opts:
            cat_dict[str(opt.category_id)].append([opt.id, opt.value])

        load_data = load_configs(load_data, form, ldict, cat_dict)

    for k, v in fdict.items():
        if v['type'] == 'checkbox':
            if res.get(k):
                load_data += '$("#' + k + '").prop("checked", true); '
            else:
                # If checkbox is left blank
                load_data += '$("#' + k + '").prop("checked", false); '
        elif v['type'] == 'radio':
            if res.get(k):
                # If radio button is selected
                load_data += "$('input[type=radio][value=" + res.get(k) + "]').attr('checked', true); "
        else:
            if type(res.get(k, "")).__name__ == 'list':
                # For group selects
                val_list = list(obj for obj in res[k])
                load_data += '$("#' + k + '").select2("val", ' + str(val_list) + ').trigger("change"); '
            else:
                load_data += '$("#' + k + '").val("' + res.get(k, "") + '").trigger("change") ; '

    template = "edit_response.html"
    template_vars = {'response': response, 'form': form, 'load_data': load_data}
    return render(request, template, template_vars)



def ajax_save_rform(request):
    if request.method == 'POST':
        fid = request.POST.get('fid')
        rid = request.POST.get('rid')

        form_dict = {}
        for k, v in request.POST.items():
            if k not in ['csrfmiddlewaretoken', 'save', 'fid', 'rid', 'honeypot']:
                if len(request.POST.getlist(k)) > 1:
                    form_dict[k] = request.POST.getlist(k)
                else:
                    form_dict[k] = v

        if rid:
            res = FormResponse.objects.get(uuid=rid)
            res.response = form_dict
            res.save()
        else:
            FormResponse.objects.create(form=fid, response=form_dict)

        messages.success(request, 'Form Details Saved')
        return {'success': True}



def ajax_add_cat(request):
    if request.method == 'POST':
        name = request.POST.get('value')

        Opts.objects.create(value=name)

    return {'success': True}



def ajax_update_val(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        id = request.POST.get('id')
        value = request.POST.get('value')

        if action == 'add':
            val, created = Opts.objects.get_or_create(category_id=id, value=value)

            return {'success': True, 'vid': val.id}
        else:
            val = Opts.objects.get(id=id)
            val.delete()

            return {'success': True}

def ajax_load_val(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        opts = Opts.objects.filter(category_id=id).order_by('value')

        opt_list = []
        for opt in opts:
            opt_list.append([opt.value, opt.value])

        return {'success': True, 'opt_list': json.dumps(opt_list)}
