from jinja2 import Template


def deploy_data_check(data, is_docker=True):
    err_msg = None

    def check_input_type(input_type, check_input, checker, value, msg):
        nonlocal err_msg
        if err_msg is not None:
            return

        if input_type != check_input:
            return

        is_pass = checker(value)
        if not is_pass:
            err_msg = msg

    if is_docker:
        run_args = data.get("run_args", [])
        for arg in run_args:
            required = arg.get("required", True)
            input_type = arg.get("type", None)
            value = arg.get("value", None)
            label = arg.get("label", "")
            if required and not value:
                return False, "{}应该为必填参数".format(label)

            check_input_type(input_type, "string", lambda x: isinstance(x, str), value, "{}应该为字符串".format(label))
            check_input_type(input_type, "int", lambda x: isinstance(x, int), value, "{}应该为整数值".format(label))
            check_input_type(input_type, "list", lambda x: isinstance(x, list), value, "{}应该为列表数据".format(label))
            check_input_type(input_type, "dict", lambda x: isinstance(x, dict), value, "{}应该为字典数据".format(label))
            check_input_type(input_type, "password", is_password, value, "{}应该包含大小写字母、数字及特殊字符".format(label))
            check_input_type(input_type, "ip", is_ip, value, "{}应该为合法IP".format(label))
            check_input_type(input_type, "number", is_number, value, "{}应该为数值".format(label))
            check_input_type(input_type, "url", is_url, value, "{}应该为合法URL".format(label))
            check_input_type(input_type, "domain", is_domain, value, "{}应该为合法域名".format(label))

            if err_msg is not None:
                return False, err_msg

        return True, data
    else:
        return True, data


def is_password(source):
    lower_letters = "abcdefghijklmnopqrstuvwxyz"
    upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special_letters = "!@#$%^&*()_+,.-="
    number_letters = "0123456789"
    all_letters = [lower_letters, upper_letters, special_letters, number_letters]
    for letters in all_letters:
        tag = False
        for s in source:
            if s in letters:
                tag = True
                break
        if not tag:
            return False
    return True


def is_ip(source):
    regex = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    return True if regex.match(source) else False


def is_number(source):
    try:
        float(source)
    except Exception:
        return False
    return True


def is_url(source):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return True if regex.match(source) else False


def is_domain(source):
    regex = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if regex.match(source) else False


def gen_unique_str(length=8):
    # 生成唯一字符串
    lower_letters = "abcdefghijklmnopqrstuvwxyz"
    upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special_letters = "!@#$%^&*()_+,.-="
    number_letters = "0123456789"
    all_letters = [lower_letters, upper_letters, special_letters, number_letters]
    alphabet = "".join(all_letters)
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (
                any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in special_letters for c in password)
        ):
            break
    return password


def gen_desc_doc(source_data, var_dict):
    if not source_data or not var_dict:
        return source_data

    special1 = "#%#@#)1"
    special2 = "#%#@#)2"
    special3 = "#%#@#)3"
    values = []
    while True:
        start = source_data.rfind("{{")
        if start < 0:
            break
        tmps = source_data[start:]
        end = tmps.find("}}")
        subs = source_data[start:start + end + 2]
        key = source_data[start + 2:start + end]
        values.append(var_dict.get(key, ""))
        source_data = source_data.replace(subs, special1)

    source_data = source_data.replace("{", special2)
    source_data = source_data.replace("}", special3)
    source_data = source_data.replace(special1, "{}")
    values.reverse()
    source_data = source_data.format(*values)
    source_data = source_data.replace(special2, "{")
    source_data = source_data.replace(special3, "}")
    return source_data


def gen_desc_doc_by_jinja2(source_data, var_dict):
    if not source_data or not var_dict:
        return source_data

    values = {}
    index = len(source_data)
    while True:
        start = source_data.rfind("{{", 0, index)
        if start < 0:
            break
        index = start
        tmps = source_data[start:]
        end = tmps.find("}}")
        key = source_data[start + 2:start + end]
        values.update({key: var_dict.get(key, "")})

    template = Template(source_data)
    source_data = template.render(values)
    return source_data
