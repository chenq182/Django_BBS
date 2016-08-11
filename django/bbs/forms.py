# coding=utf8
from django import forms
from django.core.exceptions import ValidationError

from .models import Client, User


class ReplyForm(forms.Form):
    text = forms.CharField(
        label='正文',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '正文',
            }),
        min_length=4,
        max_length=500,
        error_messages={
            'required': '正文不能为空',
            'min_length': '正文长度为4-500字符',
            'max_length': '正文长度为4-500字符',
        })


class New_PostForm(forms.Form):
    topic = forms.CharField(
        label='主题',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '主题',
            }),
        min_length=4,
        max_length=30,
        error_messages={
            'required': '主题不能为空',
            'min_length': '主题长度为4-30字符',
            'max_length': '主题长度为4-30字符',
        })
    text = forms.CharField(
        label='正文',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '正文',
            }),
        min_length=4,
        max_length=500,
        error_messages={
            'required': '正文不能为空',
            'min_length': '正文长度为4-500字符',
            'max_length': '正文长度为4-500字符',
        })
    files = forms.FileField(
        label='附件',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
        }))


def validate_username_exist(value):
    if Client.objects.filter(username=value).count() > 0:
        raise ValidationError(
            '用户名%(value)s已存在',
            params={'value': value},
        )
def validate_nickname_exist(value):
    if User.objects.filter(name=value).count() > 0:
        raise ValidationError(
            '昵称%(value)s已存在',
            params={'value': value},
        )

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '用户名',
            }),
        min_length=4,
        max_length=20,
        validators=[validate_username_exist],
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名长度为4-20字符',
            'max_length': '用户名长度为4-20字符',
        })
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '密码',
            }),
        min_length=6,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度为6-20字符',
        })
    nickname = forms.CharField(
        label='昵称',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '昵称',
            }),
        min_length=4,
        max_length=20,
        validators=[validate_nickname_exist],
        error_messages={
            'required': '昵称不能为空',
            'min_length': '昵称长度为4-20字符',
            'max_length': '昵称长度为4-20字符',
        })

