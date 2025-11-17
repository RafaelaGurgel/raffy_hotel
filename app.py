import flet as ft
from datetime import datetime

# ------------------ CLASSES ------------------
class Cliente:
    def __init__(self, nome, telefone, email, cliente_id):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cliente_id = cliente_id

class Quarto:
    def __init__(self, numero, tipo, preco, disponivel=True, imagem=""):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.disponivel = disponivel
        self.imagem = imagem

class Reserva:
    def __init__(self, cliente, quarto, check_in, check_out, status="Ativa"):
        self.cliente = cliente
        self.quarto = quarto
        self.check_in = check_in
        self.check_out = check_out
        self.status = status

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_quarto(self, quarto):
        self.quartos.append(quarto)

    def verificar_disponibilidade(self):
        return [q for q in self.quartos if q.disponivel]

    def criar_reserva(self, cliente, quarto, check_in, check_out):
        try:
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            return None
        if quarto.disponivel:
            quarto.disponivel = False
            reserva = Reserva(cliente, quarto, check_in, check_out)
            self.reservas.append(reserva)
            return reserva
        return None

    def cancelar_reserva(self, reserva):
        reserva.status = "Cancelada"
        reserva.quarto.disponivel = True

# ------------------ APP ------------------
def main(page: ft.Page):
    page.title = "🏨 Raffy Hotel - Sistema de Reservas"
    page.bgcolor = "#FDF6F0"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START

    sistema = GerenciadorDeReservas()

    # Adicionar quartos com imagens
    sistema.adicionar_quarto(Quarto(101, "Single", 250, True,
                                    "https://images.unsplash.com/photo-1501183638710-841dd1904471?auto=format&fit=crop&w=400"))
    sistema.adicionar_quarto(Quarto(102, "Double", 400, True,
                                    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=400"))
    sistema.adicionar_quarto(Quarto(201, "Suite", 700, True,
                                    "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=400"))

    # ------------------ FUNÇÕES DE NAVEGAÇÃO ------------------
    def mudar_tela(e):
        tela = telas.get(e.control.data)
        if tela:
            page.views.clear()
            page.views.append(tela())
            page.update()

    # ------------------ TELA INICIAL ------------------
    def tela_inicial():
        lista_quartos = ft.Row(
            [
                ft.Card(
                    elevation=10,
                    content=ft.Container(
                        content=ft.Column([
                            ft.Image(q.imagem, width=300, height=200, border_radius=15),
                            ft.Text(f"Quarto {q.numero} - {q.tipo}", size=18, weight="bold"),
                            ft.Text(f"R$ {q.preco}", size=16, color="#555"),
                            ft.Text("Disponível" if q.disponivel else "Ocupado",
                                    size=14, color="#2E8B57" if q.disponivel else "#B22222")
                        ], spacing=6),
                        padding=15,
                        border_radius=15,
                        bgcolor="white",
                        shadow=ft.BoxShadow(blur_radius=15, color="#D96C75", offset=(0,5)),
                        on_hover=lambda e: setattr(e.control, "shadow", ft.BoxShadow(blur_radius=20, color="#D96C75", offset=(0,8)))
                    )
                )
                for q in sistema.quartos
            ],
            scroll="auto",
            wrap=True,
            spacing=25
        )

        return ft.View(
            "/",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("🏨 Raffy Hotel", size=48, weight="bold", color="#D96C75"),
                        ft.Text("Hotel Boutique - Painel de Reservas", size=20, color="#555555")
                    ], spacing=8),
                    alignment=ft.alignment.center,
                    padding=15
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("📝 Realizar Reserva", data="/reserva", on_click=mudar_tela,
                                           style=ft.ButtonStyle(bgcolor="#D96C75", color="white", padding=15)),
                        ft.ElevatedButton("👤 Gerenciar Clientes", data="/clientes", on_click=mudar_tela,
                                           style=ft.ButtonStyle(bgcolor="#F3A683", color="white", padding=15)),
                        ft.ElevatedButton("📋 Ver Reservas", data="/listar_reservas", on_click=mudar_tela,
                                           style=ft.ButtonStyle(bgcolor="#6C5B7B", color="white", padding=15))
                    ], alignment="spaceAround", spacing=25),
                    padding=15
                ),
                lista_quartos
            ]
        )

    # ------------------ GERENCIAMENTO DE CLIENTES ------------------
    def tela_clientes():
        nome = ft.TextField(label="Nome", width=300)
        telefone = ft.TextField(label="Telefone", width=300)
        email = ft.TextField(label="E-mail", width=300)
        lista_clientes = ft.Column(spacing=10, scroll="auto")

        def atualizar_lista():
            lista_clientes.controls.clear()
            for c in sistema.clientes:
                lista_clientes.controls.append(
                    ft.Card(
                        elevation=4,
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"ID: {c.cliente_id}", weight="bold"),
                                ft.Text(f"Nome: {c.nome}"),
                                ft.Text(f"Telefone: {c.telefone}"),
                                ft.Text(f"E-mail: {c.email}")
                            ]),
                            padding=15
                        ),
                        width=400
                    )
                )
            page.update()

        def adicionar_cliente(e):
            if not nome.value.strip() or not email.value.strip():
                page.snack_bar = ft.SnackBar(content=ft.Text("Preencha nome e e-mail!"), bgcolor="#F85F73")
                page.snack_bar.open = True
                page.update()
                return

            cliente_id = len(sistema.clientes) + 1
            cliente = Cliente(nome.value.strip(), telefone.value.strip(), email.value.strip(), cliente_id)
            sistema.adicionar_cliente(cliente)

            nome.value = ""
            telefone.value = ""
            email.value = ""

            atualizar_lista()
            page.snack_bar = ft.SnackBar(content=ft.Text("Cliente adicionado com sucesso!"), bgcolor="#2E8B57")
            page.snack_bar.open = True
            page.update()

        def voltar(e):
            page.views.clear()
            page.views.append(tela_inicial())
            page.update()

        atualizar_lista()

        return ft.View(
            "/clientes",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar, style=ft.ButtonStyle(color="#D96C75")),
                            ft.Text("👤 Gerenciamento de Clientes", size=28, weight="bold", color="#D96C75"),
                        ]),
                        ft.Card(
                            elevation=8,
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("Adicionar Novo Cliente", size=18, weight="bold"),
                                    nome, telefone, email,
                                    ft.ElevatedButton("➕ Adicionar Cliente", on_click=adicionar_cliente,
                                                       style=ft.ButtonStyle(bgcolor="#D96C75", color="white"))
                                ], spacing=15),
                                padding=20
                            ),
                            margin=10
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("📋 Clientes Cadastrados", size=20, weight="bold"),
                                lista_clientes
                            ]),
                            padding=10
                        )
                    ], scroll="auto")
                )
            ]
        )

    # ------------------ FORMULÁRIO DE RESERVA ------------------
    def tela_reserva():
        clientes_dropdown = ft.Dropdown(width=300, hint_text="Selecione o cliente")
        quartos_dropdown = ft.Dropdown(width=300, hint_text="Selecione o quarto disponível")
        check_in = ft.TextField(label="Check-in (AAAA-MM-DD)", width=300)
        check_out = ft.TextField(label="Check-out (AAAA-MM-DD)", width=300)
        mensagem = ft.Text("", weight="bold", size=16)

        def carregar_dados():
            clientes_dropdown.options = [
                ft.dropdown.Option(key=str(c.cliente_id), text=f"{c.nome} - {c.email}")
                for c in sistema.clientes
            ]
            quartos_dropdown.options = [
                ft.dropdown.Option(key=str(q.numero), text=f"Quarto {q.numero} - {q.tipo} - R$ {q.preco}")
                for q in sistema.verificar_disponibilidade()
            ]
            page.update()

        def reservar(e):
            if not clientes_dropdown.value or not quartos_dropdown.value or not check_in.value or not check_out.value:
                mensagem.value = "❌ Preencha todos os campos!"
                mensagem.color = "#F85F73"
                page.update()
                return

            try:
                cliente_id = int(clientes_dropdown.value)
                cliente = next(c for c in sistema.clientes if c.cliente_id == cliente_id)
                quarto_num = int(quartos_dropdown.value)
                quarto = next(q for q in sistema.quartos if q.numero == quarto_num)

                reserva = sistema.criar_reserva(cliente, quarto, check_in.value, check_out.value)

                if reserva:
                    mensagem.value = f"✅ Reserva criada! Quarto {quarto.numero} para {cliente.nome}."
                    mensagem.color = "#2E8B57"
                    check_in.value = ""
                    check_out.value = ""
                    carregar_dados()
                else:
                    mensagem.value = "❌ Erro: datas inválidas ou quarto indisponível."
                    mensagem.color = "#F85F73"

            except (ValueError, StopIteration):
                mensagem.value = "❌ Erro ao processar reserva."
                mensagem.color = "#F85F73"

            page.update()

        def voltar(e):
            page.views.clear()
            page.views.append(tela_inicial())
            page.update()

        carregar_dados()

        return ft.View(
            "/reserva",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar, style=ft.ButtonStyle(color="#D96C75")),
                            ft.Text("📝 Criar Nova Reserva", size=28, weight="bold", color="#D96C75"),
                        ]),
                        ft.Card(
                            elevation=8,
                            content=ft.Container(
                                content=ft.Column([
                                    clientes_dropdown,
                                    quartos_dropdown,
                                    check_in,
                                    check_out,
                                    ft.ElevatedButton("✅ Confirmar Reserva", on_click=reservar,
                                                       style=ft.ButtonStyle(bgcolor="#D96C75", color="white")),
                                    mensagem
                                ], spacing=15),
                                padding=20,
                                border_radius=12,
                                bgcolor="white"
                            ),
                            width=400
                        )
                    ], scroll="auto")
                )
            ]
        )

    # ------------------ LISTAR RESERVAS ------------------
    def tela_listar_reservas():
        lista = ft.Column(spacing=10, scroll="auto")

        def atualizar():
            lista.controls.clear()
            for r in sistema.reservas:
                def criar_funcao_cancelar(reserva):
                    def cancelar(e):
                        sistema.cancelar_reserva(reserva)
                        atualizar()
                        page.snack_bar = ft.SnackBar(content=ft.Text("Reserva cancelada!"), bgcolor="#2E8B57")
                        page.snack_bar.open = True
                        page.update()
                    return cancelar

                status_color = "#2E8B57" if r.status == "Ativa" else "#F85F73"

                lista.controls.append(
                    ft.Card(
                        elevation=4,
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Reserva", weight="bold", size=16),
                                    ft.Text(r.status, color=status_color, weight="bold")
                                ]),
                                ft.Text(f"Cliente: {r.cliente.nome}"),
                                ft.Text(f"Quarto: {r.quarto.numero} - {r.quarto.tipo}"),
                                ft.Text(f"Check-in: {r.check_in}"),
                                ft.Text(f"Check-out: {r.check_out}"),
                                ft.Row([
                                    ft.ElevatedButton("❌ Cancelar", on_click=criar_funcao_cancelar(r),
                                                       style=ft.ButtonStyle(bgcolor="#F85F73", color="white"))
                                ]) if r.status == "Ativa" else ft.Container()
                            ]),
                            padding=15
                        )
                    )
                )
            page.update()

        def voltar(e):
            page.views.clear()
            page.views.append(tela_inicial())
            page.update()

        atualizar()

        return ft.View(
            "/listar_reservas",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar, style=ft.ButtonStyle(color="#D96C75")),
                            ft.Text("📋 Lista de Reservas", size=28, weight="bold", color="#D96C75"),
                        ]),
                        lista
                    ], scroll="auto")
                )
            ]
        )

    # ------------------ DICIONÁRIO DE TELAS ------------------
    telas = {
        "/": tela_inicial,
        "/reserva": tela_reserva,
        "/clientes": tela_clientes,
        "/listar_reservas": tela_listar_reservas,
    }

    page.views.append(tela_inicial())
    page.update()

# ------------------ RODAR ------------------
ft.app(target=main, view=ft.WEB_BROWSER)
