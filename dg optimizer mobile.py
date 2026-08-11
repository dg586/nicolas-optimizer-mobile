
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

import shutil
import subprocess


# ============================================================
# CONFIGURAÇÃO
# ============================================================

USUARIO_CORRETO = "nicolas"
SENHA_CORRETA = "1234"

Window.clearcolor = (0.025, 0.027, 0.04, 1)


# ============================================================
# BOTÃO PERSONALIZADO
# ============================================================

class BotaoOptimizer(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.color = (1, 1, 1, 1)
        self.font_size = dp(14)

        with self.canvas.before:
            Color(
                0.055,
                0.075,
                0.13,
                1
            )

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

        self.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

    def atualizar_fundo(self, *args):

        self.fundo.pos = self.pos
        self.fundo.size = self.size


# ============================================================
# APP
# ============================================================

class NicolasOptimizer(App):

    def build(self):

        self.root_layout = BoxLayout(
            orientation="vertical"
        )

        self.mostrar_login()

        return self.root_layout

    # ========================================================
    # LOGIN
    # ========================================================

    def mostrar_login(self):

        self.root_layout.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=[
                dp(30),
                dp(50),
                dp(30),
                dp(30)
            ],
            spacing=dp(15)
        )

        titulo = Label(
            text="[b]NICOLAS[/b] [color=00E5FF][b]OPTIMIZER[/b][/color]",
            markup=True,
            font_size=dp(30),
            size_hint_y=None,
            height=dp(60)
        )

        subtitulo = Label(
            text="ANDROID OPTIMIZER",
            color=(0, 0.85, 0.65, 1),
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30)
        )

        descricao = Label(
            text="PAINEL DE OTIMIZAÇÃO E MANUTENÇÃO",
            color=(0.55, 0.60, 0.70, 1),
            font_size=dp(11),
            size_hint_y=None,
            height=dp(30)
        )

        self.usuario = TextInput(
            hint_text="Usuário",
            multiline=False,
            font_size=dp(17),
            size_hint_y=None,
            height=dp(55),
            padding=[
                dp(15),
                dp(15)
            ]
        )

        self.senha = TextInput(
            hint_text="Senha",
            password=True,
            multiline=False,
            font_size=dp(17),
            size_hint_y=None,
            height=dp(55),
            padding=[
                dp(15),
                dp(15)
            ]
        )

        self.status_login = Label(
            text="[color=A0A8C0]● AGUARDANDO LOGIN[/color]",
            markup=True,
            font_size=dp(12),
            size_hint_y=None,
            height=dp(35)
        )

        entrar = Button(
            text="ENTRAR",
            size_hint_y=None,
            height=dp(55),
            font_size=dp(17),
            background_normal="",
            background_color=(0, 0.65, 0.48, 1)
        )

        entrar.bind(
            on_release=self.verificar_login
        )

        self.senha.bind(
            on_text_validate=self.verificar_login
        )

        layout.add_widget(titulo)
        layout.add_widget(subtitulo)
        layout.add_widget(descricao)

        layout.add_widget(
            Label(
                size_hint_y=None,
                height=dp(20)
            )
        )

        layout.add_widget(self.usuario)
        layout.add_widget(self.senha)
        layout.add_widget(self.status_login)
        layout.add_widget(entrar)

        self.root_layout.add_widget(layout)

    # ========================================================
    # LOGIN
    # ========================================================

    def verificar_login(self, instance):

        usuario = self.usuario.text.strip()
        senha = self.senha.text

        if (
            usuario == USUARIO_CORRETO
            and senha == SENHA_CORRETA
        ):

            self.status_login.text = (
                "[color=00FF88]● LOGIN AUTORIZADO[/color]"
            )

            self.status_login.markup = True

            self.entrar_no_painel()

        else:

            self.status_login.text = (
                "[color=FF3B5C]"
                "● USUÁRIO OU SENHA INCORRETOS"
                "[/color]"
            )

            self.status_login.markup = True

    # ========================================================
    # PAINEL
    # ========================================================

    def entrar_no_painel(self):

        self.root_layout.clear_widgets()

        # HEADER

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100)
        )

        titulo = Label(
            text="[b]NICOLAS[/b] [color=00E5FF][b]OPTIMIZER[/b][/color]",
            markup=True,
            font_size=dp(28)
        )

        subtitulo = Label(
            text="PAINEL ANDROID",
            color=(0, 0.85, 0.65, 1),
            font_size=dp(11)
        )

        header.add_widget(titulo)
        header.add_widget(subtitulo)

        self.root_layout.add_widget(header)

        # STATUS

        self.status = Label(
            text="[color=00FF88]● SISTEMA PRONTO[/color]",
            markup=True,
            font_size=dp(12),
            size_hint_y=None,
            height=dp(35)
        )

        self.root_layout.add_widget(
            self.status
        )

        # SCROLL

        scroll = ScrollView()

        grid = GridLayout(
            cols=2,
            spacing=dp(12),
            padding=dp(12),
            size_hint_y=None
        )

        grid.bind(
            minimum_height=grid.setter(
                "height"
            )
        )

        botoes = [

            ("📱\nAPARELHO",
             self.info_aparelho),

            ("🔋\nBATERIA",
             self.bateria),

            ("💾\nARMAZENAMENTO",
             self.armazenamento),

            ("🌐\nREDE",
             self.rede),

            ("📶\nWI-FI",
             self.wifi),

            ("🔵\nBLUETOOTH",
             self.bluetooth),

            ("⚙\nCONFIGURAÇÕES",
             self.configuracoes),

            ("🛠\nDESENVOLVEDOR",
             self.desenvolvedor),

            ("🧹\nLIMPEZA",
             self.limpeza),

            ("🎮\nGAMING",
             self.gaming),

            ("📦\nAPLICATIVOS",
             self.aplicativos),

            ("🔊\nSOM",
             self.som),

            ("🔒\nBLOQUEAR TELA",
             self.bloquear_tela),

            ("🔄\nREINICIAR CELULAR",
             self.reiniciar),

            ("ℹ\nSISTEMA",
             self.sistema),

            ("🚪\nSAIR",
             self.mostrar_login)
        ]

        for texto, comando in botoes:

            botao = BotaoOptimizer(
                text=texto,
                size_hint_y=None,
                height=dp(100)
            )

            botao.bind(
                on_release=lambda instance,
                func=comando: func()
            )

            grid.add_widget(botao)

        scroll.add_widget(grid)

        self.root_layout.add_widget(scroll)

        rodape = Label(
            text="NICOLAS OPTIMIZER MOBILE",
            color=(0.35, 0.40, 0.50, 1),
            font_size=dp(9),
            size_hint_y=None,
            height=dp(25)
        )

        self.root_layout.add_widget(
            rodape
        )

    # ========================================================
    # STATUS
    # ========================================================

    def mudar_status(self, texto):

        self.status.text = (
            "[color=00FF88]● "
            + texto
            + "[/color]"
        )

        self.status.markup = True

    # ========================================================
    # POPUP
    # ========================================================

    def mensagem(self, titulo, texto):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        mensagem = Label(
            text=texto,
            halign="center",
            valign="middle"
        )

        mensagem.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        fechar = Button(
            text="FECHAR",
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=(0, 0.65, 0.48, 1)
        )

        layout.add_widget(mensagem)
        layout.add_widget(fechar)

        popup = Popup(
            title=titulo,
            content=layout,
            size_hint=(0.9, 0.55)
        )

        fechar.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # ========================================================
    # ANDROID INTENT
    # ========================================================

    def abrir_android(self, acao):

        if platform != "android":

            self.mensagem(
                "ANDROID",
                "Esta função foi criada para o Android.\n\n"
                "No PC ela não consegue abrir "
                "as configurações do celular."
            )

            return

        try:

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            activity = PythonActivity.mActivity

            intent = Intent(acao)

            activity.startActivity(intent)

            self.mudar_status(
                "TELA ABERTA"
            )

        except Exception as erro:

            self.mensagem(
                "ERRO",
                str(erro)
            )

    # ========================================================
    # APARELHO
    # ========================================================

    def info_aparelho(self):

        if platform != "android":

            self.mensagem(
                "APARELHO",
                "Execute no Android para obter "
                "as informações do aparelho."
            )

            return

        try:

            from jnius import autoclass

            Build = autoclass(
                "android.os.Build"
            )

            texto = (
                f"Fabricante: {Build.MANUFACTURER}\n\n"
                f"Marca: {Build.BRAND}\n\n"
                f"Modelo: {Build.MODEL}\n\n"
                f"Android: {Build.VERSION.RELEASE}\n\n"
                f"SDK: {Build.VERSION.SDK_INT}"
            )

            self.mensagem(
                "INFORMAÇÕES DO APARELHO",
                texto
            )

            self.mudar_status(
                "APARELHO ANALISADO"
            )

        except Exception as erro:

            self.mensagem(
                "ERRO",
                str(erro)
            )

    # ========================================================
    # BATERIA
    # ========================================================

    def bateria(self):

        if platform != "android":

            self.mensagem(
                "BATERIA",
                "Disponível quando o APK estiver "
                "rodando no Android."
            )

            return

        try:

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            IntentFilter = autoclass(
                "android.content.IntentFilter"
            )

            activity = PythonActivity.mActivity

            filtro = IntentFilter(
                Intent.ACTION_BATTERY_CHANGED
            )

            intent = activity.registerReceiver(
                None,
                filtro
            )

            level = intent.getIntExtra(
                "level",
                -1
            )

            scale = intent.getIntExtra(
                "scale",
                -1
            )

            porcentagem = int(
                level * 100 / scale
            )

            self.mensagem(
                "BATERIA",
                f"Nível atual: {porcentagem}%"
            )

            self.mudar_status(
                f"BATERIA {porcentagem}%"
            )

        except Exception as erro:

            self.mensagem(
                "ERRO",
                str(erro)
            )

    # ========================================================
    # ARMAZENAMENTO
    # ========================================================

    def armazenamento(self):

        try:

            total, usado, livre = shutil.disk_usage("/")

            self.mensagem(
                "ARMAZENAMENTO",
                f"Total: {total / 1024**3:.1f} GB\n\n"
                f"Usado: {usado / 1024**3:.1f} GB\n\n"
                f"Livre: {livre / 1024**3:.1f} GB"
            )

            self.mudar_status(
                "ARMAZENAMENTO VERIFICADO"
            )

        except Exception as erro:

            self.mensagem(
                "ERRO",
                str(erro)
            )

    # ========================================================
    # REDE
    # ========================================================

    def rede(self):

        self.abrir_android(
            "android.settings.WIRELESS_SETTINGS"
        )

    # ========================================================
    # WI-FI
    # ========================================================

    def wifi(self):

        self.abrir_android(
            "android.settings.WIFI_SETTINGS"
        )

    # ========================================================
    # BLUETOOTH
    # ========================================================

    def bluetooth(self):

        self.abrir_android(
            "android.settings.BLUETOOTH_SETTINGS"
        )

    # ========================================================
    # CONFIGURAÇÕES
    # ========================================================

    def configuracoes(self):

        self.abrir_android(
            "android.settings.SETTINGS"
        )

    # ========================================================
    # DESENVOLVEDOR
    # ========================================================

    def desenvolvedor(self):

        self.abrir_android(
            "android.settings.APPLICATION_DEVELOPMENT_SETTINGS"
        )

    # ========================================================
    # LIMPEZA
    # ========================================================

    def limpeza(self):

        self.mensagem(
            "LIMPEZA ANDROID",
            "O Android impede que um aplicativo comum "
            "apague livremente os arquivos de outros apps.\n\n"
            "Vamos usar as ferramentas oficiais do sistema."
        )

        self.abrir_android(
            "android.settings.INTERNAL_STORAGE_SETTINGS"
        )

        self.mudar_status(
            "ARMAZENAMENTO ABERTO"
        )

    # ========================================================
    # GAMING
    # ========================================================

    def gaming(self):

        self.mensagem(
            "GAMING",
            "O modo Gaming será adaptado para cada fabricante.\n\n"
            "Samsung, Xiaomi, Motorola e outras marcas "
            "possuem sistemas diferentes."
        )

        self.mudar_status(
            "MODO GAMING"
        )

    # ========================================================
    # APLICATIVOS
    # ========================================================

    def aplicativos(self):

        self.abrir_android(
            "android.settings.MANAGE_APPLICATIONS_SETTINGS"
        )

    # ========================================================
    # SOM
    # ========================================================

    def som(self):

        self.abrir_android(
            "android.settings.SOUND_SETTINGS"
        )

    # ========================================================
    # SISTEMA
    # ========================================================

    def sistema(self):

        self.abrir_android(
            "android.settings.DEVICE_INFO_SETTINGS"
        )

    # ========================================================
    # BLOQUEAR TELA
    # ========================================================

    def bloquear_tela(self):

        if platform != "android":

            self.mensagem(
                "BLOQUEAR TELA",
                "Disponível no APK Android."
            )

            return

        self.abrir_android(
            "android.settings.SECURITY_SETTINGS"
        )

    # ========================================================
    # REINICIAR
    # ========================================================

    def reiniciar(self):

        if platform != "android":

            self.mensagem(
                "REINICIAR",
                "Esta função é exclusiva do Android."
            )

            return

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        aviso = Label(
            text=(
                "ATENÇÃO!\n\n"
                "O aparelho será reiniciado.\n\n"
                "Em Android normal, um APK comum "
                "não possui permissão para forçar "
                "o reboot."
            ),
            halign="center"
        )

        confirmar = Button(
            text="TENTAR REINICIAR",
            size_hint_y=None,
            height=dp(50)
        )

        cancelar = Button(
            text="CANCELAR",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(aviso)
        layout.add_widget(confirmar)
        layout.add_widget(cancelar)

        popup = Popup(
            title="REINICIAR APARELHO",
            content=layout,
            size_hint=(0.9, 0.6)
        )

        cancelar.bind(
            on_release=popup.dismiss
        )

        confirmar.bind(
            on_release=lambda x:
            self.executar_reboot(popup)
        )

        popup.open()

    # ========================================================
    # REBOOT
    # ========================================================

    def executar_reboot(self, popup):

        popup.dismiss()

        try:

            resultado = subprocess.run(
                ["su", "-c", "reboot"],
                capture_output=True
            )

            if resultado.returncode == 0:

                self.mudar_status(
                    "REINICIANDO..."
                )

            else:

                self.mensagem(
                    "SEM PERMISSÃO",
                    "O Android bloqueou o reboot.\n\n"
                    "Para um APK comum isso é esperado. "
                    "O aparelho precisaria de acesso privilegiado/root."
                )

        except Exception:

            self.mensagem(
                "REINICIAR",
                "Não foi possível reiniciar automaticamente.\n\n"
                "Android bloqueia essa operação para "
                "aplicativos comuns sem acesso privilegiado."
            )


# ============================================================
# INICIAR
# ============================================================

if __name__ == "__main__":
    NicolasOptimizer().run()

