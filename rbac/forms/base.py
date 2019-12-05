# create: '2019/1/19' - 362416272@qq.com
from django import forms


class BootStrapModelForm(forms.ModelForm):
    """统一给modelform生成字段添加boot样式"""
    def __init__(self, *args, **kwargs):
        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        # 统一给modelform生成字段添加boot样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'layui-input'
