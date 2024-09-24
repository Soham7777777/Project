import time
from flask import render_template_string
from dataclasses import dataclass, field, KW_ONLY

@dataclass
class BaseComponent:
    """Parts of UI which have contents that is stored in database, in other words dynamic ui."""
    _: KW_ONLY
    element_id: str = field(default_factory=lambda: ''.join(str(time.time()).split('.')), init=False)
    template_path: str
    macroname: str

    def render(self):
        return render_template_string(f'''
            {"{%"} import {self.template_path} as templ {"%}"}
            {"{{"} templ.{self.macroname}(component) {"}}"}
        ''', component=self)

@dataclass
class ToastComponent(BaseComponent):
    template_path: str = field(init=False, default='components/toast.html')
    macroname: str = field(init=False, default='ToastMacro')

    header: str
    header_text_color: str
    icon_name: str
    body: str | None = None

@dataclass
class OOBComponent(BaseComponent):
    template_path: str = field(init=False, default='components/oob.html')
    macroname: str = field(init=False, default='OOBMacro')

    element_id: str = field()
    tag: str
    hx_swap_oob: str
    content: str
