from django import forms


def IDValidator(value):
    # 身份证号码验证
    Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    Ti = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
    sum = 0
    # 身份证第十八位多是X，输入时将小写x转换为大写X
    value = value.upper()
    if len(value) != 18:
        raise forms.ValidationError("请输入18位身份证号码,您只输入了%s位" % len(value))
    for i in range(17):
        sum += int(value[i]) * Wi[i]
    if Ti[sum % 11] != value[17]:
        raise forms.ValidationError("请输入正确的身份证号码")
